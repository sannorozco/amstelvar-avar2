# menuTitle: build glyphs in sources

from importlib import reload
import hTools3.modules.accents
reload(hTools3.modules.accents)

import os, glob
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from hTools3.modules.accents import buildAccentedGlyphs

familyName    = 'AmstelvarA2'
subFamilyName = 'Roman'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
glyphConstructionPath = os.path.join(baseFolder, 'Sources', 'AmstelvarA2.glyphConstruction')

glyphNames = [
    'ghestroke'
]

targetStyles = [
    # 'XOPQ4',
    # 'XOPQ310',
    # 'XSHF0',
    # 'XSHF179',
    # 'XSHL0',
    # 'XSHL124',
    # 'XSHU0',
    # 'XSHU154',
    # 'XSVF0',
    # 'XSVF131',
    # 'XSVL0',
    # 'XSVL98',
    # 'XSVU0',
    # 'XSVU130',
    # 'XTRA208',
    # 'XTRA508',
    # 'XTSP-100',
    # 'XTSP100',
    # 'XTTW0',
    # 'XTTW30',
    # 'YOPQ4',
    # 'YOPQ311',
    # 'YSHF0',
    # 'YSHF147',
    # 'YSHL0',
    # 'YSHL140',
    # 'YSHU0',
    # 'YSHU150',
    'YSVF84',
    'YSVF251',
    'YSVL146',
    'YSVL251',
    'YSVU0',
    'YSVU165',
    'YTAS665',
    'YTAS875',
    'YTDE-100',
    'YTDE-310',
    'YTFI281',
    'YTFI896',
    'YTLC436',
    'YTLC594',
    'YTOS0',
    'YTOS25',
    'YTTL0',
    'YTTL104',
    'YTUC541',
    'YTUC875',
]

# get glyph constructions
with open(glyphConstructionPath, 'r') as f:
    glyphConstructions = f.read()

for styleName in targetStyles:
    dstPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{styleName}.ufo')
    if not os.path.exists(dstPath):
        print(f'target font {dstPath} does not exist.\n')
    dstFont = OpenFont(dstPath, showInterface=False)

    print(f'building glyphs in {dstPath}...')
    buildAccentedGlyphs(dstFont, glyphNames, glyphConstructions, clear=True, verbose=True, autoUnicodes=False, indentLevel=1)

    print(f'\tsaving font...')
    dstFont.save()
    # dstFont.close()
    print()

