import os
from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont

ttfPath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Proofs/Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf'
varfont = TTFont(ttfPath)

for opsz in [24, 36, 84]:
    # instantiate TTF
    partial = instantiateVariableFont(varfont, dict(opsz=opsz))
    partialPath = ttfPath.replace('.ttf', f'_opsz{opsz}.ttf')
    partial.save(partialPath)
    # convert to UFO
    f = OpenFont(partialPath, showInterface=False)
    folder, fileName = os.path.split(partialPath)
    ufoPath = os.path.join(folder, f'Amstelvar-Roman_opsz{opsz}.ufo')
    f.save(ufoPath)
    # clear temp TTF
    os.remove(partialPath)
