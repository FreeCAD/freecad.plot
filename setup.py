# SPDX-License-Identifier: LGPL-2.1-or-later

from setuptools import setup
import os
from freecad.plot.compile_resources import compile_resources

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "plot", "version.py")
with open(version_path) as fp:
    exec(fp.read())
    
compile_resources()

setup(name='freecad.plot',
      version=str(__version__),
      packages=['freecad',
                'freecad.plot',
                'freecad.plot.plotAxes',
                'freecad.plot.plotLabels',
                'freecad.plot.plotPositions',
                'freecad.plot.plotSave',
                'freecad.plot.plotSeries'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/FreeCAD/plot",
      description="externalized plot workbench. Created by Jose Luis Cercos Pita",
      install_requires=['numpy', 'matplotlib'], # should be satisfied by FreeCAD's system dependencies already
      include_package_data=True)
