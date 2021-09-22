"""A Python kernel backed by Pyodide"""

import sys
from collections import namedtuple

# 0. do early mocks that change `sys.modules`
from . import mocks

mocks.apply_mocks()
del mocks

# 1. do expensive patches that require imports
from . import patches

patches.apply_patches()
del patches

# 2. set up the rest of the IPython-like environment
from .display import LiteStream
from .interpreter import LitePythonShellApp

VersionInfo = namedtuple(
    "VersionInfo", ["major", "minor", "micro", "releaselevel", "serial"]
)

# DO NOT EDIT THIS DIRECTLY!  It is managed by bumpversion
version_info = VersionInfo(0, 1, 0, "alpha", 8)

_specifier_ = {"alpha": "a", "beta": "b", "candidate": "rc", "final": ""}

__version__ = "{}.{}.{}{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    (
        ""
        if version_info.releaselevel == "final"
        else _specifier_[version_info.releaselevel] + str(version_info.serial)
    ),
)

stdout_stream = LiteStream("stdout")
stderr_stream = LiteStream("stderr")

ipython_shell_app = LitePythonShellApp()
ipython_shell_app.initialize()
ipython_shell = ipython_shell_app.shell
kernel_instance = ipython_shell.kernel

# 3. handle streams
sys.stdout = stdout_stream
sys.stderr = stderr_stream
