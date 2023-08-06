import os
from setuptools import setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='Constellation-Base',
    version='0.1.4',
    packages=['constellation_base'],
    include_package_data=True,
    license='ISC License',
    description='Base components of the Constellation Suite',
    long_description=README,
    url='https://github.com/ConstellationApps/',
    author='Constellation Developers',
    author_email='bugs@constellationapps.org',
    install_requires=[
        'django',
        'Pillow',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Development Status :: 4 - Beta'
    ]
)
