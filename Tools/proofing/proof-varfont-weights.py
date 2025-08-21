import os, datetime
import drawBot as DB

baseFolder  = os.path.dirname(os.path.dirname(os.getcwd()))
fontsFolder = os.path.join(baseFolder, 'Fonts')
pdfsFolder  = os.path.join(baseFolder, 'Proofs', 'PDF')

assert os.path.exists(fontsFolder)
assert os.path.exists(pdfsFolder)

subFamilyName = ['Roman', 'Italic'][0]
fontPath = os.path.join(fontsFolder, f'AmstelvarA2-{subFamilyName}_avar2.ttf')

glyphset  = list('''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;!?@#$%&*{|}[\\](/)_<=>+~-'"^`''')

fs = 36
p  = 30, 10, 10, 10

stepsX = 12
stepsY = 8

wghts = range(100, 1001, 100) # [100, 400, 1000]
wdths = [50, 100, 150]
opszs = [8, 14, 144]

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

savePDF = True

proofName = f'varfont-weights_{subFamilyName}.pdf'
pdfPath   = os.path.join(pdfsFolder, proofName)

DB.newDrawing()

for opsz in opszs:
    for wdth in wdths:

        DB.newPage('A4Landscape')

        with DB.savedState():
            x1 = p[3]
            x2 = DB.width() / 2
            x3 = DB.width() - p[1]
            y = DB.height() - p[0]*0.57
            DB.font('Menlo')
            DB.fontSize(9)
            DB.fill(1, 0, 0)
            DB.text(f'AmstelvarA2 {subFamilyName}', (x1, y), align='left')
            DB.text(f'opsz{opsz} wdth{wdth}', (x2, y), align='center')
            DB.text(f'{now}', (x3, y), align='right')

        DB.strokeWidth(0.5)
        DB.stroke(0, 0, 0)
        DB.fill(None)
        DB.fontSize(fs)
        DB.font(fontPath)

        _variations = DB.fontVariations()
        _variations['opsz'] = opsz
        _variations['wdth'] = wdth

        stepX = (DB.width()-p[1]-p[3])  / stepsX
        stepY = (DB.height()-p[0]-p[2]) / stepsY

        y = DB.height() - p[0] - stepY

        n = 0
        for i in range(stepsY):
            x = p[3]
            for j in range(stepsX):
                if n < len(glyphset):
                    with DB.savedState():
                        pos = x + stepX / 2, y + stepX * 0.33
                        DB.stroke(None)
                        DB.fill(0, 0, 0, 0.1)
                        for wght in wghts:
                            _variations['wght'] = wght
                            DB.fontVariations(**_variations)
                            DB.text(glyphset[n], pos, align='center')

                    DB.rect(x, y, stepX, stepY)

                    n += 1
                    x += stepX

            y -= stepY

if savePDF:
    DB.saveImage(pdfPath)
