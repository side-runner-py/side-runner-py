import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='side_runner_py',
    version='0.0.5',
    author='',
    author_email='',
    maintainer='',
    maintainer_email='ya_amai@yahoo.co.jp',
    license='MIT',
    url='',
    description='Run selenium SIDE file',
    long_description=read('README.md'),
    packages=['side_runner_py'],
    install_requires=[
        'selenium',
        'jinja2',
        'emoji',
        'stingconf==0.0.3',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'side-runner-py = side_runner_py.main:main'
        ]
    },
)
