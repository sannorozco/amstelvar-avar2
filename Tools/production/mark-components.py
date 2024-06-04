# menuTitle: mark different types of glyphs

from variableValues.validation import *

def getNestingLevels(g, levels=0):
    if g.components:
        levels += 1
        for c in g.components:
            if c.baseGlyph not in f:
                print(f'ERROR in "{g.name}": glyph {c.baseGlyph} not in font')
                continue
            baseGlyph = f[c.baseGlyph]
            levels = getNestingLevels(baseGlyph, levels)
    return levels

alpha = 0.35

colorComponents = 1, 0.65, 0, alpha
colorDefault    = 0, 0.65, 1, alpha
colorWarning    = 1, 0, 0, alpha

f = CurrentFont()

sourcesFolder = os.path.split(f.path)[0]
defaultPath = os.path.join(sourcesFolder, f'AmstelvarA2-Italic_wght400.ufo')

assert os.path.exists(defaultPath)

defaultFont = OpenFont(defaultPath, showInterface=False)

for g in f:
    g.markColor = None

    if g.name not in defaultFont:
        continue

    defaultGlyph = defaultFont[g.name]

    results = validateGlyph(defaultGlyph, g)

    if g.components:
        levels = getNestingLevels(g)
        if levels > 1 or len(g.contours):
            g.markColor = colorWarning
        else:
            g.markColor = colorComponents
    else:
        if results['points'] and results['pointPositions']:
            if f.path != defaultFont.path:
                g.markColor = colorDefault
            else:
                g.markColor = None

f.changed()

