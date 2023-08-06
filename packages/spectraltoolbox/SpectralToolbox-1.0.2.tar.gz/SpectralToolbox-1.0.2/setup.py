#!/usr/bin/env python

#
# This file is part of SpectralToolbox.
#
# SpectralToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpectralToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with SpectralToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2012-2015 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Copyright (C) 2015-2016 Massachusetts Institute of Technology
# Uncertainty Quantification group
# Department of Aeronautics and Astronautics
#
# Author: Daniele Bigoni
#

import os.path
import re
import pip
from pip.req import parse_requirements
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.install import install
from setuptools.command.develop import develop

global zip_safe
zip_safe = False # needed for xml linking

global include_dirs
include_dirs = []

#####################
# DEPENDENCIES
# (mod_name, use_wheel)
deps_list = [('numpy', True),
             ('orthpol_light', False),
             ('scipy', True)]

opt_deps_list = {'ORTHPOL': [False, [('orthpol', False)] ] }

def install_list(pkg_list):
    for (pname, use_wheel) in pkg_list:
        print("[DEPENDENCY] Installing %s" % pname)
        try:
            if use_wheel:
                pip_flag = pip.main(['install', '--upgrade', pname])
            else:
                pip_flag = pip.main(['install', '--no-binary', ':all:',
                                     '--upgrade', pname])
        except Exception as e:
            print("[ERROR] Unable to install %s using pip. " % pname + \
                  "Please read the instructions for " + \
                  "manual installation.. Exiting" )
            exit(2)
        if pip_flag != 0:
            fail_list.append(pname)

def deps_install():
    # Upgrade pip
    install_list([('pip', True)])
    # Install dependencies
    install_list(deps_list)
    # Install optional dependencies
    for opt in opt_deps_list:
        if opt_deps_list[opt][0]:
            install_list(opt_deps_list[opt][1])
            
class SpectralToolbox_install(install):
    def run(self):
        deps_install()
        import numpy as np
        include_dirs.append(np.get_include())
        install.run(self)

class SpectralToolbox_develop(develop):
    def run(self):
        deps_install()
        import numpy as np
        include_dirs.append(np.get_include())
        develop.run(self)

local_path = os.path.split(os.path.realpath(__file__))[0]
version_file = os.path.join(local_path, 'SpectralToolbox/_version.py')
version_strline = open(version_file).read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_strline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (version_file,))

# Check for optional packages in environment variables
for opt in opt_deps_list:
    val = os.getenv(opt)
    if val is not None:
        if val in ['False','false']:
            opt_deps_list[opt][0] = False
        elif val in ['True', 'true']:
            opt_deps_list[opt][0] = True
    
setup(name = "SpectralToolbox",
      version = version,
      packages=find_packages(),
      include_package_data=True,
      scripts=[],
      url="http://www2.compute.dtu.dk/~dabi/",
      author = "Daniele Bigoni",
      author_email = "dabi@dtu.dk",
      license="COPYING.LESSER",
      description="Tools for building spectral methods",
      long_description=open("README.rst").read(),
      cmdclass={'install': SpectralToolbox_install,
                'develop': SpectralToolbox_develop},
      ext_modules = [ Extension('polymod',
                                ['src/tools.cpp'],
                                extra_compile_args = ['-O3'],
                                extra_link_args = ['-O3']) ],
      include_dirs=include_dirs,
      zip_safe = zip_safe          # Set to False for xml linking
      )
