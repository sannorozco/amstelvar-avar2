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
   1. Create parametric designspace from source file names.
   2. Read the Amstelvar `blends.json` file;  
      add parametric axes which are not based on measurements (`GRAD`, `BARS`);  
      save it as the AmstelvarA2 `blends.json`.
   3. Create avar2 blended axes from AmstelvarA2 `blends.json`.
   4. Create ‘parent’ blended axes for parametric axes, for example `XOPQ` for `XOUC` `XOLC` `XOFI` etc.


Results
-------

- [AmstelvarA2-Roman_avar2.designspace](http://github.com/googlefonts/amstelvar-avar2/blob/main/Sources/Roman/AmstelvarA2-Roman_avar2.designspace)
- [AmstelvarA2-Italic_avar2.designspace](http://github.com/googlefonts/amstelvar-avar2/blob/main/Sources/Italic/AmstelvarA2-Italic_avar2.designspace)


Notes
-----

- There is a single builder for both Roman and Italic designspaces.
- There are different flavors of builder, written with object inheritance. Only the avar2 builder is currently in use. 
