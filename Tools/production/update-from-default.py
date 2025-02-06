# menuTitle: update default glyphs in all sources

from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

import os, glob
from xTools4.modules.validation import assignValidationGroup

# --------
# settings
# --------

familyName     = 'AmstelvarA2'
subFamilyName  = ['Roman', 'Italic'][1]
glyphNames     = ['caroncomb-alt.case',]
newDefaultName = 'wght400'
oldDefaultName = 'BARS0'
preflight      = False

# ---------
# functions
# ---------

def updateGlyphsFromDefault(font, oldDefault, newDefault, glyphNames):
    name = os.path.splitext(os.path.split(font.path)[-1])[0].split('_')[-1]
    print(familyName, subFamilyName, name)
    fontChanged = False
    for glyphName in glyphNames:
        if glyphName not in oldDefault or glyphName not in font or glyphName not in newDefault:
            continue
        g1 = oldDefault[glyphName]
        g2 = font[glyphName]
        g3 = newDefault[glyphName]
        validationGroup = assignValidationGroup(g1, g2)
        validationGroupDefaults = assignValidationGroup(g1, g3)
        if validationGroup == 'contoursEqual' and validationGroupDefaults != 'contoursEqual':
            print(f'\tupdating /{glyphName} from {newDefaultName}...')
            font.insertGlyph(g3, name=glyphName)
            if not fontChanged:
                fontChanged = True
    if fontChanged and not preflight:
        print('\tsaving font...')
        font.save()
        font.close()
    print()

# --------
# do stuff
# --------

baseFolder     = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder  = os.path.join(baseFolder, 'Sources', subFamilyName)

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

newDefaultPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{newDefaultName}.ufo')
oldDefaultPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{oldDefaultName}.ufo')

newDefault = OpenFont(newDefaultPath, showInterface=False)
oldDefault = OpenFont(oldDefaultPath, showInterface=False)

ufoPaths.remove(newDefaultPath)
ufoPaths.remove(oldDefaultPath)

for ufoPath in ufoPaths:
    font = OpenFont(ufoPath, showInterface=False)
    updateGlyphsFromDefault(font, oldDefault, newDefault, glyphNames)

updateGlyphsFromDefault(oldDefault, oldDefault, newDefault, glyphNames)


