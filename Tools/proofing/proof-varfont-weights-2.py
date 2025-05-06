import os, datetime
import drawBot as DB

baseFolder  = os.path.dirname(os.path.dirname(os.getcwd()))
fontsFolder = os.path.join(baseFolder, 'Fonts')
pdfsFolder  = os.path.join(baseFolder, 'Proofs', 'PDF')

# --------
# settings
# --------

subFamilyName = ['Roman', 'Italic'][0]

fs = 120              # font size
p  = 25, 10, 10, 10   # padding

chars = list('HOGCE')

wghts = [100, 400, 1000]
wdths = [50, 100, 150]
opszs = [8, 14, 144]

debug   = True
debugBG = False
savePDF = False


# --------
# do stuff
# --------

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

fontPath = os.path.join(fontsFolder, f'AmstelvarA2-{subFamilyName}_avar2.ttf')

if not debug:
    wghts = range(wghts[0], wghts[-1], 100)

DB.newDrawing()

for char in chars:

    DB.newPage('A4Landscape')
    DB.blendMode('multiply')

    # with DB.savedState():
    #     DB.fill(None)
    #     DB.stroke(0.5)
    #     DB.rect(p[3], p[2], width()-p[1]-p[3], height()-p[0]-p[2])

    with DB.savedState():
        x1 = p[3]
        x2 = DB.width() / 2
        x3 = DB.width() - p[1]
        y = DB.height() - p[0]*0.57
        DB.font('Menlo')
        DB.fontSize(7)
        DB.text(f'AmstelvarA2 {subFamilyName}',
            (x1, y), align='left')
        DB.text(char, (x2, y), align='center')
        DB.text(f'{now}', (x3, y), align='right')

    stepX = (DB.width()-p[1]-p[3])  / len(wdths)
    stepY = (DB.height()-p[0]-p[2]) / len(opszs)

    a = 1.0 / len(wghts) * 0.5

    DB.font(fontPath)
    DB.fontSize(fs)
    DB.stroke(None)
    DB.translate(0, -p[0])

    for i, wdth in enumerate(wdths):
        for j, opsz in enumerate(opszs):
            _variations = DB.fontVariations()
            _variations['opsz'] = opsz
            _variations['wdth'] = wdth

            x = i * stepX + stepX/2
            y = j * stepY + stepY/2    
            for wi, wght in enumerate(wghts):
                _variations['wght'] = wght
                DB.fontVariations(**_variations)
                if debug and len(wghts) <= 3:
                    c = {
                        100  : (0, 1, 1),
                        400  : (1, 0, 1),
                        1000 : (1, 1, 0),
                    }[wght]
                    DB.fill(*c)
                else:
                    DB.fill(0, a)
                w, h = DB.textSize(char)
                if debug and debugBG:
                    with DB.savedState():
                        DB.fill(c[0], c[1], c[2], 0.15)
                        DB.rect(x - w/2, y - h*0.27, w, h)
                DB.text(char, (x, y), align='center')

                if wi == 0:
                    with DB.savedState():
                        DB.fill(0)
                        DB.font('Menlo')
                        DB.fontSize(7)
                        DB.lineHeight(10)
                        DB.fontVariations(resetVariations=True)
                        DB.text(f'opsz {opsz}\nwdth {wdth}', (x, y-20), align='center')                                        

if savePDF:
    proofName = f'varfont-weights_{subFamilyName}.pdf'
    pdfPath   = os.path.join(pdfsFolder, proofName)
    DB.saveImage(pdfPath)
