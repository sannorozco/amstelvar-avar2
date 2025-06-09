# menuTitle: fix buggy GDEF table in generated fonts

import os, glob
from mojo.smartSet import readSmartSets
from fontTools.ttLib import TTFont
from xml.etree.ElementTree import parse

subfamilyName = ['Roman', 'Italic'][0]
defaultName   = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources')
fontsFolder   = os.path.join(baseFolder, 'Fonts')
smartSetsPath = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}.roboFontSets')
defaultPath   = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}_{defaultName}.ufo')
ttfPath       = os.path.join(fontsFolder, f'AmstelvarA2-{subfamilyName}_avar2.ttf')
ttxPath       = os.path.join(fontsFolder, f'AmstelvarA2-{subfamilyName}_avar2.ttx')

assert os.path.exists(smartSetsPath)

def getCombingingAccents(smartSetsPath):
    smartSets = readSmartSets(smartSetsPath, useAsDefault=False, font=None)
    combiningAccents = []
    for smartGroup in smartSets:
        if not smartGroup.groups:
            continue
        for smartSet in smartGroup.groups:
            if 'accents comb' in smartSet.name:
                combiningAccents += smartSet.glyphNames
    return set(combiningAccents)

def findGlyphsWithUnderscoreAnchors(font):
    underscoreGlyphs = []
    for g in font:
        for a in g.anchors:
            if a.name.startswith('_'):
                underscoreGlyphs.append(g.name)
    return set(underscoreGlyphs)

def ttx2ttf(ttxPath):
    ttfPath = ttxPath.replace('.ttx', '.ttf')
    if os.path.exists(ttfPath):
        os.remove(ttfPath)
    tt = TTFont()
    tt.verbose = False
    tt.importXML(ttxPath)
    tt.save(ttfPath)
    tt.close()

def ttf2ttx(ttfPath):
    ttxPath = ttfPath.replace('.ttf', '.ttx')
    if os.path.exists(ttxPath):
        os.remove(ttxPath)
    tt = TTFont(ttfPath)
    tt.verbose = False
    tt.saveXML(ttxPath)
    tt.close()



defaultFont = OpenFont(defaultPath, showInterface=False)

# 1. get a list of all combining accents
combiningAccents = getCombingingAccents(smartSetsPath)

# 2. get a list of all glyphs with anchors starting with underscore
underscoreGlyphs = findGlyphsWithUnderscoreAnchors(defaultFont)

# subtract (1) from (2) to get a list of glyphs to fix
glyphsToFix = list(underscoreGlyphs.difference(combiningAccents))

# convert ttf font to ttx
assert os.path.exists(ttfPath)
ttf2ttx(ttfPath)

# fix wrong GDEF class for glyphs in list
assert os.path.exists(ttxPath)
tree = parse(ttxPath)
root = tree.getroot()
for child in root.find('GDEF'):
    if child.tag == 'GlyphClassDef':
        for g in child.iter('ClassDef'):
            glyphName = g.get('glyph')
            if glyphName in glyphsToFix:
                # change GDEF class from 3 to 1       
                g.set('class', '1')
tree.write(ttxPath)

# convert ttx back to ttf fonts
ttx2ttf(ttxPath)

# delete ttx file
os.remove(ttxPath)
