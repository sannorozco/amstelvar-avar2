# menuTitle: remove glyphs from all sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
ufoPaths      = glob.glob(f'{sourcesFolder}/*.ufo')

glyphNames = 'acutecombstack acutecombstack.case brevecombstack.case circumflexcombstack circumflexcombstack.case dieresiscombstack dieresiscombstack.case dotaccentcombstack dotaccentcombstack.case gravecombstack.case macroncombstack macroncombstack.case tildecombstack tildecombstack.case'.split()
dstFonts   = [
# 'XOPQ', 'WDSP1000', 
]

preflight = False

for ufoPath in ufoPaths:
    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        f = OpenFont(ufoPath, showInterface=False)
        print(f'removing glyphs in {ufoPath}...')
        for glyphName in glyphNames:
            if glyphName not in f:
                continue
            print(f'\tremoving {glyphName}...')
            if not preflight:
                del f[glyphName]
        f.save()
        f.close()
        print()
