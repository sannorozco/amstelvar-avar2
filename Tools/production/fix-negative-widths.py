import os, glob

instancesFolder = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Sources/Roman/instances'

instances = glob.glob(f'{instancesFolder}/*.ufo')

for instance in instances:
    f = OpenFont(instance, showInterface=False)
    for g in f:
        if g.width < 0:
            print(f.info.styleName, g.name, g.width)
            g.width = 0
    f.save()
    f.close()
