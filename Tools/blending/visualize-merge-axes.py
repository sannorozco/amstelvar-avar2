import os

axes = {
    # "XTRA" : dict(minimum=60, maximum=902, default=561, color=(0,0,0)),
    "XTUC" : dict(minimum=72, maximum=668, default=400, color=(1,0,0)),
    "XTUR" : dict(minimum=60, maximum=902, default=561, color=(0,1,0)),
    "XTUD" : dict(minimum=76, maximum=686, default=410, color=(0,0,1)),
}

parentAxis = "XTRA"
defaultSrc = 'XTUC'

default = {
    parentAxis : {
        'minimum' : min([
            axes[a]['minimum'] + axes[defaultSrc]['default'] - axes[a]['default'] for a in axes.keys()
        ]),
        'maximum' : max([
            axes[a]['maximum'] + axes[defaultSrc]['default'] - axes[a]['default'] for a in axes.keys()
        ]),
        'default' : axes[defaultSrc]['default'],
        'color'   : (0, 0, 0),  
    }
}

axes = { **default, **axes }

size(1000, 700)
blendMode('multiply')

x, y = width()*0.57, height() - 125

d  = 155
r1 = 6
r2 = 2
sw = 1

with savedState():    
    lineDash(2, 4)
    stroke(0.5)
    line((x, 0), (x, height()))

translate(x, y)

for axisName, axis in axes.items():
    print(axisName, axis['minimum'], axis['maximum'], axis['default'])
    xMin, xMax, xDef, c = axis['minimum'], axis['maximum'], axis['default'], axis['color']

    save()
    translate(-xDef, 0)

    with savedState():    
        stroke(*c)
        strokeWidth(sw)
        line((xMin, 0), (xMax, 0))

    with savedState():    
        stroke(None)
        fontSize(12)

        for xx in [xMin, xMax, xDef]:
            with savedState():  
                stroke(*c)
                strokeWidth(sw)
                fill(None)
                oval(xx-r1, -r1, r1*2, r1*2)
                translate(xx, -25)
                # rotate(90)
                fill(*c)
                stroke(None)
                text(str(xx), (0, -4), align='center')

        steps = []
        for aName, a in axes.items():
            if aName == parentAxis or aName == axisName:
                continue
            steps += [
                a['minimum'] - a['default'] + xDef,
                a['maximum'] - a['default'] + xDef,
            ]
        fontSize(8)
        for xxx in sorted(steps):
            # if xxx >= xMax or xxx <= xMin:
            #     continue
            fill(*c)
            oval(xxx-r2, -r2, r2*2, r2*2)
            with savedState():    
                fill(*c)
                oval(xxx-r2, -r2, r2*2, r2*2)
                translate(xxx, 19)
                rotate(90)
                text(str(xxx), (0, -3), align='center')

    with savedState():    
        stroke(None)
        fill(*c)
        fontSize(24)
        text(axisName, (xDef, 30), align='center')

    restore()

    translate(0, -d)
    

folder = os.getcwd()
pdfPath = os.path.join(folder, 'merging-axes.pdf')

saveImage(pdfPath)
