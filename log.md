AmstelvarA2 Log
===============

Phase III
---------

- disabled ASCII subsetting; variable fonts now contain the full glyph set
- expanded range for parametric axes XTRA XUCS XSHF YSVF (some issues with XTRA max)
- fixed vertical serifs XSV* YSV* min (parameters must remain independent)
- separated GlyphConstruction files for Roman and Italic
- made another attempt at implementing fences (based on Santiago's RobotoFlex example)
- small update to VariableValues extension

### Italic

- added measurements for Italic sources
- added traps to V W X Y v w x y Delta Lambda etc.
- added overlaps to Q
- rebuilding all composed glyphs
- starting to design key glyphs

### Greek & Cyrillic

- used Pe shape for Pi + made Pe component of Pi
- reviewed and fixed Greek YOPQ XOPQ min (WIP)
