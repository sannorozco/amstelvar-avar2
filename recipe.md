Recipe for building the AmstelvarA2 designspace
===============================================


Ingredients
-----------

1. [AmstelvarA2 sources + measurements file](http://github.com/googlefonts/amstelvar-avar2)
2. [Amstelvar sources + measurements file](http://github.com/gferreira/amstelvar)

*What is a measurements file? See the [Measurements format specification](http://gferreira.github.io/xTools4/reference/measurements-format/).*


Steps
-----

### Amstelvar

0. [Validate default measurements of Amstelvar against AmstelvarA2.](http://github.com/gferreira/amstelvar/blob/main/validate-measurements.py)

1. [Extract measurements from all sources into a `blends.json` file.](http://github.com/gferreira/amstelvar/blob/main/extract-measurements.py)

### AmstelvarA2

0. [Set UFO names from measurements.](http://github.com/googlefonts/amstelvar-avar2/blob/main/Tools/production/set-names-from-measurements.py)

1. [Build the AmstelvarA2 designspace.](http://github.com/googlefonts/amstelvar-avar2/blob/main/Tools/build.py)

   0. Create the AmstelvarA2 `blends.json` from the Amstelvar `blends.json`.

      - read the Amstelvar `blends.json` file
      - add parametric axes which are not based on measurements (`GRAD`, `BARS`)
      - add parent blended axes for parametric axes (for example: `XOPQ` for `XOUC` `XOLC` `XOFI`)
      - save it as the AmstelvarA2 `blends.json`

   1. Create parametric designspace from source file names.

   2. Add avar2 blended axes (mappings) to the designspace using the data in `blends.json`.


Results
-------

- [AmstelvarA2-Roman_avar2.designspace](http://github.com/googlefonts/amstelvar-avar2/blob/main/Sources/Roman/AmstelvarA2-Roman_avar2.designspace)
- [AmstelvarA2-Italic_avar2.designspace](http://github.com/googlefonts/amstelvar-avar2/blob/main/Sources/Italic/AmstelvarA2-Italic_avar2.designspace)


Notes
-----

- There is a single builder for both Roman and Italic designspaces.
- There are different flavors of builder, written with object inheritance. Only the avar2 builder is currently in use. 

### Adding parent parametric axes

0. The designspace builder has:

   - a list of names of parent axes to build (ex: `XOPQ YOPQ XTRA` etc.)
   - a default axis name for each parent name (ex: `XOPQ : XOUC`)
   - a list of special axes which should have their range match another (ex: 'XQUC : XTUR')

1. The children for each parent are extracted from the measurements file.

2. For each parent axis name:

   - get the min, max and default values for all its children*
   - create a blended parent axis with the default value of the default axis as its default
   - define the min/max parent ranges based on the lowest min / highest max of all children*
   - calculate a parent value for all min/max child values
   - for each parent value, calculate the corresponding mappings in all child axes:
     - align scales at the default value
     - use the default delta (difference between parent and child* defaults) to map between axes
     - if the axis needs to match the range of another axis:
       - calculate the scale factor between the ranges of both axes
       - use scale value and default delta to map between axes

   \* ignoring special ‘match range’ axes
