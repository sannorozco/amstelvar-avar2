AmstelvarA2
===========

Alpha version of Amstelvar with avar2 data. (work in progress)


Folder structure
----------------

```
AmstelvarA2
├── Fonts/
├── Proofs/
├── Tools/
├── Sources/
├── README.md
└── OFL.txt
```

<dl>
  <dt><a href='#fonts'>Fonts</a></dt>
  <dd>font binaries for testing</dd>
  <dt><a href='#proofs'>Proofs</a></dt>
  <dd>proofs of the variable fonts</dd>
  <dt><a href='#tools'>Tools</a></dt>
  <dd>scripts used during production</dd>
  <dt><a href='#sources'>Sources</a></dt>
  <dd>various source files used to design and build the variable fonts</dd>
</dl>


Fonts
-----

```
Fonts
├── AmstelvarA2-Roman_avar1.ttf
└── AmstelvarA2-Roman_avar2.ttf
```

<dl>
  <dt>AmstelvarA2-Roman_avar1.ttf</dt>
  <dd>Variable font in avar1 format.<br/>
    Blended axes are created by instantiating their extrema from parametric axes, and inserting them into the designspace as sources.</dd>
  <dt>AmstelvarA2-Roman_avar2.ttf</dt>
  <dd>Variable font in avar2 format.<br/>
    Blended axes are created by defining mappings from parametric axes to extrema input values.</dd>
</dl>


Proofs
------

```
Proofs
├── HTML/
├── PDF/
└── fontra-test-strings.txt
```

<dl>
  <!--
  <dt>avar2-original_blends.html</dt>
  <dd>Interactive HTML page for comparison between AmstelvarA2 avar2 (parametric axes) and the original Amstelvar (opsz wght wdth).<br/>
    Useful when defining and checking parametric locations of blended extrema against their avar2 blends.</dd>
  <dt>avar2-original_compare.html</dt>
  <dd>Interactive HTML page for comparison between AmstelvarA2 avar2 and the original Amstelvar at the same location (opsz wght wdth).<br/>
    Useful to compare the new avar2 blends to the original avar font.</dd>
  <dt>avar2-avar1.html</dt>
  <dd>Interactive HTML page for comparison between avar2 and avar1 versions of AmstelvarA2.<br/>
    Useful as a reference when testing the avar2 implementation.</dd>
  <dt>avar2-test.py</dt>
  <dd>DrawBot script for testing the avar2 variable font interactively using the native macOS text engine.<br/>
    Produces a PDF document.</dd>
  -->
  <dt>HTML</dt>
  <dd>Interactive proofs in HTML/CSS/JS format.</dd>
  <dt>PDF</dt>
  <dd>Static proofs in PDF format.</dd>
  <dt>fontra-test-strings.txt</dt>
  <dd>Test text strings for previewing glyph sets in Fontra.</dd>
</dl>


Sources
-------

This folder contains two subfolders with separate files for Roman and Italic, and project-level files which are used by both styles.

```
Sources
├── Italic/
├── Roman/
└── AmstelvarA2.roboFontSets
```

<dl>
  <dt>AmstelvarA2.roboFontSets</dt>
  <dd><a href='http://robofont.com/documentation/topics/smartsets/'>SmartSets</a> file containing various sets of glyphs.<br/>
    Useful as UI feature when browsing complete fonts, and as a data format when writing scripts that apply only to certain sets of glyphs.</dd>
</dl>

### Roman (+ same structure for Italic)

```
Roman
├── *.ufo
├── measurements.json
├── blends.json
├── fences.json
├── features/*.fea
├── instances/*.ufo
├── AmstelvarA2-Roman.glyphConstruction
├── AmstelvarA2-Roman.designspace
├── AmstelvarA2-Roman_avar1.designspace
└── AmstelvarA2-Roman_avar2.designspace
```

<dl>
<dt>*.ufo</dt>
<dd>Font sources in UFO format, with files named according to their variation parameters.<br/>
  All sources contain all glyphs, including glyphs which do not change in relation to the default (sources are not sparse).</dd>
<dt>measurements.json</dt>
<dd>Standalone JSON file containing definitions for various font- and glyph-level measurements.<br/>
  Created using the <a href='http://gferreira.github.io/fb-variable-values/reference/measurements/'>Measurements tool</a> from the VariableValues RoboFont extension.<br/>
  See <a href='http://gferreira.github.io/fb-variable-values/reference/measurements-format/'>Measurements format</a> for documentation of the data format.</dd>
<dt>blends.json</dt>
<dd>Standalone JSON file containing definitions of blended axes and blended sources from parametric axes.<br/>
  This data is used to build the avar2 designspace.</dd>
<dt>fences.json</dt>
<dd>Standalone JSON file containing definitions of min/max fence values for parametric values at blended sources.<br/>
  This data is used to add mappings for fences to the avar2 designspace. (experimental)</dd>
<dt>features</dt>
<dd>Subfolder with files containing OpenType code which can be linked to the source fonts.<br/>
  <em>Currently not used when building the variable fonts.</em></dd>
<dt>instances</dt>
<dd>Subfolder containing instances generated from the parametric sources, used to add blended axes to the avar1 designspace.<br/>
  Also useful for comparison with the original Amstelvar1 sources for blended extrema.</dd>
<dt>AmstelvarA2-Roman.glyphConstruction</dt>
<dd><a href='https://github.com/typemytype/GlyphConstruction'>GlyphConstruction</a> file containing instructions for building glyphs from components.</dd>
<dt>AmstelvarA2-Roman.designspace</dt>
<dd>Basic parametric designspace for use during design and development.<br/>
  Also used to build instances for the avar1 designspace.</dd>
<dt>AmstelvarA2-Roman_avar1.designspace</dt>
<dd>Designspace for building avar1 variable font.<br/>
  Includes the blended instances as sources for blended axes.</dd>
<dt>AmstelvarA2-Roman_avar2.designspace
<dd>Designspace for building avar2 variable font.<br/>
  Includes avar2 mappings which define blended sources from parametric values.</dd>
</dl>


Tools
-----

```
Tools
├── production/*.py
└── build.py
```

### Build script

The different designspaces and variable fonts are built by a single `build.py` script. The code is written around a core `AmstelvarDesignSpaceBuilder` object which provides common functionality to all AmstelvarA2 designspaces:

- reading all necessary data from the appropriate files and folders
- creating a designspace document with the parametric axes, taking min/max values from the UFO file names, and default values by measuring the default UFO
- inserting parametric sources at their appropriate locations, based on actual measurements taken from each source
- adding blended axes using data from the `blends.json` file, and building blended sources as instances
- saving the designspace document into a `.designspace` file
- building a variable font for the current designspace

More specific designspaces inherit from this core object, and add their own special behavior on top of it.

### Production scripts

A subfolder containing various scripts used during development. The most relevant ones are listed below.

<dl>
  <dt>set-names-from-measurements.py</dt>
  <dd>Set file name and style name from measurements in all UFOs in a given folder.<br/>
    Includes a preflight mode which only prints the new names without changing the files.</dd>
  <dt>copy-glyphs.py</dt>
  <dd>Copy glyphs from the default font to selected sources.</dd>
  <dt>build-glyphs.py</dt>
  <dd>Build glyphs from glyph constructions in the selected sources.</dd>
  <dt>validate-locations.py</dt>
  <dd>Check if source locations are within the allowed min/max bounds for each axis.<br/>
    Helpful when debugging calculated blend values in relation to the current parametric axes.</dd>
  <dt>mark-components.py</dt>
  <dd>Mark glyphs in the current font containing components with different colors depending on their components' nesting level.</dd>
</dl>


Blending
--------

The appropriate values for blending `opsz` `wght` `wdth` from parametric axes are produced on a [separate repository](http://github.com/gferreira/amstelvar) which is a fork of the original Amstelvar source. [The naming of UFO files was adjusted for easier parameter parsing (using underscores to separate parameters instead of hyphens), and all unnecessary files were deleted.]

A separate measurements file was added for Amstelvar, with the same parameters used for measuring AmstelvarA2. This file is needed because the contour structures of the two versions are different, and in most measurements different point indexes must be used.

### Extracting measurements

Using this separate measurements file, the original Amstelvar sources are then measured to produce the `blends.json` file which is used by the AmstelvarA2 designspace builder.


Variation axes in AmstelvarA2
-----------------------------

### Typographic axes

1. `opsz` Optical size
1. `wght` Weight
1. `wdth` Width
1. `XTSP` Proportional spacing

### Parent axes (parametric)

1. `XOPQ` General x opaque
2. `YOPQ` General y opaque
3. `XTRA` General x transparent
4. `XSHA` General x horizontal serifs
5. `YSHA` General y horizontal serif
6. `XSVA` General x vertical serifs
7. `YSVA` General y vertical serifs
8. `XVAA` General vertical serif angle
9. `YHAA` General horizontal serif angle

### Parametric axes

1. `XOUC` X stem uppercase
2. `XOLC` X stem lowercase
3. `XOFI` X stem figures
4. `YOUC` Y stem uppercase
5. `YOLC` Y stem lowercase
6. `YOFI` Y stem figures
7. `XTUC` X transparent uppercase
8. `XTUR` X transparent uppercase rounds
9. `XTUD` X transparent uppercase diagonals
10. `XTLC` X transparent lowercase
11. `XTLR` X transparent lowercase rounds
12. `XTLD` X transparent lowercase diagonals
13. `XTFI` X transparent figures
14. `YTUC` Y transparent uppercase
15. `YTLC` Y transparent lowercase
16. `YTAS` Y transparent ascender
17. `YTDE` Y transparent descender
18. `YTFI` Y transparent figures
19. `XSHU` X horizontal serif uppercase
20. `YSHU` Y horizontal serif uppercase
21. `XSVU` X vertical serif uppercase
22. `YSVU` Y vertical serif uppercase
23. `XSHL` X horizontal serif lowercase
24. `YSHL` Y horizontal serif lowercase
25. `XSVL` X vertical serif lowercase
26. `YSVL` Y vertical serif lowercase
27. `XSHF` X horizontal serif figures
28. `YSHF` Y horizontal serif figures
29. `XSVF` X vertical serif figures
30. `YSVF` Y vertical serif figures
31. `XVAU` Uppercase vertical serif angle
32. `YHAU` Uppercase horizontal serif angle
33. `XVAL` Lowercase vertical serif angle
34. `YHAL` Lowercase horizontal serif angle
35. `XVAF` Figures vertical serif angle
36. `YHAF` Figures horizontal serif angle
37. `XTTW` Trap width
38. `YTTL` Trap length
39. `YTOS` General y overshoot
40. `XUCS` X sidebearing uppercase straights
41. `XUCR` X sidebearing uppercase rounds
42. `XUCD` X sidebearing uppercase diagonals
43. `XLCS` X sidebearing lowercase rounds
44. `XLCR` X sidebearing lowercase straights
45. `XLCD` X sidebearing lowercase diagonals
46. `XFIR` X sidebearing figure 0
47. `WDSP` Word space width
48. `XDOT` Dot width
49. `BARS` 
50. `XTEQ` 
51. `YTEQ` 

