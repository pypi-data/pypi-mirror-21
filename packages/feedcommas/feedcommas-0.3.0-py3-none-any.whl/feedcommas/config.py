# Copyright (C) 2017 Michał Góral.
#
# This file is part of Feed Commas
#
# Feed Commas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Feed Commas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Feed Commas. If not, see <http://www.gnu.org/licenses/>.

'''Reader and handler of globally-available app configuration.'''

import os
import configparser

from collections import OrderedDict

import mgcomm.xdg
import mgcomm.env

from feedcommas.locale import _
from feedcommas.utils import mkdir_p, eprint

_cfg = None
_path = None

_defaults = OrderedDict((
    ('server', OrderedDict((
        ('address', 'https://commafeed.com'),
        ('username', ''),
        ('password', ''),
        ('password-cmd', ''),
        ('timeout', 10),
    ))),

    ('keys', OrderedDict((
        ('nav-down', 'j'),
        ('nav-up', 'k'),
        ('nav-right', 'l'),
        ('nav-left', 'h'),
        ('open-browser', 'c-]'),
        ('read-all', ''),
        ('read-toggle', 'R'),
        ('star-toggle', 'S'),
        ('show-all', ''),
        ('show-unread', ''),
        ('refresh', 'r'),
        ('sync', ''),
        ('offline-toggle', ''),
        ('quit', 'q'),
    ))),

    ('settings', OrderedDict((
        ('mark-read-time', 2),
        ('show-read', False),
        ('supported-colors', 256),
        ('bright-bold', False),
        ('html-filter', 'builtin'),
        ('offline', False),
        ('window-title', 'Feed Commas'),
        ('workers', 2),
        ('status-line', '{unread}{offline} {notif}'),
        ('sync-article-count', 1000),
    ))),

    ('colors', OrderedDict((
        ('article-title', 'yellow'),
        ('article-title-focus', 'light blue'),
        ('article-border-focus', 'light blue'),
        ('metadata', 'light gray'),
        ('menu-focus-fg', 'white'),
        ('menu-focus-bg', 'light blue'),
        ('menu-line', 'dark gray'),
        ('menu-selected', 'light red'),
        ('status-fg', 'black'),
        ('status-bg', 'light gray'),
        ('error-fg', 'white'),
        ('error-bg', 'dark red'),
    ))),
))


class _NoDefault:
    pass
_NoDefaultInstance = _NoDefault()


class ConfigNotWritable(Exception):
    '''Exception thrown when specified configuration file is not writable.'''
    pass


class _ConfigParser(configparser.ConfigParser):  # pylint: disable=too-many-ancestors
    '''ConfigParser subclass which tracks options modifications.'''
    def __init__(self, *args, **kwargs):
        self._modified = False
        super().__init__(*args, **kwargs)

    @property
    def modified(self):
        '''Tells whether current configuration was modified since last write.'''
        return self._modified

    def set(self, *args, **kwargs):
        '''Re-implementation of ConfigParser.set'''
        super().set(*args, **kwargs)
        self._modified = True

    def write(self, *args, **kwargs):
        '''Re-implementation of ConfigParser.write'''
        super().write(*args, **kwargs)
        self._modified = False


def set_path(path):
    '''Hardcode configuration file path.'''
    if _path_seems_writable(path):
        global _path
        _path = path
    else:
        raise ConfigNotWritable(path)


def config_path():
    '''Returns a path to the configuration file, which is searched in a way
    specified by XDG Base Directory Specification:
    https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

    This function doesn't ensure that configuration file indeed exists. If no
    suitable configuration exists, it returns a user-specific path which is best
    suitable (according to XDG spec).'''
    if _path:
        return _path

    app_name = 'feed-commas'
    cfg_name = 'config.ini'

    default_cfg_dir = os.path.join(mgcomm.env.home(), '.config')
    cfg_home = os.getenv('XDG_CONFIG_HOME', default_cfg_dir)
    default_path = os.path.join(cfg_home, app_name, cfg_name)

    return mgcomm.xdg.config(app_name, cfg_name, default_path)


def config(section=None):
    '''Returns a global (shared) configuration object. If it hasn't been created
    yet, it is read from the mix of default values and configuration file.'''
    global _cfg  # pylint: disable=global-statement
    if _cfg is None:
        _cfg = _ConfigParser()

        # this preserves the order of configuration file
        _cfg.read(config_path())
        for section, opts in _defaults.items():
            if not _cfg.has_section(section):
                _cfg.add_section(section)
            for option_name, value in opts.items():
                if not _cfg.has_option(section, option_name):
                    _cfg.set(section, option_name, str(value))
    return _cfg


def exists():
    '''Returns whether there was found any configuration file.'''
    return os.path.exists(config_path())


def write_config(cfg, force=False):
    '''Writes back any changes in configuration to the file. If there's no
    configuration under a `config_path()`, creates one. If `force` is set to
    True, writes configuration file even it wasn't modified.'''
    if force is False and cfg.modified is False:
        return

    cfg_path = config_path()
    try:
        mkdir_p(os.path.dirname(cfg_path))
        with open(cfg_path, 'w') as configfile:
            cfg.write(configfile)
    except Exception as e:  # pylint: disable=broad-except
        eprint(_('Configuration not saved because of error: %s') % str(e))


def get_value(spec, default=_NoDefaultInstance):
    '''Properly returns a value of the field, even if it isn't set or is set to
    an empty value. Uses a global configuration and field name is given as a
    string in form "section_name.field_name".'''
    section_name, _, field_name = spec.partition('.')

    assert section_name
    assert field_name

    if default is _NoDefaultInstance:
        default = _defaults[section_name][field_name]

    section = config()[section_name]

    try:
        if isinstance(default, bool):
            return section.getboolean(field_name, fallback=default)
        elif isinstance(default, int):
            return section.getint(field_name, fallback=default)
        elif isinstance(default, float):
            return section.getfloat(field_name, fallback=default)
    except ValueError:
        pass

    ret = section.get(field_name, fallback=default)
    if not ret:  # correct; handles a case when ret is e.g. empty string
        ret = default
    return type(default)(ret)  # cast to the correct type


def set_value(spec, value):
    '''Sets configuration value for a given `spec`. `spec` is given as a string
    in form "section_name.field_name".'''
    section_name, _, field_name = spec.partition('.')

    assert section_name
    assert field_name
    assert isinstance(value, type(_defaults[section_name][field_name]))

    section = config()[section_name]
    section[field_name] = str(value)


def _path_seems_writable(path):
    if os.path.exists(path) and not os.path.isdir(path):
        return True
    elif os.path.isdir(path):
        return False

    # Feed Commas does "mkdir -p", so we need to check the nearest existing
    # directory for being writable and executable.
    directory = os.path.dirname(path)

    while directory and not os.path.isdir(directory):
        directory = os.path.dirname(directory)

    if not directory:
        directory = '.'

    return os.access(directory, os.W_OK | os.X_OK)
