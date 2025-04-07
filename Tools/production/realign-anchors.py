# menuTitle: horizontally align anchors based on the default

import os
from xTools4.modules.fontutils import getGlyphs2

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
defaultName   = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultPath   = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')

anchorNames = [
    'top',
    # 'GRKtop',
    # 'center',
    'bottom',
]

defaultFont = OpenFont(defaultPath, showInterface=False)

f = CurrentFont()

glyphNames = getGlyphs2(f)

for glyphName in glyphNames:
    defaultGlyph = defaultFont[glyphName]
    glyph = f[glyphName]
    print(f'realigning anchors in {glyphName}...')
    glyph.prepareUndo('realigning anchors')
    for i, a in enumerate(glyph.anchors):
        if a.name not in anchorNames:
            continue
        xPos = defaultGlyph.width / defaultGlyph.anchors[i].x
        xNew = glyph.width / xPos
        print(f'\t{a.name}: {a.x} -> {int(xNew)}')
        a.x = xNew
    glyph.performUndo()
    print()
    