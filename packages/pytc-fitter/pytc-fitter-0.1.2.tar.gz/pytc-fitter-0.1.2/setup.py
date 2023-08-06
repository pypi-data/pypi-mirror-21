import sys

if sys.version_info[0] < 3:
    sys.exit('Sorry, Python < 3.x is not supported')

# Try using setuptools first, if it's installed
from setuptools import setup, find_packages

# Need to add all dependencies to setup as we go!
setup(name='pytc-fitter',
      packages=find_packages(),
      version='0.1.2',
      description="Python software package for analyzing Isothermal Titration Calorimetry data",
      author='Michael J. Harms',
      author_email='harmsm@gmail.com',
      url='https://github.com/harmslab/pytc',
      download_url='https://github.com/harmslab/pytc/tarball/0.1.2',
      zip_safe=False,
      install_requires=["matplotlib","scipy","numpy","pandas"],
      classifiers=['Programming Language :: Python'])

