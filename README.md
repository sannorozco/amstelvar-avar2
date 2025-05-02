AmstelvarA2
===========

Alpha version of Amstelvar with avar2 data. (work in progress) 


Folder structure
----------------

```
AmstelvarA2
├── Fonts/
├── Proofs/
├── Sources/
├── Tools/
├── OFL.txt
├── README.md
└── build.sh
```

<dl>
  <dt><a href='#fonts'>Fonts</a></dt>
  <dd>font binaries for testing</dd>
  <dt><a href='#proofs'>Proofs</a></dt>
  <dd>proofs of the variable fonts</dd>
  <dt><a href='#sources'>Sources</a></dt>
  <dd>various source files used to design and build the variable fonts</dd>
  <dt><a href='#tools'>Tools</a></dt>
  <dd>scripts used during production</dd>
  <dt>build.sh</dt>
  <dd>shell script to build Roman & Italic variable fonts from their source files</dd>
</dl>


Fonts
-----

```
Fonts
├── legacy/
├── AmstelvarA2-Roman_avar2.ttf
└── AmstelvarA2-Italic_avar2.ttf
```

<dl>
<dt>legacy</dt>
<dd>Subfolder containing the original avar1 version of Amstelvar for use in proofs.</dd>
<dt>AmstelvarA2-Roman_avar2.ttf, AmstelvarA2-Italic_avar2.ttf</dt>
<dd>Roman and Italic variable fonts in avar2 format</dd>
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

### Roman (+ same structure for Italic)

```
Roman
├── *.ufo
├── measurements.json
├── blends.json
├── features/*.fea
├── AmstelvarA2-Roman.glyphConstruction
├── AmstelvarA2-Roman.roboFontSets
└── AmstelvarA2-Roman_avar2.designspace
```

<dl>
<dt>*.ufo</dt>
<dd>Font sources in UFO format, with files named according to their variation parameters.</dd>
<dt>measurements.json</dt>
<dd>Standalone JSON file containing definitions for various font- and glyph-level measurements.<br/>
  Created using the <a href='http://gferreira.github.io/fb-variable-values/reference/measurements/'>Measurements tool</a> from the VariableValues RoboFont extension.<br/>
  See <a href='http://gferreira.github.io/fb-variable-values/reference/measurements-format/'>Measurements format</a> for documentation of the data format.</dd>
<dt>blends.json</dt>
<dd>Standalone JSON file containing definitions of blended axes and blended sources from parametric axes.<br/>
  Used when building the avar2 designspace.</dd>
<dt>features</dt>
<dd>Subfolder with .fea files containing OpenType feature code used by the source fonts.</dd>
<dt>AmstelvarA2-Roman.glyphConstruction</dt>
<dd><a href='https://github.com/typemytype/GlyphConstruction'>GlyphConstruction</a> file containing instructions for building glyphs from components.</dd>
<dt>AmstelvarA2-Roman.roboFontSets</dt>
<dd><a href='http://robofont.com/documentation/topics/smartsets/'>SmartSets</a> file containing various sets of glyphs.</dd>
<dt>AmstelvarA2-Roman_avar2.designspace
<dd>Designspace for building the avar2 variable font.</dd>
</dl>


Tools
-----

```
Tools
├── blending/
├── production/
├── proofing/
└── build-designspace.py
```

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
2. `wght` Weight
3. `wdth` Width
4. `XTSP` Proportional spacing

### Parent parametric axes

1. `XOPQ` General x opaque
2. `YOPQ` General y opaque
3. `XTRA` General x transparent
4. `XSHA` General x horizontal serifs
5. `YSHA` General y horizontal serif
6. `XSVA` General x vertical serifs
7. `YSVA` General y vertical serifs
8. `XVAA` General vertical serif angle
9. `YHAA` General horizontal serif angle
10. `XTEQ` X internal curvature
11. `YTEQ` Y internal curvature

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
50. `XQUC` X internal curvature uppercase
51. `XQLC` X internal curvature lowercase
52. `XQFI` X internal curvature figures
53. `YQUC` Y internal curvature uppercase
54. `YQLC` Y internal curvature lowercase
55. `YQFI` Y internal curvature figures
