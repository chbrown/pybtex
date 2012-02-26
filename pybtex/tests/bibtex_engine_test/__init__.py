import os
import pkgutil
import posixpath
from contextlib import contextmanager
from shutil import rmtree
from tempfile import mkdtemp


from pybtex.bibtex import make_bibliography


@contextmanager
def cd_tempdir():
    current_workdir = os.getcwd()
    tempdir = mkdtemp(prefix='pybtex_test_')
    os.chdir(tempdir)
    try:
        yield tempdir
    finally:
        os.chdir(current_workdir)
        rmtree(tempdir)


def copy_resource(package, resource):
    filename = posixpath.basename(resource)
    data = pkgutil.get_data(package, resource)
    with open(filename, 'wb') as data_file:
        data_file.write(data)


def copy_files(test_name):
    for filename in 'test.bib', 'test.aux':
        copy_resource('pybtex.tests.bibtex_engine_test', posixpath.join(test_name, filename))


def bibtex_engine_test(test_name='xampl'):
    with cd_tempdir() as tempdir:
        copy_files(test_name)
        make_bibliography('test.aux')
        with open('test.bbl', 'rb') as result_file:
            result = result_file.read()
        correct_result = pkgutil.get_data('pybtex.tests.bibtex_engine_test', posixpath.join(test_name, 'result.bbl'))
        assert result == correct_result
