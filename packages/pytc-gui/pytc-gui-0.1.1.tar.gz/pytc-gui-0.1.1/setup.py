#!/usr/bin/env python3

import sys

if sys.version_info[0] < 3:
    sys.exit('Sorry, Python < 3.x is not supported')

# Try using setuptools first, if it's installed
from setuptools import setup, find_packages

# Need to add all dependencies to setup as we go!
setup(name='pytc-gui',
      packages=find_packages(exclude=['pytc']),
      version='0.1.1',
      description="PyQt5 GUI for pytc API",
      author='Hiranmayi Duvvuri',
      author_email='hiranmayid8@gmail.com',
      url='https://github.com/harmslab/pytc-gui',
      download_url='https://github.com/harmslab/pytc-gui/tarball/0.1.0',
      zip_safe=False,
      install_requires=["pytc-fitter","seaborn","pyqt5"],
      classifiers=['Programming Language :: Python'],
      scripts=['scripts/pytc-gui'])

