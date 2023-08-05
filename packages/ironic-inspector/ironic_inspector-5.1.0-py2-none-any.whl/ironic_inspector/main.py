# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import eventlet  # noqa
eventlet.monkey_patch()

import functools
import os
import re
import ssl
import sys

import flask
from futurist import periodics
from oslo_config import cfg
from oslo_log import log
from oslo_utils import uuidutils
import werkzeug

from ironic_inspector import api_tools
from ironic_inspector.common.i18n import _
from ironic_inspector.common import ironic as ir_utils
from ironic_inspector.common import swift
from ironic_inspector import conf  # noqa
from ironic_inspector import db
from ironic_inspector import firewall
from ironic_inspector import introspect
from ironic_inspector import node_cache
from ironic_inspector.plugins import base as plugins_base
from ironic_inspector import process
from ironic_inspector import rules
from ironic_inspector import utils

CONF = cfg.CONF


app = flask.Flask(__name__)
LOG = utils.getProcessingLogger(__name__)

MINIMUM_API_VERSION = (1, 0)
# TODO(dtantsur): set to the current version as soon we move setting IPMI
# credentials support completely.
DEFAULT_API_VERSION = (1, 8)
CURRENT_API_VERSION = (1, 9)
_LOGGING_EXCLUDED_KEYS = ('logs',)


def _get_version():
    ver = flask.request.headers.get(conf.VERSION_HEADER,
                                    _DEFAULT_API_VERSION)
    try:
        requested = tuple(int(x) for x in ver.split('.'))
    except (ValueError, TypeError):
        return error_response(_('Malformed API version: expected string '
                                'in form of X.Y'), code=400)
    return requested


def _format_version(ver):
    return '%d.%d' % ver


_DEFAULT_API_VERSION = _format_version(DEFAULT_API_VERSION)


def error_response(exc, code=500):
    res = flask.jsonify(error={'message': str(exc)})
    res.status_code = code
    LOG.debug('Returning error to client: %s', exc)
    return res


def convert_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except utils.Error as exc:
            return error_response(exc, exc.http_code)
        except werkzeug.exceptions.HTTPException as exc:
            return error_response(exc, exc.code or 400)
        except Exception as exc:
            LOG.exception('Internal server error')
            msg = _('Internal server error')
            if CONF.debug:
                msg += ' (%s): %s' % (exc.__class__.__name__, exc)
            return error_response(msg)

    return wrapper


@app.before_request
def check_api_version():
    requested = _get_version()

    if requested < MINIMUM_API_VERSION or requested > CURRENT_API_VERSION:
        return error_response(_('Unsupported API version %(requested)s, '
                                'supported range is %(min)s to %(max)s') %
                              {'requested': _format_version(requested),
                               'min': _format_version(MINIMUM_API_VERSION),
                               'max': _format_version(CURRENT_API_VERSION)},
                              code=406)


@app.after_request
def add_version_headers(res):
    res.headers[conf.MIN_VERSION_HEADER] = '%s.%s' % MINIMUM_API_VERSION
    res.headers[conf.MAX_VERSION_HEADER] = '%s.%s' % CURRENT_API_VERSION
    return res


def create_link_object(urls):
    links = []
    for url in urls:
        links.append({"rel": "self",
                      "href": os.path.join(flask.request.url_root, url)})
    return links


def generate_resource_data(resources):
    data = []
    for resource in resources:
        item = {}
        item['name'] = str(resource).split('/')[-1]
        item['links'] = create_link_object([str(resource)[1:]])
        data.append(item)
    return data


def generate_introspection_status(node):
    """Return a dict representing current node status.

    :param node: a NodeInfo instance
    :return: dictionary
    """
    started_at = node.started_at.isoformat()
    finished_at = node.finished_at.isoformat() if node.finished_at else None

    status = {}
    status['uuid'] = node.uuid
    status['finished'] = bool(node.finished_at)
    status['started_at'] = started_at
    status['finished_at'] = finished_at
    status['error'] = node.error
    status['links'] = create_link_object(
        ["v%s/introspection/%s" % (CURRENT_API_VERSION[0], node.uuid)])
    return status


@app.route('/', methods=['GET'])
@convert_exceptions
def api_root():
    versions = [
        {
            "status": "CURRENT",
            "id": '%s.%s' % CURRENT_API_VERSION,
        },
    ]

    for version in versions:
        version['links'] = create_link_object(
            ["v%s" % version['id'].split('.')[0]])

    return flask.jsonify(versions=versions)


@app.route('/<version>', methods=['GET'])
@convert_exceptions
def version_root(version):
    pat = re.compile("^\/%s\/[^\/]*?$" % version)

    resources = []
    for url in app.url_map.iter_rules():
        if pat.match(str(url)):
            resources.append(url)

    if not resources:
        raise utils.Error(_('Version not found.'), code=404)

    return flask.jsonify(resources=generate_resource_data(resources))


@app.route('/v1/continue', methods=['POST'])
@convert_exceptions
def api_continue():
    data = flask.request.get_json(force=True)
    if not isinstance(data, dict):
        raise utils.Error(_('Invalid data: expected a JSON object, got %s') %
                          data.__class__.__name__)

    logged_data = {k: (v if k not in _LOGGING_EXCLUDED_KEYS else '<hidden>')
                   for k, v in data.items()}
    LOG.debug("Received data from the ramdisk: %s", logged_data,
              data=data)

    return flask.jsonify(process.process(data))


# TODO(sambetts) Add API discovery for this endpoint
@app.route('/v1/introspection/<node_id>', methods=['GET', 'POST'])
@convert_exceptions
def api_introspection(node_id):
    utils.check_auth(flask.request)

    if flask.request.method == 'POST':
        new_ipmi_password = flask.request.args.get('new_ipmi_password',
                                                   type=str,
                                                   default=None)
        if new_ipmi_password:
            new_ipmi_username = flask.request.args.get('new_ipmi_username',
                                                       type=str,
                                                       default=None)
            new_ipmi_credentials = (new_ipmi_username, new_ipmi_password)
        else:
            new_ipmi_credentials = None

        if new_ipmi_credentials and _get_version() >= (1, 9):
            return _('Setting IPMI credentials is deprecated and not allowed '
                     'starting with API version 1.9'), 400

        introspect.introspect(node_id,
                              new_ipmi_credentials=new_ipmi_credentials,
                              token=flask.request.headers.get('X-Auth-Token'))
        return '', 202
    else:
        node_info = node_cache.get_node(node_id)
        return flask.json.jsonify(generate_introspection_status(node_info))


@app.route('/v1/introspection', methods=['GET'])
@convert_exceptions
def api_introspection_statuses():
    utils.check_auth(flask.request)

    nodes = node_cache.get_node_list(
        marker=api_tools.marker_field(),
        limit=api_tools.limit_field(default=CONF.api_max_limit)
    )
    data = {
        'introspection': [generate_introspection_status(node)
                          for node in nodes]
    }
    return flask.json.jsonify(data)


@app.route('/v1/introspection/<node_id>/abort', methods=['POST'])
@convert_exceptions
def api_introspection_abort(node_id):
    utils.check_auth(flask.request)
    introspect.abort(node_id, token=flask.request.headers.get('X-Auth-Token'))
    return '', 202


@app.route('/v1/introspection/<node_id>/data', methods=['GET'])
@convert_exceptions
def api_introspection_data(node_id):
    utils.check_auth(flask.request)

    if CONF.processing.store_data == 'swift':
        if not uuidutils.is_uuid_like(node_id):
            node = ir_utils.get_node(node_id, fields=['uuid'])
            node_id = node.uuid
        res = swift.get_introspection_data(node_id)
        return res, 200, {'Content-Type': 'application/json'}
    else:
        return error_response(_('Inspector is not configured to store data. '
                                'Set the [processing] store_data '
                                'configuration option to change this.'),
                              code=404)


@app.route('/v1/introspection/<node_id>/data/unprocessed', methods=['POST'])
@convert_exceptions
def api_introspection_reapply(node_id):
    utils.check_auth(flask.request)

    if flask.request.content_length:
        return error_response(_('User data processing is not '
                                'supported yet'), code=400)

    if CONF.processing.store_data == 'swift':
        process.reapply(node_id)
        return '', 202
    else:
        return error_response(_('Inspector is not configured to store'
                                ' data. Set the [processing] '
                                'store_data configuration option to '
                                'change this.'), code=400)


def rule_repr(rule, short):
    result = rule.as_dict(short=short)
    result['links'] = [{
        'href': flask.url_for('api_rule', uuid=result['uuid']),
        'rel': 'self'
    }]
    return result


@app.route('/v1/rules', methods=['GET', 'POST', 'DELETE'])
@convert_exceptions
def api_rules():
    utils.check_auth(flask.request)

    if flask.request.method == 'GET':
        res = [rule_repr(rule, short=True) for rule in rules.get_all()]
        return flask.jsonify(rules=res)
    elif flask.request.method == 'DELETE':
        rules.delete_all()
        return '', 204
    else:
        body = flask.request.get_json(force=True)
        if body.get('uuid') and not uuidutils.is_uuid_like(body['uuid']):
            raise utils.Error(_('Invalid UUID value'), code=400)

        rule = rules.create(conditions_json=body.get('conditions', []),
                            actions_json=body.get('actions', []),
                            uuid=body.get('uuid'),
                            description=body.get('description'))

        response_code = (200 if _get_version() < (1, 6) else 201)
        return flask.make_response(
            flask.jsonify(rule_repr(rule, short=False)), response_code)


@app.route('/v1/rules/<uuid>', methods=['GET', 'DELETE'])
@convert_exceptions
def api_rule(uuid):
    utils.check_auth(flask.request)

    if flask.request.method == 'GET':
        rule = rules.get(uuid)
        return flask.jsonify(rule_repr(rule, short=False))
    else:
        rules.delete(uuid)
        return '', 204


@app.errorhandler(404)
def handle_404(error):
    return error_response(error, code=404)


def periodic_update():  # pragma: no cover
    try:
        firewall.update_filters()
    except Exception:
        LOG.exception('Periodic update of firewall rules failed')


def periodic_clean_up():  # pragma: no cover
    try:
        if node_cache.clean_up():
            firewall.update_filters()
        sync_with_ironic()
    except Exception:
        LOG.exception('Periodic clean up of node cache failed')


def sync_with_ironic():
    ironic = ir_utils.get_client()
    # TODO(yuikotakada): pagination
    ironic_nodes = ironic.node.list(limit=0)
    ironic_node_uuids = {node.uuid for node in ironic_nodes}
    node_cache.delete_nodes_not_in_list(ironic_node_uuids)


def create_ssl_context():
    if not CONF.use_ssl:
        return

    MIN_VERSION = (2, 7, 9)

    if sys.version_info < MIN_VERSION:
        LOG.warning('Unable to use SSL in this version of Python: '
                    '%(current)s, please ensure your version of Python is '
                    'greater than %(min)s to enable this feature.',
                    {'current': '.'.join(map(str, sys.version_info[:3])),
                     'min': '.'.join(map(str, MIN_VERSION))})
        return

    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    if CONF.ssl_cert_path and CONF.ssl_key_path:
        try:
            context.load_cert_chain(CONF.ssl_cert_path, CONF.ssl_key_path)
        except IOError as exc:
            LOG.warning('Failed to load certificate or key from defined '
                        'locations: %(cert)s and %(key)s, will continue '
                        'to run with the default settings: %(exc)s',
                        {'cert': CONF.ssl_cert_path, 'key': CONF.ssl_key_path,
                         'exc': exc})
        except ssl.SSLError as exc:
            LOG.warning('There was a problem with the loaded certificate '
                        'and key, will continue to run with the default '
                        'settings: %s', exc)
    return context


class Service(object):
    _periodics_worker = None

    def setup_logging(self, args):
        log.register_options(CONF)
        CONF(args, project='ironic-inspector')

        log.set_defaults(default_log_levels=[
            'sqlalchemy=WARNING',
            'iso8601=WARNING',
            'requests=WARNING',
            'urllib3.connectionpool=WARNING',
            'keystonemiddleware=WARNING',
            'swiftclient=WARNING',
            'keystoneauth=WARNING',
            'ironicclient=WARNING'
        ])
        log.setup(CONF, 'ironic_inspector')

        LOG.debug("Configuration:")
        CONF.log_opt_values(LOG, log.DEBUG)

    def init(self):
        if CONF.auth_strategy != 'noauth':
            utils.add_auth_middleware(app)
        else:
            LOG.warning('Starting unauthenticated, please check'
                        ' configuration')

        if CONF.processing.store_data == 'none':
            LOG.warning('Introspection data will not be stored. Change '
                        '"[processing] store_data" option if this is not '
                        'the desired behavior')
        elif CONF.processing.store_data == 'swift':
            LOG.info('Introspection data will be stored in Swift in the '
                     'container %s', CONF.swift.container)

        utils.add_cors_middleware(app)

        db.init()

        try:
            hooks = [ext.name for ext in
                     plugins_base.processing_hooks_manager()]
        except KeyError as exc:
            # callback function raises MissingHookError derived from KeyError
            # on missing hook
            LOG.critical('Hook(s) %s failed to load or was not found',
                         str(exc))
            sys.exit(1)

        LOG.info('Enabled processing hooks: %s', hooks)

        if CONF.firewall.manage_firewall:
            firewall.init()

        periodic_update_ = periodics.periodic(
            spacing=CONF.firewall.firewall_update_period,
            enabled=CONF.firewall.manage_firewall
        )(periodic_update)
        periodic_clean_up_ = periodics.periodic(
            spacing=CONF.clean_up_period
        )(periodic_clean_up)

        self._periodics_worker = periodics.PeriodicWorker(
            callables=[(periodic_update_, None, None),
                       (periodic_clean_up_, None, None)],
            executor_factory=periodics.ExistingExecutor(utils.executor()))
        utils.executor().submit(self._periodics_worker.start)

    def shutdown(self):
        LOG.debug('Shutting down')

        firewall.clean_up()

        if self._periodics_worker is not None:
            self._periodics_worker.stop()
            self._periodics_worker.wait()
            self._periodics_worker = None

        if utils.executor().alive:
            utils.executor().shutdown(wait=True)

        LOG.info('Shut down successfully')

    def run(self, args, application):
        self.setup_logging(args)

        app_kwargs = {'host': CONF.listen_address,
                      'port': CONF.listen_port}

        context = create_ssl_context()
        if context:
            app_kwargs['ssl_context'] = context

        self.init()
        try:
            application.run(**app_kwargs)
        finally:
            self.shutdown()


def main(args=sys.argv[1:]):  # pragma: no cover
    service = Service()
    service.run(args, app)
