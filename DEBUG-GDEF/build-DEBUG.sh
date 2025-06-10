#!/bin/sh

source ../venv/bin/activate

echo "Building test fonts..."

# build static ttfs
fontmake -u wght400.ufo -o ttf --keep-overlaps --output-path static_feaWriter-ON.ttf                          --keep-direction --verbose WARNING
fontmake -u wght400.ufo -o ttf --keep-overlaps --output-path static_feaWriter-OFF.ttf   --feature-writer None --keep-direction --verbose WARNING # --no-generate-GDEF

# build variable ttfs
fontmake -m DEBUG-GDEF.designspace -o variable --output-path variable_feaWriter-ON.ttf                        --keep-direction --verbose WARNING
fontmake -m DEBUG-GDEF.designspace -o variable --output-path variable_feaWriter-OFF.ttf --feature-writer None --keep-direction --verbose WARNING # --no-generate-GDEF 

echo "done!"

deactivate