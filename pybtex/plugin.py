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

from pybtex.exceptions import PybtexError


class PluginNotFound(PybtexError):
    def __init__(self, plugin_group, name):
        message = u'plugin {name} not found in {plugin_group}'.format(
            plugin_group=plugin_group,
            name=name,
        )
        super(PluginNotFound, self).__init__(message)


class PluginLoader(object):
    def find_plugin(plugin_group, name):
        raise NotImplementedError


class BuiltInPluginLoader(PluginLoader):
    def find_plugin(self, plugin_group, name):
        m = __import__(str(plugin_group), globals(), locals(), [str(name)])
        try:
            return getattr(m, name)
        except AttributeError:
            raise PluginNotFound(plugin_group, name)


plugin_loaders = [BuiltInPluginLoader()]


def find_plugin(plugin_group, name):
    for loader in plugin_loaders:
        try:
            return loader.find_plugin(plugin_group, name)
        except PluginNotFound:
            continue
    raise PluginNotFound(plugin_group, name)
