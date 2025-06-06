#!/bin/sh

source ../venv/bin/activate

echo "Building test fonts..."

# build static ttfs
fontmake -u AmstelvarA2-Roman_wght400-DEBUG.ufo -o ttf --keep-overlaps --output-path static_feaWriter-ON.ttf                        --keep-direction --verbose WARNING
fontmake -u AmstelvarA2-Roman_wght400-DEBUG.ufo -o ttf --keep-overlaps --output-path static_feaWriter-OFF.ttf --feature-writer None --keep-direction --verbose WARNING

# build variable ttfs
fontmake -m AmstelvarA2-Roman_avar2-DEBUG.designspace -o variable --output-path variable_feaWriter-ON.ttf                           --keep-direction --verbose WARNING
fontmake -m AmstelvarA2-Roman_avar2-DEBUG.designspace -o variable --output-path variable_feaWriter-OFF.ttf --feature-writer None    --keep-direction --verbose WARNING

echo "done!"

deactivate