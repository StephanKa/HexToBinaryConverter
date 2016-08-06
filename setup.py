import sys
from py2exe.build_exe import py2exe
from distutils.core import setup

data_files = []
setup( windows=[{"script":"HexBinConverter.py", "icon_resources": [(1, "hexbin.ico")], "dest_base":"HexBinConverter"}], options={"py2exe":{"includes":["sip"], 'bundle_files': 1, "optimize":2, "compressed": 1}}, data_files=data_files, version="1.0.0.0", name="HexBinConverter", description="Hex to Bin Converter")