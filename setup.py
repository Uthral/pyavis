import os, codecs
from setuptools import setup, find_packages

project_root = os.path.dirname(os.path.abspath(__file__))

version = '0.1.0'

with open(os.path.join(project_root, 'requirements.txt')) as file:
    install_requires = file.read().splitlines()

with codecs.open(os.path.join(project_root, 'README.md'), 'r', 'utf-8') as file:
    long_description = ''.join(file.readlines())

extras_require = {
    "qt" : ["PyQt5"],
    "ipywidgets" : ["ipywidgets", "ipympl"],
    "full" : ["PyQt5","ipywidgets", "ipympl"]
}


setup(
    name='pyavis',
    version='0.1.0',
    description='Visualization of audio data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    extras_require=extras_require,
    author='Robin Külker',
    author_email='rkuelker@techfak.uni-bielefeld.de',
    keywords=[''],
    # url='https://github.com/',
    classifiers=[]
)