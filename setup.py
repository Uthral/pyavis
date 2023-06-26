from setuptools import setup, find_packages

setup(
    name='pyavis',
    version='0.0.1',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # license='MIT',
    packages=find_packages(exclude=["tests"]),
    install_requires=open('requirements.txt').read().splitlines(),
    # extras_require=REQUIRED_EXTRAS,
    # tests_require=REQUIRED_TEST,
    author='Robin Külker',
    author_email='rkuelker@techfak.uni-bielefeld.de',
    keywords=[''],
    # url='https://github.com/',
    classifiers=[]
)