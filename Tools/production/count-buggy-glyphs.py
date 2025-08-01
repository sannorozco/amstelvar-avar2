# menuTitle: count all glyphs affected by fontmake's auto mark feature bug 
# for more info see http://github.com/googlefonts/fontmake/issues/1148

import os, glob
from fontTools.ttLib import TTFont
from xml.etree.ElementTree import parse
from mojo.smartSet import readSmartSets
from glyphConstruction import *

subfamilyName    = ['Roman', 'Italic'][0]
defaultName      = 'wght400'
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources')
fontsFolder      = os.path.join(baseFolder, 'Fonts')
smartSetsPath    = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}.roboFontSets')
defaultPath      = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}_{defaultName}.ufo')
ttfPath          = os.path.join(fontsFolder, f'AmstelvarA2-{subfamilyName}_avar2.ttf')
ttxPath          = os.path.join(fontsFolder, f'AmstelvarA2-{subfamilyName}_avar2.ttx')
constructionPath = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}.glyphConstruction')

baseAnchors = []

marks = [ '_top', '_topright', '_bottom', '_centerright', '_ogonek', '_GRKtop', '_GRKtopleft', '_tonos', ]

f = OpenFont(defaultPath, showInterface=False)

for g in f:
    for a in g.anchors:
        if not a.name.startswith('_'):
            continue
        if a.name not in baseAnchors and a.name not in marks:
            baseAnchors.append(a.name)

print(f'anchor pairs ({len(baseAnchors)}) which are used in glyph constructions, but should *not* be used when building the mark feature:')
for a in baseAnchors:
    print(f'- {a[1:]}, {a}')
print()

# glyphsWithBaseAnchors      = []
# glyphsWithComponentAnchors = []

# for g in f:
#     for a in g.anchors:
#         if a.name in baseAnchors:
#             if g.name not in glyphsWithComponentAnchors:
#                 glyphsWithComponentAnchors.append(g.name)
#         if f'_{a.name}' in baseAnchors:
#             if g.name not in glyphsWithBaseAnchors:
#                 glyphsWithBaseAnchors.append(g.name)   

# print(glyphsWithBaseAnchors)
# print()
# print(glyphsWithComponentAnchors)

# get constructions
with open(constructionPath, 'r') as f:
    glyphConstructions = f.read()

constructions = ParseGlyphConstructionListFromString(glyphConstructions)
constructions = [c for c in constructions if len(c)]

buggyGlyphs = []

for c in constructions:
    for a in baseAnchors:
        if a[1:] in c:
            buggyGlyphs.append(c.split('=')[0].strip())

print(f"glyphs ({len(buggyGlyphs)}) which would have to be decomposed to avoid fontmake's mark feature bug:")
for g in buggyGlyphs:
    print(f'- {g}')
print()
