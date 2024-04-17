# menuTitle: copy default glyphs to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

preflight = False

glyphNames = 'Che ghe.bgr ghe ze Ecyr Y Yacute eng napostrophe Ycircumflex Ygrave Ydotbelow Ytilde engtail Upsilon Upsilontonos Upsilondieresis alpha Ka'.split()

sourceFont = OpenFont(sourcePath, showInterface=False)

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    dstFont = OpenFont(ufoPath, showInterface=False)

    print(f'copying glyphs to {ufoPath}...')
    for glyphName in glyphNames:
        print(f'\tcopying {glyphName}...')
        if not preflight:
            dstFont.insertGlyph(sourceFont[glyphName], name=glyphName)

    if not preflight:
        print(f'\tsaving font...')
        dstFont.save()

    dstFont.close()
    print()
