Overview of AmstelvarA2 production scripts
==========================================


### set-names-from-measurements.py

Set file name and style name from measurements in all UFOs in a given folder.

Includes a preflight mode which only prints the new names without changing the files.

### copy-glyphs.py

Copy glyphs from the default font to selected sources.

### build-glyphs.py

Build glyphs from glyph constructions in the selected sources.

### validate-locations.py

Check if source locations are within the allowed min/max bounds for each axis.

Helpful when debugging calculated blend values in relation to the current parametric axes.

### mark-components.py

Mark glyphs in the current font containing components with different colors depending on their components' nesting level.


...