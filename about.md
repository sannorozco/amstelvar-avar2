About AmstelvarA2
=================

*introductory text about the AmstelvarA2 project (draft)*

### Differences in relation to Amstelvar

All parametric sources were redone from scratch from a new revised default. Changes include denesting components, changing point structures, fixing contour directions, adding traps, etc.

### Blending

Blending allows us to define *synthetic axes* using the parametric ones. This is achieved with `<mapping>` elements in the designspace file, which map an input in blended axes to an output in parametric axes. 

To see the advantage of this approach, compare the avar1 and avar2 versions of the AmstelvarA2 designspace: in avar1 the extrema of `opsz` `wght` `wdth` need to exist as UFO sources\*, in avar2 they don't.

\* instances of the parametric designspace, reinserted as sources.

### Measuring

In the original Amstelvar project, measuring was done with [ParamaRoundup](#). In AmstelvarA2 we are using a new measuring tool which is part of the VariableValues extension. 

we take various measurements (parameters) from all sources, and use these to create the parametric designspace and place the sources at the right locations. we also measure the original opsz wght wdth extrema to define their parametric 'recipes' (blends). 

### Technical requirements

macOS 13 is needed for avar2 fonts to work. then it's available via the OS to the browser, DrawBot, TextEdit etc.

The fonts are developed in “RoboFontra” with assistance from additional tools and scripts.

- [RoboFont 4.5b (latest beta)](http://robofont.com/)
- [Fontra (latest build)](http://fontra.xyz/)
- [VariableValues](http://github.com/gferreira/fb-variable-values)


- - -

### An introduction to the Measurements tool: what it does and how it works

The starting point is David's system of parametric axes: [http://variationsguide.typenetwork.com/]()

Starting from the default, each parametric axis modifies one 'root element' of the design – for example the vertical stem width (XOPQ), the width of the counters (XTRA), the height of lowercase (YTLC), the height of horizontal uppercase serifs (YSHU), etc.

The central idea is that typical typographic axes like *weight*, *width* and *optical size* are created by mixing these 'primary colors' by different amounts.

Each of these root elements can be measured. The values in each parametric axis correspond to actual distances measured in the fonts, in values expressed as thousands of em.

There are font-level measurements (taken from specific glyphs) which are representative of the whole font; these values are used to name the fonts and place them in the designspace.

There are also glyph-level measurements, which are local and reference the parent font-level ones. These are useful for interactive visualization during glyph design.

Measurements are defined in a JSON file, for example: [http://github.com/gferreira/amstelvar-avar2/blob/main/Sources/Roman/measurements.json]()

The data format is documented here: [http://gferreira.github.io/fb-variable-values/reference/measurements-format/]()

There is a RoboFont tool to create and edit measurements, and visualize them while working in the Glyph Editor: [http://gferreira.github.io/fb-variable-values/reference/measurements/]()

The measuring code* is also used in production scripts, for example to automatically name the fonts: [http://github.com/gferreira/amstelvar-avar2/blob/main/Scripts/production/set-names-from-measurements.py#L31]()

\* the actual measuring code is here, but it was written on top of something else and is currently not very pretty:

[http://github.com/gferreira/fb-variable-values/blob/master/code/Lib/variableValues/measurements.py]()
[http://github.com/gferreira/fb-variable-values/blob/master/code/Lib/variableValues/linkPoints.py]()
 