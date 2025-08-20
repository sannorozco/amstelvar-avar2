# menuTitle: cleanup unnecessary data from all sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

preflight = False
ufoPaths  = glob.glob(f'{sourcesFolder}/*.ufo')

ignoreFontLibKeys = [
    'com.typemytype.robofont.italicSlantOffset',
    'com.typemytype.robofont.segmentType',
]

fontLibKeys  = []
glyphLibKeys = []

for ufoPath in ufoPaths:
    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    f = OpenFont(ufoPath, showInterface=False)
    # clear font libs
    for k in f.lib.keys():
        if k.startswith('public.') or k in ignoreFontLibKeys:
             continue
        if k not in fontLibKeys:
            fontLibKeys.append(k)
            del fontLibKeys[k]
    # clear glyph libs
    for g in f:
        for k in g.lib.keys():
            if k not in glyphLibKeys:
                glyphLibKeys.append(k)
                del glyphLibKeys[k]
        # clear mark color
        g.markColor = None

    f.save()
    f.close()

print(fontLibKeys)
print()
print(glyphLibKeys)

print('...done!\n')
