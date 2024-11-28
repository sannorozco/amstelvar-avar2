# menuTitle: find components which are used in both upper- and lowercase

import os
from mojo.smartSet import readSmartSets

subfamilyName = ['Roman', 'Italic'][1]
defaultName     = 'wght400'
baseFolder      = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder   = os.path.join(baseFolder, 'Sources')
smartSetsPath = os.path.join(sourcesFolder, 'AmstelvarA2.roboFontSets')
defaultPath   = os.path.join(sourcesFolder, subfamilyName, f'AmstelvarA2-{subfamilyName}_{defaultName}.ufo')

assert os.path.exists(smartSetsPath)
assert os.path.exists(defaultPath)

smartSets = readSmartSets(smartSetsPath, useAsDefault=False, font=None)

f = OpenFont(defaultPath, showInterface=False)

components = {}

for case in ['uppercase', 'lowercase']:
    components[case] = []
    for smartSet in smartSets:
        for group in smartSet.groups:
            if case not in group.name:
                continue
            for glyphName in group.glyphNames:
                if glyphName not in f:
                    continue
                g = f[glyphName]
                if not g.components:
                    continue
                for c in g.components:
                    if c.baseGlyph not in components[case]:
                        components[case].append(c.baseGlyph)

componentsUC = set(components['uppercase'])
componentsLC = set(components['lowercase'])

componentsCommon = componentsUC.intersection(componentsLC)

print('components which are used in both UC & lc glyphs:')
for glyphName in componentsCommon:
    print(f'- {glyphName}')

