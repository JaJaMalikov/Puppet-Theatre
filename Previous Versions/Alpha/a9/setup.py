from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'aom')
]

setup(name='Avatars of Morpheus',
      version = '1.0',
      description = 'Save the world, no matter how much it changes',
      options = dict(build_exe = buildOptions),
      executables = executables)
