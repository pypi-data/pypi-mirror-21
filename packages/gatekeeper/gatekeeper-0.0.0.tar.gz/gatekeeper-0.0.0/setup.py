from setuptools import setup

long_description = """
Gatekeeper is a python library that uses the Web Ser Gateway Interface (WSGI) to handle incoming HTTP requests. It's packed with features to help routing, handling, and extracting information from requests, as well as options to help writing appropriate responses.
"""

setup(
    name = 'gatekeeper',
    version = '0.0.0',

    packages = ['gatekeeper', 'gatekeeper.endpoints', 'gatekeeper.requests', 'gatekeeper.responses'],
    include_package_data = True,

    install_requires = [],
    entry_points = {'console_scripts': []},

    author = 'Hugo Leonardo Leão Mota',
    author_email = 'hugo.txt@gmail.com',
    license = 'MIT',
    url = 'https://github.com/hugollm/gatekeeper',

    keywords = 'gatekeeper http routing wsgi endpoint request response',
    description = 'Python library handle incoming HTTP requests.',

    long_description = long_description,
)
