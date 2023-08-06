from distutils.core import setup
setup(
    name = 'scaleapi',
    packages = ['scaleapi'],
    version = '0.1.7',
    description = 'The official Python client library for the Scale API, the API for human labor.',
    author = 'Calvin Huang',
    author_email = 'c@lvin.me',
    url = 'https://github.com/scaleapi/scaleapi-python-client',
    download_url = 'https://github.com/scaleapi/scaleapi-python-client/tarball/0.1.2',
    keywords = ['scale', 'scaleapi', 'humans', 'tasks', 'categorization', 'transcription', 'annotation', 'comparison', 'data collection', 'phone call', 'audio transcription'],
    install_requires = ['requests>=2.4.2', 'enum34'],
    classifiers = ['Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries']
)
