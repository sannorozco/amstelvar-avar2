# menuTitle: cleanup all sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePaths   = glob.glob(f'{sourcesFolder}/*.ufo')

glyphLibKeys = []
fontLibKeys  = []

for srcPath in sourcePaths:
    name = os.path.splitext(os.path.split(srcPath)[-1])[0].split('_')[-1]

    f = OpenFont(srcPath, showInterface=False)
    for k in f.lib.keys():
        if k.startswith('public.'):
            continue
        if k not in fontLibKeys:
            fontLibKeys.append(k)
            
print(fontLibKeys)

