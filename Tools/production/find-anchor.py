# menuTitle: find all anchors with a given name

anchorName = '_yu_dash'

f = CurrentFont()
for g in f:
    for a in g.anchors:
        if a.name == anchorName:
            print(g.name)
            