# coding: utf-8
import setuptools


def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()


setuptools.setup(
    name='fixedwidthwriter',
    packages=['fixedwidthwriter'],  # this must be the same as the name above
    version='1.0.1',
    description='A class to write fixed-width files with an interface similar to python`s csv writer',
    author='Arthur Bressan',
    author_email='arthurpbressan@gmail.com',
    url='https://github.com/ArthurPBressan/py-fixedwidthwriter',  # use the URL to the github repo
    download_url='https://github.com/ArthurPBressan/py-fixedwidthwriter/tarball/1.0.1',
    keywords=['file writer', 'fixed width'],  # arbitrary keywords
    classifiers=[],
    install_requires=parse_requirements('requirements.txt')
)
# thanks to Peter Downs for posting his upload guide to PyPI at http://peterdowns.com/posts/first-time-with-pypi.html
