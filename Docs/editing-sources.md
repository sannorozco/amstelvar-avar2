Editing AmstelvarA2 sources
===========================


Requirements
------------

### Tools

- Git
- Python3
- [Fontra](http://fontra.xyz/)
- [RoboFont 4.6b (latest beta)](http://beta.robofont.com/)
- [Mechanic](http://robofontmechanic.com/)
- DrawBot extension (install via Mechanic)
- [xTools4](http://gferreira.github.io/xTools4/how-tos/installing-xtools4)

### Sources

- [AmstelvarA2](http://github.com/gferreira2/amstelvar-avar2/)
- [Amstelvar](http://github.com/gferreira/amstelvar)


Source formats
--------------

| description        | file format          |
|--------------------|----------------------|
| font sources       | `.ufo`               |
| designspace        | `.designspace`       |
| measurements       | `.measurements`      |
| smart sets         | `.roboFontSets`      |
| glyph construction | `.glyphConstruction` |

### Folder structure

```
AmstelvarA2
├── Docs/
├── Fonts/
├── Proofs/
├── Sources/
│   ├── Italic/
│   └── Roman/
│       ├── .ufo
│       ├── .designspace
│       ├── .roboFontSets
│       ├── .glyphConstruction
│       └── .measurements
└── Tools/
    └── *.py
```


Toolkit overview
----------------

“Expert tools” – [Variable font production with xTools4](http://gist.github.com/gferreira2/7219f99019d83b44512d315ef7bbc951)

- Measurements
- GlyphValidator
- VarGlyphAssistant
- VarFontAssistant
- [TempEdit](http://www.hipertipo.com/log/2021-05-07-elementar-ferramentas/#tempedit)
- [GlyphMeme](http://github.com/googlefonts/amstelvar-avar2/blob/main/Tools/GlyphMeme.py)

### Workflow

- Fontra overview
- HTML proofer (comparison with original Amstelvar)
- build-designspace.py + [recipe](http://github.com/gferreira2/amstelvar-avar2/blob/main/Docs/recipe-designspace.md)
- overview of PDF proofs


Process
-------

???
