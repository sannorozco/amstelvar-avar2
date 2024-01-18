AmstelvarA2
===========

Alpha version of Amstelvar with avar2 data. (work in progress)


Table of contents
-----------------

- [Current folder structure](#current-folder-structure)
- [The Fonts folder](#the-fonts-folder)
  - [ASCII Alpha](#ascii-alpha)
- [The Source folder](#the-source-folder)
  - [Parametric avar2](#parametric-avar2)
  - [Measurements file](#measurements-file)
  - [Blends file](#blends-file)
  - [Fences file](#fences-file)
- [The designspace and variable font builder](#the-designspace-and-variable-font-builder)


Current folder structure
------------------------

```
AmstelvarA2
├── Fonts/
├── Source/
├── Proofs/
├── README.md
└── OFL.txt
```

<dl>
  <dt>Fonts</dt>
  <dd>This folder contains variable font binaries for testing, in subfolders for different stages of the project.</dd>
  <dt>Source</dt>
  <dd>This folder contains various source files used to design and build the variable fonts, in subfolders for different stages of the project. Source files include UFO font sources, designspace files, Python scripts, as well as additional text files with data for glyph sets, glyph constructions, measurements, parametric blends, and fences.</dd>
  <dt>Proofs</dt>
  <dd>This folder is meant to contain font proofs. It currently contains only a PDF with screenshots comparing Amstelvar1 to AmstelvarA2. ⚠️ <em>The remaining proofs can be found in subfolders of the Fonts folder, next to the font files which they are proofing. Keeping fonts and test documents in the same folder is convenient to avoid broken links and data duplication.</em>
  </dd>
</dl>


The Fonts folder
----------------

The Fonts folder currently contains two subfolders which correspond to different development stages of the project.

```
Fonts
├── TechAlpha/
├── AsciiAlpha/
├── Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf
└── Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf
```
<dl>
  <dt>TechAlpha</dt>
  <dd>Our first (failed) attempt at building an avar2 font. ⚠️ *These files are no longer useful and can probably be archived in a branch.*</dd>
  <dt>AsciiAlpha</dt>
  <dd>Our second (successful) attempt at building an avar2 font, and current development stage. This subfolder contains the current working files (more details below).</dd>
</dl>

At the root of the Fonts folder are also the original “Amstelvar1” Roman and Italic fonts, which are used in proofs and comparisons.

### ASCII Alpha 

```
AsciiAlpha
├── AmstelvarA2-Roman_avar1.ttf
├── AmstelvarA2-Roman_avar2.ttf
├── AmstelvarA2-Roman_avar2_fences.ttf
├── AmstelvarA2-Roman_avar2_fences-wght200.ttf
├── var2-original.html
├── var2-var1.html
├── test.py
└── test2.py 
```
<dl>
  <dt>AmstelvarA2-Roman_avar1.ttf</dt>
  <dd>Variable font in avar1 format. Blended axes are created by instantiating their extrema from parametric axes, and inserting them into the designspace as sources.</dd>
  <dt>AmstelvarA2-Roman_avar2.ttf</dt>
  <dd>Variable font in avar2 format. Blended axes are created by defining mappings from parametric axes to extrema input values.</dd>
  <dt>AmstelvarA2-Roman_avar2_fences.ttf</dt>
  <dd>Attempt to build an avar2 font with “fences” to restrict the limits of parametric values at blended extrema locations. The added fences work at the default location, but not at the blended extrema.*</dd>
  <dt>AmstelvarA2-Roman_avar2_fences-wght200.ttf</dt>
  <dd>An attempt to implement fences at one blended extreme only, for testing purposes. The fences added for location <code>wght200</code> do not work as intended.*</dd></dd>
  <dt>var2-original.html</dt>
  <dd>Interactive HTML page for comparison between the ASCII Alpha avar2 font (parametric axes) and the original Amstelvar1 font (blended axes). Useful when defining and checking parametric locations of blended extrema.</dd>
  <dt>var2-var1.html</dt>
  <dd>Interactive HTML page for comparison between avar2 and avar1 versions of the ASCII Alpha font. Useful as a reference when testing the avar2 implementation.</dd>
  <dt>test.py</dt>
  <dd>Interactive DrawBot script for testing the avar2 variable font using the native macOS text engine. Produces a PDF document.</dd>
  <dt>test2.py </dt>
  <dd>An attempt to create a visualization of parametric values for changes in blended axes. <em>Not working because point indexes in the variable font are different from point indexes in the source UFOs. (double check)</em></dd>
</dl>

\* see [Implementing fences](https://github.com/googlefonts/amstelvar-avar2/issues/4)


The Sources folder
------------------

Just like the Fonts folder, the Sources folder contains subfolders which correspond to different stages of the project:

```
Source
├── TechAlpha/
├── Parametric-avar2/
└── tools/
```

<dl>
  <dt>TechAlpha</dt>
  <dd>Sources in the TechAlpha folder were derived from the original Amstelvar1 parametric sources. A measurements file in JSON format is included, as well as the original extrema sources in a subfolder. <em>With the exception of the `extrema` sources and the measurements file (which are used in the initial blends calculation, see below), all other files are no longer useful and can probably be archived in a branch.</em></dd>
  <dt>Parametric-avar2</dt>
  <dd>Sources in the Parametric-avar2 folder were recreated from a revised default. These are the current workin files.</dd>
  <dt>tools</dt>
  <dd>This folder collects various small scripts which were used during development of TechAlpha and/or Parametric-avar2 sources. Most of them are no longer needed. The most relevant ones are listed below.</dd>
</dl>

### Tools folder

A selelction of production scripts which are worth mentioning:

<dl>
  <dt>extract-measurements.py</dt>
  <dd>Extract measurements from one or more UFO sources into a dictionary. Optionally, save it into a JSON file.</dd>
  <dt>set-names-from-measurements.py</dt>
  <dd>Set file name and style name from measurements in all UFOs in a given folder. Includes a preflight mode which only prints the new names without changing the files.</dd>
  <dt>validate-locations.py</dt>
  <dd>Check if any source location is outside of the min/max bounds of its axis. This was helpful when debugging the first avar2 font builds.</dd>
</dl>

see also:

<dl>
  <dt><a href='#'>mark-components.py</a></dt>
  <dd>Mark current font glyphs containing components with different colors depending on their nesting level.</dd>
</dl>

### Parametric avar2

This folder contains two main subfolders with separate source files for Roman and Italic, and a few project-level files which are used with both Roman and Italic files.

```
Parametric-avar2
├── AmstelvarA2.roboFontSets
├── AmstelvarA2.glyphConstruction
├── build.py
├── Roman
│   └── ...
└── Italic
    └── ...
```

<dl>
  <dt>AmstelvarA2.roboFontSets</dt>
  <dd>RoboFont SmartSets file containing various sets of glyphs. Useful as UI feature when browsing complete fonts, and as a file format when writing scripts that apply only to certain sets of glyphs.</dd>
  <dt>AmstelvarA2.glyphConstruction</dt>
  <dd>GlyphConstruction file containing recipes for building various glyphs from components.</dd>
  <dt>build.py</dt>
  <dd>Python script with specialized objects for building different designspaces and variable fonts during development. See below for more information on the build process.</dd>
</dl>

### Roman sources

Folder containing source files specific to the Roman designspace and variable font.

```
Roman
├── *.ufo
├── measurements.json
├── blends.json
├── fences.json
├── features
│   └── *.fea
├── instances
│   ├── AmstelvarA2-Roman_opsz8.ufo
│   ├── AmstelvarA2-Roman_opsz144.ufo
│   ├── AmstelvarA2-Roman_wdth85.ufo
│   ├── AmstelvarA2-Roman_wdth125.ufo
│   ├── AmstelvarA2-Roman_wght200.ufo
│   └── AmstelvarA2-Roman_wght800.ufo
├── AmstelvarA2-Roman.designspace
├── AmstelvarA2-Roman_avar1.designspace
├── AmstelvarA2-Roman_avar2.designspace
├── AmstelvarA2-Roman_avar2_fences.designspace
└── AmstelvarA2-Roman_avar2_fences-wght200.designspace
```

<dl>
<dt>*.ufo</dt>
<dd>Font sources in UFO format, with files named according to their variation parameters. All sources contain all glyphs, including glyphs which do not change in relation to the default (in other words, font sources are not sparse).</dd>
<dt>measurements.json</dt>
<dd>Standalone JSON file containing definitions for various font- and glyph-level measurements. Created using the <a href='#'>Measurements tool</a> from the <a href='#'>VariableValues</a> extension. See <a href='http://gferreira.github.io/fb-variable-values/reference/measurements-format/'>Measurements format</a> for documentation of the data format.</dd>
<dt>blends.json</dt>
<dd>Standalone JSON file containing definitions of blended axes and blended sources from parametric axes. This data is used to build the avar2 designspace.</dd>
<dt>fences.json</dt>
<dd>Standalone JSON file containing definitions of min/max fence values for parametric values at blended sources. This data is used to add mappings for fences to the avar2 designspace (experimental).</dd>
<dt>features</dt>
<dd>Subfolder with files containing OpenType code which can be linked to the source fonts. <em>Currently not used when building the variable fonts.</em></dd>
<dt>instances</dt>
<dd>Subfolder containing instances generated from the parametric sources, which are used to add blended axes to the avar1 designspace. Also useful for comparison with the original Amstelvar1 sources for blended extrema.</dd>
<dt>AmstelvarA2-Roman.designspace</dt>
<dd>Basic parametric designspace for use during design and development. Also used to build instances for the avar1 designspace.</dd>
<dt>AmstelvarA2-Roman_avar1.designspace</dt>
<dd>Designspace for building avar1 variable font.* Includes the blended instances as sources for blended axes.</dd>
<dt>AmstelvarA2-Roman_avar2.designspace
<dd>Designspace for building avar2 variable font.* Includes avar2 mappings which define blended sources from parametric values.</dd>
<dt>AmstelvarA2-Roman_avar2_fences.designspace
<dd>Experimental designspace containing avar2 mappings for fences. Includes avar2 mappings of fences for the default and blended extrema.</dd>
<dt>AmstelvarA2-Roman_avar2_fences-wght200.designspace
<dd>Experimental designspace containing avar2 fence mappings for one blended extreme only (wght200). Used while debugging avar2 implementation of fences.</dd>
</dl>

\* All variable fonts are built into the `Fonts/AsciiAlpha` folder.


The designspace and variable font builder
-----------------------------------------

The different designspaces and variable fonts are built by a single `build.py` program. This program contains a core `AmstelvarDesignSpaceBuilder` object with common functionality to all AmstelvarA2 designspaces:

- reading all necessary data from the appropriate files and folders
- creating a designspace document with the parametric axes, taking min/max values from the UFO file names, and the default values by measuring the default UFO
- adding the default source
- inserting parametric sources at their appropriate locations, based on actual measurements taken from each source
- adding blended axes using data from `blends.json`, and build blended sources as instances
- saving the designspace document into the appropriate `.designspace` file
- build a variable font for the current designspace

More specific designspaces inherit from this core object, and add their own special behavior on top of it.
