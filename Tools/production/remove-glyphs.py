# menuTitle: remove glyphs from all sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
ufoPaths      = glob.glob(f'{sourcesFolder}/*.ufo')

glyphNames = ['periodcentered.loclCAT.case', 'hook-stack.case']
dstFonts   = []
preflight  = True

for ufoPath in ufoPaths:
    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        f = OpenFont(ufoPath, showInterface=False)
        glyphOrder = f.glyphOrder
        templateGlyphOrder = f.templateGlyphOrder

        print(f'removing glyphs in {os.path.split(ufoPath)[-1]}...')
        for layerName in f.layerOrder:
            layer = f.getLayer(layerName)
            for glyphName in glyphNames:
                if glyphName in layer:
                    print(f'\tremoving {glyphName} ({layerName})...')
                    del layer[glyphName]
                    if glyphName in glyphOrder:
                        glyphOrder.remove(glyphName)
                        templateGlyphOrder.remove(glyphName)

        f.glyphOrder = glyphOrder
        f.templateGlyphOrder = templateGlyphOrder

        if not preflight:
            f.save()

        print()
