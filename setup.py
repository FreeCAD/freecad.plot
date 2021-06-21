from setuptools import setup
import os
import subprocess as sub

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "plot", "version.py")
with open(version_path) as fp:
    exec(fp.read())
    
# try to create a resource file
# assume either pyside2-rcc or pyside-rcc are available.
# if both are available pyside2-rcc is used.
rc_input = os.path.abspath(os.path.join("freecad", "plot", "resources", "Plot.qrc"))
rc_output = os.path.join("freecad", "plot", "Plot_rc.py")
try:
    try:
        proc = sub.Popen(["pyside2-rcc", "-o", rc_output, rc_input], stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = proc.communicate()
    except FileNotFoundError:
        proc = sub.Popen(["pyside-rcc", "-o", rc_output, rc_input], stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = proc.communicate()
except Exception as e:
    print("An error occured while trying to create the resource file: \n" + str(e))

print(out.decode("utf8"))
print(err.decode("utf8"))

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
