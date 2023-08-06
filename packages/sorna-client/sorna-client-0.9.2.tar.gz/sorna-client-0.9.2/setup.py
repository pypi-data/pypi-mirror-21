# Always prefer setuptools over distutils
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ""


setup(
    name='sorna-client',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.2',
    description='Sorna API Client Library',
    long_description=long_description,
    url='https://github.com/lablup/sorna-client',
    author='Lablup Inc.',
    author_email='joongi@lablup.com',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],

    packages=['sorna', 'sorna.asyncio'],

    python_requires='>=3.6',
    install_requires=[
        'aiohttp~=2.0.7',
        'namedlist',
        'python-dateutil>=2.5',
        'simplejson',
        'requests',
    ],
    extras_require={
        'dev': [],
        'test': ['pytest', 'pytest-mock', 'pytest-asyncio', 'asynctest'],
    },
    data_files=[],
)
