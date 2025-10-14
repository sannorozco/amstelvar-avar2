import os, json
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import Window, Button, CheckBox, TextBox, Slider
from defcon.objects.glyph import Glyph
from defcon.objects.font import Font
from mojo.roboFont import RGlyph, CurrentGlyph, OpenWindow, OpenFont
from ufoProcessor.ufoOperator import UFOOperator
from mutatorMath.objects.location import Location
from xTools4.modules.encoding import char2psname

baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePath  = os.path.join(sourcesFolder, 'AmstelvarA2-Roman_avar2.designspace')
blendsPath       = os.path.join(sourcesFolder, 'blends.json')
baseFolderOld    = os.path.join(os.path.dirname(baseFolder), 'amstelvar')
familyNameOld    = 'Amstelvar'
sourcesFolderOld = os.path.join(baseFolderOld, subFamilyName)
tempEditModeKey  = 'com.xTools4.tempEdit.mode'

# proofing mode: 0=batch, 1=dialog
mode = 1

# batch settings:

ASCII = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;!?@#$%&*{|}[\\](/)_<=>+~- '"^`'''

glyphNames = [char2psname(char) for char in ASCII]
compare    = True
margins    = True
levels     = False
labels     = True
wireframe  = False
savePDF    = True

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

def getVarDistance(sourceLocation, defaultLocation):
    n = 1
    for k in sourceLocation.keys():
        if sourceLocation[k] != defaultLocation[k]:
            n += 1
    return n


class BlendsPreview:

    margin      = 40
    glyphScale  = 0.045
    cellSize    = 2000
    labelsSize  = 5

    compare     = False
    wireframe   = False
    margins     = False
    labels      = False
    levels      = False
    levelsShow  = 1

    opszs = [8, 14, 144]
    wghts = [100, 400, 1000]
    wdths = [50, 100, 125]

    compareColors = [
        (1, 0, 1), # Amstelvar
        (0, 1, 1), # AmstelvarA2
    ]

    levelsColors = [
        (0.0, 0.5, 1.0), # monovar
        (1.0, 0.0, 0.5), # duovars
        (0.0, 1.0, 0.5), # trivars
        (1.0, 0.5, 0.0), # quadvars
    ]

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

    def getColors(self, level=0):
        colors = {
            'fillHeader2'    : (0,),
            'fill2'          : (0,),
            'stroke2'        : None,
            'points2'        : None,
            'strokeMargins2' : (0,),
        }
        if self.wireframe:
            colors['fill2']   = None
            colors['stroke2'] = 0,
            colors['points2'] = 0,

        levelColor = self.levelsColors[level]

        if self.compare and not self.levels:
            colors['fillHeader2']    = self.compareColors[1]
            colors['fill2']          = self.compareColors[1]
            colors['strokeMargins2'] = self.compareColors[1]

            colors['fillHeader1']    = self.compareColors[0]
            colors['fill1']          = self.compareColors[0]
            colors['strokeMargins1'] = self.compareColors[0]
            colors['stroke1']        = None
            colors['points1']        = None

            if self.wireframe:
                colors['fill2']   = None
                colors['stroke2'] = self.compareColors[1]
                colors['points2'] = self.compareColors[1]
                colors['fill1']   = None
                colors['stroke1'] = self.compareColors[0]
                colors['points1'] = self.compareColors[0]

        elif not self.compare and self.levels:
            colors['fill2']          = levelColor
            colors['strokeMargins2'] = levelColor

            if self.wireframe:
                colors['fill2']   = None
                colors['stroke2'] = levelColor
                colors['points2'] = levelColor

        elif self.compare and self.levels:
            colors['fill2']          = levelColor
            colors['strokeMargins2'] = levelColor

            colors['fillHeader1']    = 0.8,
            colors['fill1']          = 0.9,
            colors['stroke1']        = None # 0.8,
            colors['points1']        = None
            colors['strokeMargins1'] = 0.8,

            if self.wireframe:
                colors['fill1']   = None
                colors['stroke1'] = 0.7,
                colors['points1'] = 0.7,

                colors['fill2']   = None
                colors['stroke2'] = levelColor
                colors['points2'] = levelColor

        return colors

    def draw(self, glyphName):

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

        colors = self.getColors()

        # draw page header
        with DB.savedState():
            m = 20
            DB.translate(0, DB.height()-m)
            DB.fill(*colors['fillHeader2'])
            DB.text('AmstelvarA2', (m, 0))
            if self.compare:
                DB.save()
                DB.translate(DB.textSize('AmstelvarA2 ')[0] + m, 0)
                DB.fill(*colors['fillHeader1'])
                DB.text('Amstelvar', (0, 0))
                DB.restore()

            DB.fill(0,)
            DB.text(glyphName, (DB.width()/2, 0), align='center')
            DB.text(subFamilyName, (DB.width()-m, 0), align='right')

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

                    # get var distance
                    n = 0 if styleName == 'wght400' else len(styleName.split('_'))

                    if n >= self.levelsShow:
                        continue

                    colors = self.getColors(n)

                    DB.save()
                    DB.translate(k * cellWidth, j * cellHeight)

                    # draw location name
                    if self.labels:
                        with DB.savedState():
                            DB.rotate(90)
                            DB.fill(0)
                            DB.font('Menlo')
                            DB.fontSize(self.labelsSize)
                            DB.text(_styleName.replace('_', ' '), (0, 10))

                    DB.scale(self.glyphScale)

                    # draw glyph AmstelvarA2
                    if self.wireframe:
                        DB.strokeWidth(2)

                    fill2   = colors['fill2']
                    stroke2 = colors['stroke2']
                    points2 = colors['points2']

                    if fill2 is not None:
                        DB.fill(*fill2)
                    else:
                        DB.fill(fill2)

                    if stroke2 is not None:
                        DB.stroke(*stroke2)
                    else:
                        DB.stroke(stroke2)

                    drawGlyph(g2)

                    if self.wireframe and points2 is not None:
                        DB.fill(*points2)
                        DB.stroke(None)
                        for c in g2.contours:
                            for p in c.points:
                                DB.oval(p.x-r, p.y-r, r*2, r*2)

                    if self.margins:
                        yBottom = font.info.descender
                        yTop    = font.info.unitsPerEm - abs(yBottom)
                        DB.strokeWidth(1)
                        DB.stroke(*colors['strokeMargins2'])
                        DB.line((0, yBottom), (0, yTop))
                        DB.line((g2.width, yBottom), (g2.width, yTop))

                    # draw glyph Amstelvar
                    if self.compare:
                        ufoPathOld = os.path.join(sourcesFolderOld, f'{familyNameOld}-{subFamilyName}_{styleName}.ufo')
                        assert os.path.exists(ufoPathOld)
                        f = OpenFont(ufoPathOld, showInterface=False)
                        g1 = f[glyphName]

                        if self.wireframe:
                            DB.strokeWidth(2)

                        fill1   = colors['fill1']
                        stroke1 = colors['stroke1']
                        points1 = colors['points1']

                        if fill1 is not None:
                            DB.fill(*fill1)
                        else:
                            DB.fill(fill1)

                        if stroke1 is not None:
                            DB.stroke(*stroke1)
                        else:
                            DB.stroke(stroke1)

                        drawGlyph(g1)

                        if self.wireframe and points1 is not None:
                            DB.stroke(None)
                            DB.fill(*points1)
                            for c in g1.contours:
                                for p in c.points:
                                    DB.oval(p.x-r, p.y-r, r*2, r*2)

                        if self.margins:
                            DB.strokeWidth(1)
                            DB.stroke(*colors['strokeMargins1'])
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
    buttonWidth = 75

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
            'points',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.labels = CheckBox(
            (x, y, self.buttonWidth, self.lineHeight),
            'labels',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.levels = CheckBox(
            (x, y, self.buttonWidth, self.lineHeight),
            'levels',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.levelsShowLabel = TextBox(
            (x, y+4, self.buttonWidth, self.lineHeight),
            'show levels',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        x += self.buttonWidth
        self.w.levelsShow = Slider(
            (x, y, self.buttonWidth, self.lineHeight),
            minValue=1,
            maxValue=4,
            value=4,
            tickMarkCount=4,
            stopOnTickMarks=True,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        self._updatePreview()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = "BlendsPreview"
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

    @property
    def labels(self):
        return self.w.labels.get()

    @property
    def levels(self):
        return int(self.w.levels.get())

    @property
    def levelsShow(self):
        return self.w.levelsShow.get()

    def updatePreviewCallback(self, sender):
        self._updatePreview()

    def _updatePreview(self):
        font = CurrentFont()
        if font is None:
            return

        glyph = CurrentGlyph()
        if glyph is not None:
            if font.lib.get(tempEditModeKey) == 'glyphs':
                glyphName = glyph.name[:glyph.name.rfind('.')]
            else:
                glyphName = glyph.name
        else:
            if len(font.selectedGlyphs):
                glyphName = font.selectedGlyphs[0].name
                if font.lib.get(tempEditModeKey) == 'glyphs':
                    glyphName = glyphName[:glyphName.rfind('.')]
            else:
                glyphName = None

        B = BlendsPreview()
        B.compare    = self.compare
        B.wireframe  = self.wireframe
        B.margins    = self.margins
        B.labels     = self.labels
        B.levels     = self.levels
        B.levelsShow = self.levelsShow
        B.draw(glyphName)

        pdfData = DB.pdfImage()
        self.w.canvas.setPDFDocument(pdfData)


if __name__ == '__main__':

    if mode:
        OpenWindow(BlendsPreviewDialog)

    else:
        pdfPath = os.path.join(baseFolder, 'Proofs', 'PDF', f'blending-preview_{subFamilyName}.pdf')
        B = BlendsPreview()
        B.compare    = compare
        B.margins    = margins
        B.wireframe  = wireframe
        B.levels     = levels
        B.levelsShow = levelsShow
        B.labels     = labels

        for glyphName in glyphNames:
            B.draw(glyphName)
        if savePDF:
            print(f'saving {pdfPath}...', end=' ')
            B.save(pdfPath)
            print(f'done!\n')
