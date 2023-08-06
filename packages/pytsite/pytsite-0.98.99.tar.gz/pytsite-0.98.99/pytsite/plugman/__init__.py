"""PytSite Plugin Manager.
"""
# Public API
from . import _error as error
from ._api import get_plugins_path, get_plugin_info, install, uninstall, is_installed, start, is_started, \
    get_license_info, get_installed_plugins, get_remote_plugins, get_required_plugins, is_api_host, is_api_dev_host

# Locally necessary imports
from pytsite import reload as _reload, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_plugman_started = False


def _cron_check_license():
    global _plugman_started

    try:
        get_license_info()
        if not _plugman_started:
            _reload.reload()
    except error.InvalidLicense:
        if _plugman_started:
            _reload.reload()


def _init():
    from os import mkdir, path
    from pytsite import settings, lang, assetman, permissions, http_api, logger, events, cron
    from . import _settings_form, _eh, _http_api

    # Resources
    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**/*.less')
    assetman.t_js(__name__ + '@**/*.js')

    # Create 'plugins' package
    plugins_path = get_plugins_path()
    if not path.exists(plugins_path):
        mkdir(plugins_path, 0o755)
        with open(path.join(plugins_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Application Plugins.\n"""\n')

    # HTTP API
    http_api.handle('POST', 'plugman/install/<name>', _http_api.post_install, 'pytsite.plugman@post_install')
    http_api.handle('POST', 'plugman/uninstall/<name>', _http_api.post_uninstall, 'pytsite.plugman@post_uninstall')
    http_api.handle('POST', 'plugman/upgrade/<name>', _http_api.post_upgrade, 'pytsite.plugman@post_upgrade')

    if not is_api_dev_host():
        # Permissions
        permissions.define_permission('pytsite.plugman.manage', 'pytsite.plugman@plugin_management', 'app')

        # Settings
        settings.define('plugman', _settings_form.Form, 'pytsite.plugman@plugins', 'fa fa-plug',
                        'pytsite.plugman.manage')

        # Install required plugins
        for plugin_name in _reg.get('plugman.plugins', set()):
            if not is_installed(plugin_name):
                install(plugin_name)

        # Check license at start and then by cron, but don't do this at plugins host
        if not is_api_host():
            try:
                get_license_info()
                cron.hourly(_cron_check_license)
            except error.InvalidLicense:
                logger.error('Plugins license expired or invalid. Plugins will not be loaded.')
                return
            except error.ApiRequestError as e:
                logger.error('Error while communicating with plugin API. Plugins will not be loaded.')
                logger.error(e)
                return

        # Event handlers
        events.listen('pytsite.update', _eh.update)
        events.listen('pytsite.update.after', _eh.update_after)

    # Start installed plugins
    for p_name in get_installed_plugins():
        try:
            if not is_started(p_name):
                start(p_name)
        except error.PluginStartError as e:
            logger.error(e, exc_info=e)

    global _plugman_started
    _plugman_started = True


_init()
