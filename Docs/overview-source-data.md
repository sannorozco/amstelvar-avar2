Overview of the AmstelvarA2 source data
=======================================


```
AmstelvarA2
├── Docs/
├── Fonts/
├── Proofs/
├── Sources/
│   ├── Italic/
│   └── Roman/
│       ├── features/
│       │   └── .fea
│       ├── .ufo
│       ├── .designspace
│       ├── .roboFontSets
│       ├── .glyphConstruction
│       └── .measurements
└── Tools/
    └── *.py
```


Data formats
------------

| data type          | file format          | description                                                                                 |
|--------------------|----------------------|---------------------------------------------------------------------------------------------|
| font sources       | `.ufo`               | Font sources in UFO format, with files named according to their variation parameters.       |
| OpenType features  | `.fea`               | Files containing OpenType feature code used by the source fonts.                            |
| designspace        | `.designspace`       | Designspace for building the avar2 variable font.                                           |
| measurements       | `.measurements`      | Standalone JSON file containing definitions for various font- and glyph-level measurements. |
| smart sets         | `.roboFontSets`      | SmartSets file containing various collections of glyphs.                                    |
| glyph construction | `.glyphConstruction` | GlyphConstruction file containing recipes for building glyphs from components.              |


Notes
-----

1. Measurement files are created using the [Measurements tool]. See [Measurements format] for documentation of the `.measurements` data format.


[GlyphConstruction]: http://github.com/typemytype/GlyphConstruction
[SmartSets]: http://robofont.com/documentation/topics/smartsets/
[Measurements tool]: #
[Measurements format]: #
