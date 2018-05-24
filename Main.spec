# -*- mode: python -*-

block_cipher = None


a = Analysis(['Main.py'],
             pathex=['BR_switch'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('switch-icon.svg', 'switch-icon.svg', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='BR Switching Tool',
          debug=False,
          strip=False,
          upx=True,
          console=True, 
		  icon='switch-icon.ico')
