import os
import subprocess as sub


PYSIDE_MAX_VERSION = 10
RCC_NAMES = ["pyside{}-rcc".format(i) for i in range(2, PYSIDE_MAX_VERSION + 1)]
RCC_NAMES.append("pyside-rcc")


def compile_resources():
    # try to create a resource file
    # assume either pyside2-rcc or pyside-rcc are available.
    # if both are available pyside2-rcc is used.
    rc_input = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "Plot.qrc"))
    rc_output = os.path.join(os.path.dirname(__file__), "Plot_rc.py")
    for rcc in RCC_NAMES:
        try:
            proc = sub.Popen([rcc, "-o", rc_output, rc_input], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
            out, err = proc.communicate()
        except FileNotFoundError:
            continue
        except Exception as e:
            print("An error occured while trying to create the resource file: \n" + str(e))
        print(out)
        print(err)
        break


if __name__ == '__main__':
    compile_resources()
