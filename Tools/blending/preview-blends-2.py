'''
A rewrite of BlendsPreview using the new avar tools in fontTools.

'''

import os
import drawBot as DB
from defcon.objects.glyph import Glyph
from fontTools.ttLib import TTFont
from fontTools.varLib.avar.build import build
from fontTools.varLib.avar.map import map
from ufoProcessor.ufoOperator import UFOOperator
from mutatorMath.objects.location import Location

designspacePath = '/Users/gferreira/hipertipo/fonts/fontbureau/amstelvar-avar2/Sources/Roman/AmstelvarA2-Roman_avar2.designspace'

def getEffectiveLocation(designspacePath, blendedLocation):
    font = TTFont()
    build(font, designspacePath)
    return map(font, blendedLocation)

def instantiateGlyph(operator, glyphName, location):
    glyphMutator, uni = operator.getGlyphMutator(glyphName)
    if not glyphMutator:
        return
    instance = glyphMutator.makeInstance(Location(**location))
    g = instance.extractGlyph(Glyph())
    return g

def drawGlyph(g):
    B = DB.BezierPath()
    g.draw(B)
    DB.drawPath(B)

opszs = [8, 14, 144]
wghts = [100, 400, 1000]
wdths = [50, 100, 125]

glyphName   = 'n'
glyphScale  = 0.045
cellSize    = 2000 * glyphScale

x = y = 40

DB.newDrawing()
DB.size('A4')
DB.translate(x, y)

operator = UFOOperator()
operator.read(designspacePath)
operator.loadFonts()

for i, opsz in enumerate(opszs):
    for j, wght in enumerate(reversed(wghts)):
        for k, wdth in enumerate(wdths):

            blendedLocation = dict(wght=wght, wdth=wdth, opsz=opsz)

            parametricLocation = getEffectiveLocation(designspacePath, blendedLocation)

            g = instantiateGlyph(operator, glyphName, parametricLocation)
            if not g:
                continue

            with DB.savedState():
                DB.translate(k * cellSize * 1.5, j * cellSize)
                DB.scale(glyphScale)
                drawGlyph(g)

    DB.translate(0, cellSize * len(wghts))

DB.saveImage('test-avar.pdf')
