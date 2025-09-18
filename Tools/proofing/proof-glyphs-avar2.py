import os, datetime
import drawBot as DB
from xTools4.modules.encoding import char2psname

baseFolder   = os.path.dirname(os.path.dirname(os.getcwd()))
pdfsFolder   = os.path.join(baseFolder, 'Proofs', 'PDF')
fontsFolder  = os.path.join(baseFolder, 'Fonts')
fontRoman    = os.path.join(fontsFolder, 'AmstelvarA2-Roman_avar2.ttf')
fontItalic   = os.path.join(fontsFolder, 'AmstelvarA2-Italic_avar2.ttf')

assert os.path.exists(pdfsFolder)
assert os.path.exists(fontRoman)
assert os.path.exists(fontItalic)

fontRoman_old  = os.path.join(fontsFolder, 'legacy', 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf')
fontItalic_old = os.path.join(fontsFolder, 'legacy', 'Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf')

_wdth = [ 50, 100, 150 ]
_wght = [ 100, 400, 1000 ]
_opsz = [ 8, 14, 144 ]

fontStyles = ['Italic', 'Roman'] #[1:]
fontsNew = { 'Roman'  : fontRoman, 'Italic' : fontItalic }
fontsOld = { 'Roman'  : fontRoman_old, 'Italic' : fontItalic_old }

compare = True
savePDF = True

fs = 56

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

controlGlyphs = [char2psname(char) for char in list('HOVTnovr01$')]

UC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lc = UC.lower()

ASCII  = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()

LATIN1 = ASCII + ' exclamdown cent sterling currency yen brokenbar section dieresis copyright ordfeminine guillemotleft logicalnot registered macron degree plusminus twosuperior threesuperior acute uni00B5 micro paragraph periodcentered cedilla onesuperior ordmasculine guillemotright onequarter onehalf threequarters questiondown Agrave Aacute Acircumflex Atilde Adieresis Aring AE Ccedilla Egrave Eacute Ecircumflex Edieresis Igrave Iacute Icircumflex Idieresis Eth Ntilde Ograve Oacute Ocircumflex Otilde Odieresis multiply Oslash Ugrave Uacute Ucircumflex Udieresis Yacute Thorn germandbls agrave aacute acircumflex atilde adieresis aring ae ccedilla egrave eacute ecircumflex edieresis igrave iacute icircumflex idieresis eth ntilde ograve oacute ocircumflex otilde odieresis divide oslash ugrave uacute ucircumflex udieresis yacute thorn ydieresis idotless Lslash lslash OE oe Scaron scaron Ydieresis Zcaron zcaron florin circumflex caron breve dotaccent ring ogonek tilde hungarumlaut endash emdash quoteleft quoteright quotesinglbase quotedblleft quotedblright quotedblbase dagger daggerdbl bullet ellipsis perthousand guilsinglleft guilsinglright fraction Euro trademark minus fi fl'.split()

glyphNames = controlGlyphs # UC # ASCII

ignoreGlyphs = 'space nbspace CR .notdef .null gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcomb dieresiscomb hookabovecomb ringcomb hungarumlautcomb caroncomb breveinvertedcomb dblgravecomb horncomb dotbelowcomb dieresisbelowcomb commaaccentcomb cedillacomb ogonekcomb brevebelowcomb macronbelowcomb commaaccentturnedcomb gravecomb-stack acutecomb-stack circumflexcomb-stack tildecomb-stack macroncomb-stack brevecomb-stack dotaccentcomb-stack dieresiscomb-stack hookabovecomb-stack ringcomb-stack hungarumlautcomb-stack caroncomb-stack breveinvertedcomb-stack dblgravecomb-stack gravecomb-stack.case acutecomb-stack.case dieresiscomb-stack.case macroncomb-stack.case circumflexcomb-stack.case caroncomb-stack.case brevecomb-stack.case dotaccentcomb-stack.case ringcomb-stack.case tildecomb-stack.case hungarumlautcomb-stack.case hookabovecomb-stack.case breveinvertedcomb-stack.case dblgravecomb-stack.case caroncomb.alt tonoscomb dieresistonoscomb breve.cyrcomb yi-dieresiscomb'.split()

DB.newDrawing()

for glyphName in glyphNames:
    if glyphName in ignoreGlyphs:
        continue

    DB.newPage('A4Landscape')

    with DB.savedState():
        mx, my = 13, 12
        yTop = DB.height()-my
        T = FormattedString(fontSize=7, align='left')
        if compare:    
            T.append('AmstelvarA2 ', fill=(0, 1, 1))
            T.append('Amstelvar', fill=(1, 0, 1))
        else:
            T.append('AmstelvarA2')
        DB.text(T, (mx, yTop))
        DB.fontSize(7)
        DB.text(glyphName, (DB.width()/2, yTop), align='center')
        DB.text(now, (DB.width()-mx, yTop), align='right')
        
    #     rotate(90)
    #     W = height()/3
    #     for pt in [8, 14, 144]:
    #         text(f'{pt}', (W/2, -10), align='center')
    #         translate(W, 0)

    w  = DB.width()  / (len(_wght))
    h  = DB.height() / (len(_opsz))

    ww = w / len(_wdth)
    hh = h / 2

    if compare:
        blendMode('multiply')
        compareAlpha = 1.0
        
    for i, wght in enumerate(_wght):
        for j, opsz in enumerate(_opsz):
            for ii, wdth in enumerate(_wdth):
                for jj, styleName in enumerate(fontStyles):
                    fontStyle = fontsNew[styleName]
                    x = i * w + ii * ww + ww * 0.5
                    y = j * h + jj * hh + hh * 0.3
                    T = DB.FormattedString()
                    T.fontSize(fs)
                    T.font(fontStyle)
                    variations = {
                        'opsz' : opsz,
                        'wght' : wght,
                        'wdth' : wdth,
                    }
                    T.fontVariations(**variations)
                    if compare:
                        T.fill(0, 1, 1, compareAlpha)
                    T.appendGlyph(glyphName)
                    DB.text(T, (x, y), align='center')

                    if compare:
                        fontStyle_old = fontsOld[styleName]
                        T2 = DB.FormattedString()
                        T2.fill(1, 0, 1, compareAlpha)
                        T2.fontSize(fs)
                        T2.font(fontStyle_old)
                        T2.fontVariations(**variations)
                        T2.appendGlyph(glyphName)
                        DB.text(T2, (x, y), align='center')

                    with DB.savedState():
                        txt = f'{styleName}\n{opsz} {wght} {wdth}'
                        DB.fontSize(7)
                        DB.text(txt, (x, y-10), align='center')

# save PDF
if savePDF:
    pdfPath = os.path.join(pdfsFolder, 'glyphs-Roman-Italic.pdf')
    if compare:
        pdfPath = pdfPath.replace('.pdf', '_compare.pdf')
    DB.saveImage(pdfPath)
