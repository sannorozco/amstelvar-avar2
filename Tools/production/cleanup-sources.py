# menuTitle: cleanup unnecessary data from all sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)

ufoPaths  = glob.glob(f'{sourcesFolder}/*.ufo')

ignoreFontLibKeys = [
    'com.typemytype.robofont.italicSlantOffset',
    'com.typemytype.robofont.segmentType',
]

fontLibKeys  = []
glyphLibKeys = []

print('cleaning up sources...')

for ufoPath in ufoPaths:
    fileName = os.path.split(ufoPath)[-1]
    name = os.path.splitext(fileName)[0].split('_')[-1]
    print(f'\tcleaning up {fileName}...')
    f = OpenFont(ufoPath, showInterface=False)
    # clear font libs
    print(f'\t\tcleaning up font libs...')
    for k in f.lib.keys():
        if k.startswith('public.') or k in ignoreFontLibKeys:
             continue
        if k not in fontLibKeys:
            fontLibKeys.append(k)
        del f.lib[k]
    # clear glyph libs
    print(f'\t\tcleaning up glyph libs and mark colors...')
    for g in f:
        for k in g.lib.keys():
            if k not in glyphLibKeys:
                glyphLibKeys.append(k)
            del g.lib[k]
        # clear mark color
        g.markColor = None
    # done
    print()
    f.save()
    f.close()

print('...done!\n')

print()
print('deleted font libs:')
for k in fontLibKeys:
    print(f'- {k}')
print()
print('deleted glyph libs:')
for k in glyphLibKeys:
    print(f'- {k}')
print()
