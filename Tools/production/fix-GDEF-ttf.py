f = CurrentFont()

# read smart sets
# get all combininig accents 

buggyGlyphs = []

for g in f:
    for a in g.anchors:
        if a.name.startswith('_'):
            if 'comb' not in g.name:
                # if g.name not in buggyGlyphs:
                buggyGlyphs.append((g.name, a.name))

print(buggyGlyphs)