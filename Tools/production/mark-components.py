# menuTitle: mark different types of glyphs

from importlib import reload
import variableValues.validation
reload(variableValues.validation)

from variableValues.validation import *
from variableValues.decomposePointPen import DecomposePointPen

alpha = 0.35

colorComponents      = 1, 0.3, 0, alpha
colorComponentsEqual = 1, 0.65, 0, alpha
colorDefault         = 0, 0.65, 1, alpha
colorWarning         = 1, 0, 0, 0.65

selectedGlyphs = False

currentFont = CurrentFont()

sourcesFolder = os.path.split(currentFont.path)[0]
defaultPath = os.path.join(sourcesFolder, f'AmstelvarA2-Italic_wght400.ufo')

assert os.path.exists(defaultPath)

defaultFont = OpenFont(defaultPath, showInterface=False)

glyphNames = currentFont.selectedGlyphNames
if not glyphNames or not selectedGlyphs:
    glyphNames = currentFont.glyphOrder

for glyphName in glyphNames:
    currentGlyph = currentFont[glyphName]
    currentGlyph.markColor = None

    if glyphName not in defaultFont:
        continue

    # decompose glyphs with components
    if currentGlyph.components:
        currentGlyph_flat = RGlyph()
        pointPen = currentGlyph_flat.getPointPen()
        decomposePen = DecomposePointPen(currentFont, pointPen)
        currentGlyph.drawPoints(decomposePen)
        currentGlyph_flat.name    = currentGlyph.name
        currentGlyph_flat.unicode = currentGlyph.unicode
        currentGlyph_flat.width   = currentGlyph.width
    else:
        currentGlyph_flat = currentGlyph

    defaultGlyph = defaultFont[glyphName]

    # decompose default glyph with components
    if defaultGlyph.components:
        defaultGlyph_flat = RGlyph()
        pointPen = defaultGlyph_flat.getPointPen()
        decomposePen = DecomposePointPen(defaultFont, pointPen)
        defaultGlyph.drawPoints(decomposePen)
        defaultGlyph_flat.name    = defaultGlyph.name
        defaultGlyph_flat.unicode = defaultGlyph.unicode
        defaultGlyph_flat.width   = defaultGlyph.width
    else:
        defaultGlyph_flat = defaultGlyph

    results = validateGlyph(defaultGlyph, currentGlyph)
    results_flat = validateGlyph(defaultGlyph_flat, currentGlyph_flat)

    if currentGlyph.components:
        levels = getNestingLevels(currentGlyph)
        if levels > 1 or len(currentGlyph.contours):
            currentGlyph.markColor = colorWarning
        else:
            if all(results_flat.values()):
                currentGlyph.markColor = colorComponentsEqual
            else:
                currentGlyph.markColor = colorComponents
    else:
        if results['points'] and results['pointPositions']:
            if currentFont.path != defaultFont.path:
                currentGlyph.markColor = colorDefault
            else:
                currentGlyph.markColor = None

currentFont.changed()

