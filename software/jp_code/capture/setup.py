#setup.py
from cx_Freeze import setup, Executable
setup(
    name = "ProDIS",
    version = "1.0.0",
    description = "ProDIS",
    author="Joao Paulo Andrade",
    options = {"build_exe": {
        'packages': ["sys","serial","time","threading","pyqtgraph","numpy"],
        'include_msvcr': True,
    }},
    executables = [Executable("ProDIS_Freeze.py",base="Win32GUI",icon="Cut.ico")]
    )