import os, glob
from xTools4.modules.validation import validateFonts

subfamilyName = ['Roman', 'Italic'][0]
defaultName   = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subfamilyName)
defaultPath   = os.path.join(sourcesFolder, f'AmstelvarA2-{subfamilyName}_{defaultName}.ufo')

options = {
    'width'      : False,
    'left'       : False,
    'right'      : False,
    'points'     : True,
    'components' : True,
    'anchors'    : True,
    'unicodes'   : True,
}

txt = 'validating sources...\n\n'
for check in options:
    txt += f'\t- {check}\n'
txt += '\n'

# get default font
defaultFont = OpenFont(defaultPath, showInterface=False)
txt += f'\tdefault font: {defaultFont.info.familyName} {defaultFont.info.styleName}\n\n'

# get target sources
targetPaths = glob.glob(f'{sourcesFolder}/*.ufo')

if defaultPath in targetPaths:
    targetPaths.remove(defaultPath)
targetFonts = [OpenFont(f, showInterface=False) for f in targetPaths]

txt += validateFonts(targetFonts, defaultFont, options)
txt += '...done!\n\n'

print(txt)
