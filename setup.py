from setuptools import setup
import os
import subprocess as sub

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "plot", "version.py")
with open(version_path) as fp:
    exec(fp.read())
    
# try to create a resource file
proc = sub.Popen(["pyside-rcc", "-o", "Ship_rc.py", "resources/Ship.qrc"], stdout=sub.PIPE, stderr=sub.PIPE)
out, err = proc.communicate()
print(out.decode("utf8"))
print(err.decode("utf8"))

setup(name='freecad.plot',
      version=str(__version__),
      packages=['freecad',
                'freecad.plot.plotAxes',
                'freecad.plot.plotLabels',
                'freecad.plot.plotPositions',
                'freecad.plot.plotSave',
                'freecad.plot.plotUtils'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/FreeCAD/ship",
      description="externalized plot workbench. Created by Jose Luis Cercos Pita",
      install_requires=['numpy', 'matplotlib'], # should be satisfied by FreeCAD's system dependencies already
      include_package_data=True)
