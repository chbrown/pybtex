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

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic

class MyHiglightStyle(Style):
    """
    Port of the default trac highlighter design.
    """

    default_style = ''

    styles = {
        Comment:                'italic #999988',
#        Comment.Preproc:        'bold noitalic #999999',
#        Comment.Special:        'bold #999999',

        Operator:               'bold',

        String:                 '#B81',
        String.Escape:          '#900',
#        String.Regex:           '#808000',

        Number:                 '#590 bold',

        Keyword:                'bold',
#        Keyword.Type:           '#445588',

        Name.Builtin:           '#840',
        Name.Function:          'bold #840',
        Name.Class:             'bold #900',
        Name.Exception:         'bold #A00',
        Name.Decorator:         '#840',
        Name.Namespace:         '#900',
#        Name.Variable:          '#088',
#        Name.Constant:          '#088',
        Name.Tag:               '#840',
#        Name.Tag:               '#000080',
#        Name.Attribute:         '#008080',
#        Name.Entity:            '#800080',

#        Generic.Heading:        '#999999',
#        Generic.Subheading:     '#aaaaaa',
#        Generic.Deleted:        'bg:#ffdddd #000000',
#        Generic.Inserted:       'bg:#ddffdd #000000',
        Generic.Error:          '#aa0000',
        Generic.Emph:           'italic',
        Generic.Strong:         'bold',
        Generic.Prompt:         '#555555',
        Generic.Output:         '#888888',
        Generic.Traceback:      '#aa0000',

        Error:                  'bg:#e3d2d2 #a61717'
    }
