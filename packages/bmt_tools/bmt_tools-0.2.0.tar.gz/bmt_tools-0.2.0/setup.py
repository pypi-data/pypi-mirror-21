from setuptools import setup

setup(name='bmt_tools',
      version='0.2.0',
      description='Tools for Bad Movie Twins',
      url='http://github.com/patsmad/BMT/bmt_tools',
      author='Patrick Smadbeck',
      author_email='patrick@smadbeck.com',
      license='',
      packages=['bmt_tools'],
      include_package_data = True,
      install_requires=['requests','beautifulsoup4','numpy'],
      zip_safe=False)
