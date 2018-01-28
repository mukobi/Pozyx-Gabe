from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

additional_mods = ['numpy.core._methods', 'numpy.lib.format']

options = {
    'build_exe': {

        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        'includes': additional_mods
    }
}

setup(
    name="PSUPozyx",
    version="0.1.2",
    description="A script used for the PSU Pozyx system",
    options=options,
    executables=[Executable("1D_ranging.py"), Executable("3D_positioning.py"), Executable("motion_data.py")]
)
