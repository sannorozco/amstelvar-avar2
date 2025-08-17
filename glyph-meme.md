Editing parametric variable fonts with GlyphMeme
================================================


Introduction
------------

A “glyph meme” is a high-level description of the parameters involved in the design of a glyph in all its variations – like a list of ingredients, and where to find them.

The GlyphMeme tool is a first experimental implementation of this idea. It uses existing data formats to find which sources are involved in the design of a given glyph, and allows us to open *only this glyph from only those sources* into a temporary font for editing, and then saving it back to the source where it belongs.

This approach provides two major benefits to the parametric design workflow:

1. It allows the designer to focus his attention by showing only the relevant parametric glyph sources side-by-side.

2. It greatly speeds up the production process by avoiding the performance bottleneck of opening multiple full font sources at once.


Required input data
-------------------

The GlyphMeme tool needs the following types of font data as input:

A `.designspace` file describing the parametric variation space.
— used to find individual font sources

A `.roboFontSets` file containing various groupings of glyphs.
— select a glyph for editing

A measurements file containing definitions of where to measure each parameter.
— find which parameters are used to produce a glyph

<!--
A `.glyphConstruction` file describing how to assemble glyphs from components.
— find which glyphs are used to assemble a glyph
-->

Concepts
--------

The GlyphMeme tool uses the following concepts from [TempEdit]:

### temp font

A temp font is a font that is never saved to disk. It is used as a temporary editing workspace for glyphs from various sources.

### temp font mode

There are 3 different modes for temp fonts, depending on how the glyphs are imported:

1. layers – glyphs are imported as layers of a single glyph in a single font
2. glyphs – glyphs are imported as multiple glyphs in a single font
3. fonts  – glyphs are imported as multiple fonts





