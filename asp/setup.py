#!/usr/bin/env python

# Based on codepy's setup.py (see http://mathema.tician.de/software/codepy)

import distribute_setup
import asp
distribute_setup.use_setuptools()

from setuptools import setup
import glob

setup(name="asp",
      version=asp.__version__,
      description="ASP is a SEJITS (specialized embedded just-in-time compiler) toolkit for Python.",
      long_description="""
      See http://www.armandofox.com/geek/home/sejits/ for more about SEJITS, including links to
      publications. See http://aspsejits.pbworks.com/w/page/31670594/FrontPage for more about ASP.
      """,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        ],

      author=u"Shoaib Kamil, Henry Cook, and others",
      url="http://aspsejits.pbworks.com/w/page/31670594/FrontPage",
      author_email="skamil@cs.berkeley.edu",
      license = "BSD",

      packages=["asp", "asp.codegen", "asp.codegen.templating", "asp.jit"],
#      install_requires=[
#          "pytools>=8",
#          ],
#      data_files=[("include/codepy", glob.glob("include/codepy/*.hpp"))],
     )
