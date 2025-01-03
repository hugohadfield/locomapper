
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'locomapper/version.py')).read())

setup(
    name='locomapper',
     # Read from VERSION file
    version=__version__,
    description="Locomapper is a Python package for localising based on landmark data",
    author='Hugo Hadfield',
    author_email='hadfield.hugo@gmail.com',
    url='https://github.com/hugohadfield/locomapper',
    packages=find_packages(),
    install_requires=[
        'pydantic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)