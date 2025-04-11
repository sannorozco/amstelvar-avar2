# menuTitle: visualize the combination of parametric axes into a blended parent axis

import os

# --------
# settings
# --------

parametricAxes = {
    "XTUC" : dict(minimum=72, maximum=668, default=400, color=(1,0,0)),
    "XTUR" : dict(minimum=60, maximum=902, default=561, color=(0,1,0)),
    "XTUD" : dict(minimum=76, maximum=686, default=410, color=(0,0,1)),
}

parentAxisName = "XTRA" # name of the parent parametric axis
defaultSrc     = 'XTUC' # source parametric axis for the default parent value

w, h = 930, 429
d  = 101
r1 = 4
r2 = 2
sw = 1
fs1 = 14
fs2 = 7
fs3 = 24

drawRanges   = True
drawMappings = True
savePDF      = True

# ----------------
# calculate parent
# ----------------

# get parent ranges and default from parametric axes
parentAxis = {
    parentAxisName : {
        'default' : parametricAxes[defaultSrc]['default'],
        'minimum' : min([
            parametricAxes[a]['minimum'] + parametricAxes[defaultSrc]['default'] - parametricAxes[a]['default'] 
            for a in parametricAxes.keys()
        ]),
        'maximum' : max([
            parametricAxes[a]['maximum'] + parametricAxes[defaultSrc]['default'] - parametricAxes[a]['default'] 
            for a in parametricAxes.keys()
        ]),
        'color'   : (0, 0, 0),  
    }
}

axes = { **parentAxis, **parametricAxes }

# ------------------
# draw visualization
# ------------------

size(w, h)
blendMode('multiply')

x, y = width()*0.585, height() - 65

translate(x, y)

for i, axisName in enumerate(axes.keys()):
    axis = axes[axisName]
    xMin, xMax, xDef, c = axis['minimum'], axis['maximum'], axis['default'], axis['color']
    # print(axisName, xMin, xDef, xMax)

    save()
    translate(-xDef, 0)

    # draw mapping guides
    with savedState():
        stroke(0.925)
        if i == 0:
            line((xDef, -y), (xDef, height()))
        else:
            if drawMappings:
                line((xMin, -y), (xMin, height()))
                line((xMax, -y), (xMax, height()))

    with savedState():    
        stroke(*c)
        strokeWidth(sw)
        line((xMin, 0), (xMax, 0))

    with savedState():    
        stroke(None)
        fontSize(fs1)

        # draw minimum / maximum / default
        if drawRanges:
            for xx in [xMin, xMax, xDef]:
                with savedState():  
                    stroke(*c)
                    strokeWidth(sw)
                    fill(None)
                    oval(xx-r1, -r1, r1*2, r1*2)
                    translate(xx, -25)
                    fill(*c)
                    stroke(None)
                    text(str(xx), (0, 2), align='center')

        # calculate mapping steps
        if drawMappings:
            steps = []
            for aName, a in axes.items():
                if aName == parentAxis:
                    continue
                steps += [
                    a['minimum'] - a['default'] + xDef,
                    a['maximum'] - a['default'] + xDef,
                    # xDef,
                ]
            fontSize(fs2)

            # draw mapping steps
            for xxx in sorted(steps):
                ### if xxx <= xMin or xxx >= xMax: CLAMP to axis min/max
                fill(*c)
                oval(xxx-r2, -r2, r2*2, r2*2)
                with savedState():    
                    fill(*c)
                    oval(xxx-r2, -r2, r2*2, r2*2)
                    translate(xxx, 18)
                    rotate(90)
                    text(str(xxx), (0, -3), align='center')
    
    # draw axis name
    with savedState():    
        stroke(None)
        fill(*c)
        fontSize(fs3)
        text(axisName, (xDef, 15), align='center')

    restore()
    translate(0, -d)
    
# save to PDF file
if savePDF:
    folder = os.getcwd()
    pdfPath = os.path.join(folder, 'merging-axes.pdf')
    saveImage(pdfPath)
