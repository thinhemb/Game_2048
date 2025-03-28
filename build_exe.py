import PyInstaller.__main__
import PyInstaller.config
import os

distpath ="--distpath=" + os.path.join(str(os.getcwd()) ,"builder")
workpath = "--workpath=" + os.path.join(str(os.getcwd()),  "builder/tempo")
# PyInstaller.config.CONF['distpath'] = path
PyInstaller.__main__.run([
    'main.py',
    # '--onedir',
    '--onefile',
    '-nGame_2048',
    # '--hidden-import=pya2l.cgen',
    '--windowed',
    #'--disable-windowed-traceback'
    distpath,
    workpath,
    '--clean',
    '-y'
])
