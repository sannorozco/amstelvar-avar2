# menuTitle: build glyphs from glyph constructions in sources

from importlib import reload
import xTools4.modules.accents
reload(xTools4.modules.accents)

import os, glob
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from xTools4.modules.accents import buildAccentedGlyphs

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
glyphConstructionPath = os.path.join(baseFolder, 'Sources', subFamilyName, f'{familyName}-{subFamilyName}.glyphConstruction')

glyphNames = [
    'DZcaron', 'Dzcaron', 'Lj', 'Nj',
    'dzcaron', 'lj', 'nj',
    'IJ', 'IJacute', 'Iacute_J.loclNLD',
    'ij', 'ijacute', 'iacute_j.loclNLD'
]
dstFonts   = []

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

# get glyph constructions
with open(glyphConstructionPath, 'r') as f:
    glyphConstructions = f.read()

verbose = True

for ufoPath in ufoPaths:
    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:
        dstFont = OpenFont(ufoPath, showInterface=False)
        print(f'building glyphs in {os.path.split(ufoPath)[-1]}...')
        buildAccentedGlyphs(dstFont, glyphNames, glyphConstructions, clear=True, verbose=verbose, autoUnicodes=False, indentLevel=1)
        print(f'\tsaving font...')
        dstFont.save()
        # dstFont.close()
        print()
