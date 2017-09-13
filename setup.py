from description import __version__, __author__
from setuptools import setup, find_packages

setup(
   name="customized_KoNLPy",
   version=__version__,
   author=__author__,
   author_email='soy.lovit@gmail.com',
   url='https://github.com/lovit/customized_konlpy',
   description="KoNLPy customization version (wrapping package)",
   long_description="""Add customized words and tags and pos tagging with templates   
   """,
   install_requires=["Jpype1>=0.6.1", "konlpy>=0.4.4"],
   keywords = ['KoNLPy wrapping customization'],
   packages=find_packages(),
   package_data={'ckonlpy':['data/*/*.txt', 'data/*/*/*.txt']}
)