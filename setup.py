#!/usr/bin/env python

import sys
import os
from glob import glob1
from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.log import info

progname = 'pybtex'
from pybtex import __version__ as version

def list_modules():
    modules = []
    def add(art, dirname, filenames):
        dirs = dirname.split(os.path.sep)
        if '.svn' in dirs:
            return
        module = '.'.join(dirs)
        modules.append(module)
    os.path.walk(progname, add, None)
    return modules

class InstallData(install_data):
    def run(self):
        # we don't usually have the tools to compile po files in win32
        if sys.platform != 'win32':
            self.data_files.extend(self._compile_po_files())

        install_data.run(self)

    def _compile_po_files(self):
        data_files = []
        for po in glob1('po', '*.po'):
            lang = os.path.splitext(po)[0]
            po = os.path.join('po', po)
            mo = os.path.join('locale', lang,
                              'LC_MESSAGES', '%s.mo' % progname)

            if not os.path.exists(mo) or newer(po, mo):
                directory = os.path.dirname(mo)
                if not os.path.exists(directory):
                    info("creating %s" % directory)
                    os.makedirs(directory)
                cmd = 'msgfmt -o %s %s' % (mo, po)
                info('compiling %s -> %s' % (po, mo))
                if os.system(cmd) != 0:
                    raise SystemExit("Error while running msgfmt")
            dest = os.path.dirname(os.path.join('share', mo))
            data_files.append((dest, [mo]))

        return data_files

data_files = [
    (os.path.join('share', 'doc', '%s-%s' % (progname, version)) , ('README', 'COPYING', 'NEWS'))
]

setup(name=progname,
    version=version,
    description='Bibliography processor in Python',
    author='Andrey Golovizin',
    author_email='golovizin@gorodok.net',
    url='http://pybtex.sourceforge.net/',
    packages=list_modules(),
    scripts=[os.path.join('scripts', progname)],
    data_files=data_files,
    cmdclass={'install_data': InstallData}
    )
