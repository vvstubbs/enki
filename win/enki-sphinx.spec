# .. -*- mode: python -*-
#
# ****************
# enki-sphinx.spec
# ****************
# This file instructs Pyinstaller to build a binary containing both Enki
# and Sphinx executables.
#
# Procedure to create this file:
#
# #. Run ``win\build_exe.bat`` and test. This creates working
#    ``enki.spec`` and ``sphinx-build.spec`` files.
# #. Combine these files according to the `Pyinstaller merge docs
#    <http://htmlpreview.github.io/?https://github.com/pyinstaller/pyinstaller/blob/develop/doc/Manual.html#multipackage-bundles>`_.
#    These steps are illustrated in the comments below.
# #. Run ``win\build_exe.bat`` again; the third build is the combined version.

# Use the ``.exe`` extension for Windows, but not Unix.
import sys
if sys.platform.startswith('linux'):
    ext = ''
else:
    ext = '.exe'

block_cipher = None

# Per the `Pyinstaller merge docs`_, first create uniquely-named analysis
# objects for both programs.
enki_a = Analysis(['bin/enki'],
             # I don't particularly like an absolute path. Can it be made
             # relative? The autogenerated .spec files have an absolute path.
             pathex=['.'],
             hiddenimports=[],
             hookspath=['win'],
             runtime_hooks=['win/rthook_pyqt4.py'],
             # Per  Hartmut on 24-Sep-2014 on the Pyinstaller e-mail list:
             # "An optional list of module or package names (their Python names,
             # not path names) that will be ignored (as though they were not
             # found)."
             excludes=['_tkinter'],
             cipher=block_cipher)
sphinx_a = Analysis(['win/sphinx-build.py'],
             pathex=['.'],
             hiddenimports=['CodeChat'],
             hookspath=['win'],
             runtime_hooks=[],
             excludes=['_tkinter'],
             cipher=block_cipher)

import pylint
import os.path

           # Find the location of pylint's __init__.py file. Note that
           # ``pylint.__file__`` returns a .pyc file, which breaks PyInstaller.
           # So, replace the extension with a ``.py`` instead.
pylint_a = Analysis([os.path.splitext(pylint.__file__)[0] + '.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=['_tkinter'],
             cipher=block_cipher)
# Next, eliminate duplicate libraries and modules. Listing Enki first seems to
# place all libraries and modules there.
MERGE(
    (enki_a, 'enki', 'enki'),
    (sphinx_a, 'sphinx', 'sphinx'),
    (pylint_a, 'pylint', 'pylint'),
    )

# Finally, produce both binaries. Note that the resulting Sphinx binary doesn't
# work as is, since it has no libraries bundled with it. Instead, it needs to
# be copied to the Enki directory before being executed.
enki_pyz = PYZ(enki_a.pure,
             cipher=block_cipher)
enki_exe = EXE(enki_pyz,
          enki_a.scripts,
          exclude_binaries=True,
          name='enki-editor' + ext,
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icons/logo/enki.ico')
enki_coll = COLLECT(enki_exe,
               enki_a.binaries,
               enki_a.zipfiles,
               enki_a.datas,
               strip=None,
               upx=True,
               name='enki')

sphinx_pyz = PYZ(sphinx_a.pure,
             cipher=block_cipher)
sphinx_exe = EXE(sphinx_pyz,
          sphinx_a.scripts,
          exclude_binaries=True,
          name='sphinx-build' + ext,
          debug=False,
          strip=None,
          upx=True,
          console=True )
sphinx_coll = COLLECT(sphinx_exe,
               sphinx_a.binaries,
               sphinx_a.zipfiles,
               sphinx_a.datas,
               strip=None,
               upx=True,
                name='sphinx-build')

pylint_pyz = PYZ(pylint_a.pure,
             cipher=block_cipher)
pylint_exe = EXE(pylint_pyz,
          pylint_a.scripts,
          exclude_binaries=True,
          name='pylint' + ext,
          debug=False,
          strip=None,
          upx=True,
          console=True )
pylint_coll = COLLECT(pylint_exe,
               pylint_a.binaries,
               pylint_a.zipfiles,
               pylint_a.datas,
               strip=None,
               upx=True,
               name='pylint')
