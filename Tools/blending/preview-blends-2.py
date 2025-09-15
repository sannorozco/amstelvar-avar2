import os, json
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import Window, Button, CheckBox
from defcon.objects.glyph import Glyph
from defcon.objects.font import Font
from mojo.roboFont import RGlyph, CurrentGlyph, OpenWindow, OpenFont
from ufoProcessor.ufoOperator import UFOOperator
from mutatorMath.objects.location import Location


baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
familyName       = 'AmstelvarA2'
subfamilyName    = ['Roman', 'Italic'][0]
sourcesFolder    = os.path.join(baseFolder, 'Sources', subfamilyName)
designspacePath  = os.path.join(sourcesFolder, 'AmstelvarA2-Roman_avar2.designspace')
blendsPath       = os.path.join(sourcesFolder, 'blends.json')
baseFolderOld    = os.path.join(os.path.dirname(baseFolder), 'amstelvar')
familyNameOld    = 'Amstelvar'
sourcesFolderOld = os.path.join(baseFolderOld, subfamilyName)
tempEditModeKey  = 'com.xTools4.tempEdit.mode'


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


class BlendsPreview:

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
        # load blends data
        with open(blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        self.blends = blendsData['sources']
        # initiate operator + sources
        self.operator = UFOOperator()
        self.operator.read(designspacePath)
        self.operator.loadFonts()
        # initiate drawing
        DB.newDrawing()

    def draw(self, glyphName, compare=False, wireframe=False, margins=False):

        cellWidth  = self.cellSize * self.glyphScale * 1.5
        cellHeight = self.cellSize * self.glyphScale

        w = cellWidth  * len(self.wdths) + self.margin * 2
        h = cellHeight * len(self.wghts) * len(self.opszs) + self.margin * 2
        x = y = self.margin

        DB.newPage(w, h)
        DB.blendMode('multiply')

        # no glyph = empty page
        if glyphName is None:
            return

        # draw page header
        with DB.savedState():
            DB.translate(20, DB.height()-20)
            if compare:
                DB.fill(*self.color2)
            DB.text('AmstelvarA2', (0, 0))
            if compare:
                DB.translate(DB.textSize('AmstelvarA2 ')[0], 0)
                DB.fill(*self.color1)
                DB.text('Amstelvar', (0, 0))

        DB.translate(x, y)

        r = 10

        font = Font(self.operator.doc.default.path)

        for i, opsz in enumerate(self.opszs):
            for j, wght in enumerate(reversed(self.wghts)):
                for k, wdth in enumerate(self.wdths):
                    _styleName = f'opsz{opsz}_wght{wght}_wdth{wdth}'
                    styleName  = getShortStyleName(opsz, wght, wdth)
                    
                    assert styleName in self.blends
                    location = self.blends[styleName]
                    g2 = instantiateGlyph(self.operator, glyphName, location)

                    if not g2:
                        continue

                    DB.save()
                    DB.translate(k * cellWidth, j * cellHeight)
                    DB.scale(self.glyphScale)

                    # draw glyph AmstelvarA2

                    if compare:
                        DB.fill(*self.color2)

                    if wireframe:
                        with DB.savedState():
                            DB.fill(None)
                            DB.strokeWidth(2)
                            if compare:
                                DB.stroke(*self.color2)
                            else:
                                DB.stroke(0)
                            drawGlyph(g2)
                        for c in g2.contours:
                            for p in c.points:
                                DB.oval(p.x-r, p.y-r, r*2, r*2)

                    else:
                        drawGlyph(g2)

                    if margins:
                        yBottom = font.info.descender
                        yTop    = font.info.unitsPerEm - abs(yBottom)
                        with DB.savedState():
                            if compare:
                                DB.stroke(*self.color2)
                            else:
                                DB.stroke(0.5)
                            DB.strokeWidth(1)
                            DB.line((0, yBottom), (0, yTop))
                            DB.line((g2.width, yBottom), (g2.width, yTop))

                    # draw glyph Amstelvar
                    if compare:
                        ufoPathOld = os.path.join(sourcesFolderOld, f'{familyNameOld}-{subfamilyName}_{styleName}.ufo')
                        assert os.path.exists(ufoPathOld)
                        f = OpenFont(ufoPathOld, showInterface=False)
                        g1 = f[glyphName]

                        DB.fill(*self.color1)
                        if wireframe:
                            with DB.savedState():
                                DB.fill(None)
                                DB.strokeWidth(2)
                                if compare:
                                    DB.stroke(*self.color1)
                                else:
                                    DB.stroke(0)
                                drawGlyph(g1)
                            for c in g1.contours:
                                for p in c.points:
                                    DB.oval(p.x-r, p.y-r, r*2, r*2)

                        else:
                            drawGlyph(g1)

                        if margins:
                            DB.stroke(*self.color1)
                            DB.strokeWidth(1)
                            DB.line((0, yBottom), (0, yTop))
                            DB.line((g1.width, yBottom), (g1.width, yTop))

                    DB.restore()

            DB.translate(0, cellHeight*3)

    def save(self, pdfPath):
        DB.saveImage(pdfPath)


class BlendsPreviewDialog:

    title       = 'BlendsPreview'
    width       = 800
    height      = 600
    padding     = 10
    lineHeight  = 22
    verbose     = True
    buttonWidth = 80

    def __init__(self):

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
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.margins = CheckBox(
            (x, y, self.buttonWidth, self.lineHeight),
            'margins',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.wireframe = CheckBox(
            (x, y, self.buttonWidth, self.lineHeight),
            'wireframe',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        self._updatePreview()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    @property
    def compare(self):
        return self.w.compare.get()

    @property
    def margins(self):
        return self.w.margins.get()

    @property
    def wireframe(self):
        return self.w.wireframe.get()

    def updatePreviewCallback(self, sender):
        self._updatePreview()

    def _updatePreview(self):

        g = CurrentGlyph()
        if g is not None:
            if g.font.lib.get(tempEditModeKey) == 'glyphs':
                glyphName = g.name[:g.name.rfind('.')]
            else:
                glyphName = g.name
        else:
            glyphName = None

        B = BlendsPreview()
        B.draw(glyphName, compare=self.compare, wireframe=self.wireframe, margins=self.margins)

        pdfData = DB.pdfImage()
        self.w.canvas.setPDFDocument(pdfData)



if __name__ == '__main__':

    # glyphNames  = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # glyphNames += list('abcdefghijklmnopqrstuvwxyz')
    # glyphNames += ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    # B = BlendsPreview()
    # for glyphName in glyphNames:
    #     B.draw(glyphName, compare=True)
    # B.save('test-avar-ZZZ.pdf')

    OpenWindow(BlendsPreviewDialog)
