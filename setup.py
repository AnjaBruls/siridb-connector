from distutils.core import setup
import setuptools
from siridb.connector import __version__


VERSION = __version__


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='siridb-connector',
    packages=[
        'siridb',
        'siridb.connector',
        'siridb.connector.lib'],
    version=VERSION,
    description='SiriDB Connector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeroen van der Heijden',
    author_email='jeroen@transceptor.technology',
    url='https://github.com/SiriDB/siridb-connector',
    download_url=
        'https://github.com/SiriDB/'
        'siridb-connector/tarball/{}'.format(VERSION),
    keywords=['siridb', 'connector', 'database', 'client'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database',
        'Topic :: Software Development'
    ],
    install_requires=['qpack']
)
