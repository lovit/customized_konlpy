import ckonlpy
import setuptools
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="customized-konlpy",
    version=ckonlpy.__version__,
    author=ckonlpy.__author__,
    author_email='soy.lovit@gmail.com',
    description="KoNLPy wrapping package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lovit/customized_konlpy',
    packages=setuptools.find_packages(),
    package_data={'ckonlpy':['data/*/*.txt', 'data/*/*/*.txt']},
    install_requires=["Jpype1>=0.6.1", "konlpy>=0.4.4"],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)