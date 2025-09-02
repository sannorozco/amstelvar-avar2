Editing AmstelvarA2 with GlyphMeme
==================================

GlyphMeme moved to [xTools4]: http://gferreira.github.io/xTools4/reference/tools/variable/glyph-meme/

Introduction
------------

A “glyph meme” is a high-level description of the parameters involved in the creation of a glyph in all its variations – like a list of ingredients, and where to find them.

The GlyphMeme tool is a first experimental implementation of this idea. It uses existing data to find which sources are involved in the design of a given glyph; and it allows us to open *only this glyph from only those sources* into a temporary font for editing, and then saving them back to the source where they belong.

This approach provides two major benefits to the parametric design workflow:

1. It allows the designer to focus his attention, by showing only the relevant parametric glyph sources side-by-side and nothing else.
2. It greatly speeds up the production process by avoiding the performance bottleneck of opening multiple full font sources at once.

Using the GlyphMeme tool
------------------------

### Required data files

| data format  | what it is used for                                               |
|--------------|-------------------------------------------------------------------|
| designspace  | finding individual font sources                                   |
| smarts sets  | selecting a glyph for editing                                     |
| measurements | finding which parameters participate in the variations of a glyph |

### Usage with other tools

The [GlyphValidator] and [Measurement] tools in the latest xTools4 have been patched to make them compatible with temporary fonts created by GlyphMeme.

[GlyphValidator]: http://gferreira.github.io/xTools4/reference/tools/variable/glyph-validator/
[Measurement]: http://gferreira.github.io/xTools4/reference/tools/variable/measurements/
