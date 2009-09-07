#!/usr/bin/env python

# Copyright (C) 2009  Andrey Golovizin
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
import optparse

from pybtex.__version__ import version

from pybtex.textutils import capfirst, add_period


class CommandLine(object):
    options = ()
    option_defaults = None
    prog = None
    args = None
    description = ''
    num_args = 0

    def __init__(self):
        self.opt_parser = self.make_option_parser()

    def __call__(self):
        from pybtex.exceptions import PybtexError
        import pybtex.io
        try:
            self.main()
        except PybtexError, error:
            print >>pybtex.io.stderr, 'ERROR: %s' % capfirst(add_period(unicode(error)))
            sys.exit(1)

    def make_option_parser(self):
        opt_parser = optparse.OptionParser(
            prog=self.prog,
            usage='%prog ' + self.args,
            description=capfirst(add_period(self.description)),
            version='%%prog-%s' % version
        )
        for option_group, option_list in self.options:
            if option_group is None:
                container = opt_parser
            else:
                container = opt_parser.add_option_group(option_group)
            for option in option_list:
                container.add_option(option)

        if self.option_defaults:
            opt_parser.set_defaults(**self.option_defaults)

        return opt_parser

    def run(self, options, args):
        raise NotImplementedError

    def main(self):
        options, args = self.opt_parser.parse_args()
        if len(args) != self.num_args:
            self.opt_parser.print_help()
            sys.exit(1)

        self.run(options, args)
