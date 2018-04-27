"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='ipfs-pin-steem',  # Required
    version='1.0.7',  # Required
    description='Creates an object of all Hashes given from a dtube/dsound/dlive URL and pins it to an IPFS Node',  # Required
    license='Unlicensed',
    classifiers=[

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ipfs steem dtube dsound dlive',  # Optional
    packages=['ipfspinsteem'],#find_packages('ipfspinsteem'),  # Required
    install_requires=['ipfsapi'],
    extras_require={
    'steem':['steem'],
    'beem':['beem']
    },

    #package_data={  # Optional
    #    'ipfs-pin-steem': ['package_data.dat'],
    #},
    entry_points={  # Optional
        'console_scripts': [
            'ipfs-pin-steem=ipfspinsteem:main',
        ],
    },
)
