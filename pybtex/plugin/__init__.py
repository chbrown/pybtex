# Copyright (C) 2007, 2008, 2009  Andrey Golovizin
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from itertools import chain

from pybtex.exceptions import PybtexError


class PluginGroupNotFound(PybtexError):
    def __init__(self, group_name):
        message = u'plugin group {group_name} not found'.format(
            group_name=group_name,
        )
        super(PluginGroupNotFound, self).__init__(message)


class PluginNotFound(PybtexError):
    def __init__(self, plugin_group, name, filename):
        message = u'plugin {name} not found in {plugin_group}'.format(
            plugin_group=plugin_group,
            name=name,
        )
        super(PluginNotFound, self).__init__(message)


class Plugin(object):
    name = None
    aliases = ()
    suffixes = ()
    default_plugin = None


class PluginLoader(object):
    def find_plugin(plugin_group, name):
        raise NotImplementedError

    def enumerate_plugin_names(plugin_group):
        raise NotImplementedError


class BuiltInPluginLoader(PluginLoader):
    def get_group_info(self, plugin_group):
        from pybtex.plugin.registry import plugin_registry
        try:
            return plugin_registry[plugin_group]
        except KeyError:
            raise PluginGroupNotFound(plugin_group)

    def find_plugin(self, plugin_group, name=None, filename=None):
        plugin_group_info = self.get_group_info(plugin_group)
        module_name = None
        if name:
            if name in plugin_group_info['plugins']:
                module_name = name
            elif name in plugin_group_info['aliases']:
                module_name = plugin_group_info['aliases'][name]
            else:
                raise PluginNotFound(plugin_group, name)
        elif filename:
            raise NotImplementedError  # FIXME
        else:
            module_name = plugin_group_info['default_plugin']

        class_name = plugin_group_info['class_name']
        return self.import_plugin(plugin_group, module_name, class_name)

    def import_plugin(self, plugin_group, module_name, class_name):
        module = __import__(str(plugin_group), globals(), locals(), [str(module_name)])
        #return getattr(getattr(module, module_name), class_name)
        return getattr(module, module_name)

    def enumerate_plugin_names(self, plugin_group):
        plugin_group_info = self.get_group_info(plugin_group)
        return plugin_group_info['plugins']


plugin_loaders = [BuiltInPluginLoader()]


def find_plugin(plugin_group, name=None, filename=None):
    for loader in plugin_loaders:
        try:
            return loader.find_plugin(plugin_group, name, filename)
        except PluginNotFound:
            continue
    raise PluginNotFound(plugin_group, name, filename)


def enumerate_plugin_names(plugin_group):
    results = (
        loader.enumerate_plugin_names(plugin_group)
        for loader in plugin_loaders
    )
    return chain(*results)
