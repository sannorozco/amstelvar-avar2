import os, json
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import Window, Button, CheckBox
from defcon.objects.glyph import Glyph
from mojo.roboFont import RGlyph, CurrentGlyph
from ufoProcessor.ufoOperator import UFOOperator
from mutatorMath.objects.location import Location

tempEditModeKey = 'com.xTools4.tempEdit.mode'

def instantiateGlyph(operator, glyphName, location):
    glyphMutator, uni = operator.getGlyphMutator(glyphName)
    if not glyphMutator:
        return
    instance = glyphMutator.makeInstance(Location(**location))
    g = instance.extractGlyph(Glyph())
    return RGlyph(g)

def drawGlyph(g):
    B = DB.BezierPath()
    g.draw(B)
    DB.drawPath(B)

def getShortStyleName(opsz, wght, wdth):
    styleNameParts = []
    if opsz != 14:
        styleNameParts.append(f'opsz{opsz}')
    if wght != 400:
        styleNameParts.append(f'wght{wght}')
    if wdth != 100:
        styleNameParts.append(f'wdth{wdth}')
    if opsz == 14 and wght == 400 and  wdth == 100:
        styleNameParts.append(f'wght{wght}')
    return '_'.join(styleNameParts)

baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
familyName       = 'AmstelvarA2'
subfamilyName    = ['Roman', 'Italic'][0]
sourcesFolder    = os.path.join(baseFolder, 'Sources', subfamilyName)
designspacePath  = os.path.join(sourcesFolder, 'AmstelvarA2-Roman_avar2.designspace')
blendsPath       = os.path.join(sourcesFolder, 'blends.json')
baseFolderOld    = os.path.join(os.path.dirname(baseFolder), 'amstelvar')
familyNameOld    = 'Amstelvar'
sourcesFolderOld = os.path.join(baseFolderOld, subfamilyName)

class BlendsPreview:

    title       = 'BlendsPreview'
    width       = 800
    height      = 600
    padding     = 10
    lineHeight  = 22
    verbose     = True
    buttonWidth = 80

    glyphName   = None
    margin      = 40
    glyphScale  = 0.045
    cellSize    = 2000
    captionSize = 7
    color1      = 1, 0, 1
    color2      = 0, 1, 1

    opszs = [8, 14, 144]
    wghts = [100, 400, 1000]
    wdths = [50, 100, 125]

    def __init__(self):

        self.operator = UFOOperator()
        self.operator.read(designspacePath)
        self.operator.loadFonts()

        with open(blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        self.blends = blendsData['sources']

        self.w = Window(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width*0.7, self.height*0.7))

        x = y = p = self.padding
        self.w.canvas = DrawView((x, y, -p, -(self.lineHeight + p*2)))

        y = -(self.lineHeight + p)
        self.w.updatePreviewButton = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'update',
                callback=self.updatePreviewCallback,
                sizeStyle='small')

        x += self.buttonWidth + p*2
        self.w.compare = CheckBox(
            (x, y, self.buttonWidth, self.lineHeight),
            'compare',
            callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.margins = CheckBox(
            (x, y, self.buttonWidth, self.lineHeight),
            'margins',
            callback=self.updatePreviewCallback,
            sizeStyle='small')

        self.updatePreview()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    @property
    def compare(self):
        return self.w.compare.get()

    @property
    def margins(self):
        return self.w.margins.get()

    def updatePreviewCallback(self, sender):
        self.updatePreview()

    def updatePreview(self):

        g = CurrentGlyph()
        if g is not None:
            if g.font.lib.get(tempEditModeKey) == 'glyphs':
                self.glyphName = g.name[:g.name.rfind('.')]
            else:
                self.glyphName = g.name
        else:
            self.glyphName = None

        cellWidth  = self.cellSize * self.glyphScale * 1.5
        cellHeight = self.cellSize * self.glyphScale

        w = cellWidth  * len(self.wdths) + self.margin*2
        h = cellHeight * len(self.wghts) * len(self.opszs) + self.margin*2
        x = y = self.margin

        DB.newDrawing()
        DB.size(w, h)
        DB.blendMode('multiply')

        # no glyph = empty page
        if self.glyphName is None:
            pdfData = DB.pdfImage()
            self.w.canvas.setPDFDocument(pdfData)
            return

        # draw header
        with DB.savedState():
            DB.translate(20, DB.height()-20)
            if self.compare:
                DB.fill(*self.color2)
            DB.text('AmstelvarA2', (0, 0))
            if self.compare:
                DB.translate(DB.textSize('AmstelvarA2 ')[0], 0)
                DB.fill(*self.color1)
                DB.text('Amstelvar', (0, 0))

        DB.translate(x, y)

        for i, opsz in enumerate(self.opszs):
            for j, wght in enumerate(reversed(self.wghts)):
                for k, wdth in enumerate(self.wdths):
                    _styleName = f'opsz{opsz}_wght{wght}_wdth{wdth}'
                    styleName  = getShortStyleName(opsz, wght, wdth)
                    
                    assert styleName in self.blends
                    location = self.blends[styleName]
                    g2 = instantiateGlyph(self.operator, self.glyphName, location)

                    if not g2:
                        continue

                    DB.save()
                    DB.translate(k * cellWidth, j * cellHeight)
                    DB.scale(self.glyphScale)

                    # draw glyph AmstelvarA2
                    if self.compare:
                        DB.fill(*self.color2)
                    drawGlyph(g2)
                    if self.margins:
                        yBottom = g.font.info.descender
                        yTop    = g.font.info.unitsPerEm - abs(yBottom)
                        with DB.savedState():
                            if self.compare:
                                DB.stroke(*self.color2)
                            else:
                                DB.stroke(0.5)
                            DB.strokeWidth(0.5 / self.glyphScale)
                            DB.line((0, yBottom), (0, yTop))
                            DB.line((g2.width, yBottom), (g2.width, yTop))

                    # draw glyph Amstelvar
                    if self.compare:
                        ufoPathOld = os.path.join(sourcesFolderOld, f'{familyNameOld}-{subfamilyName}_{styleName}.ufo')
                        assert os.path.exists(ufoPathOld)
                        f = OpenFont(ufoPathOld, showInterface=False)
                        g1 = f[self.glyphName]
                        DB.fill(*self.color1)
                        drawGlyph(g1)
                        if self.margins:
                            DB.stroke(*self.color1)
                            DB.strokeWidth(0.5 / self.glyphScale)
                            DB.line((0, yBottom), (0, yTop))
                            DB.line((g1.width, yBottom), (g1.width, yTop))

                    DB.restore()

            DB.translate(0, cellHeight*3)

        pdfData = DB.pdfImage()
        self.w.canvas.setPDFDocument(pdfData)


if __name__ == '__main__':
        
    BlendsPreview()
