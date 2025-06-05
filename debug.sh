#!/bin/sh

source venv/bin/activate

echo "Building test fonts..."
fontmake -u Sources/Roman/AmstelvarA2-Roman_wght400-DEBUG.ufo -o ttf --keep-overlaps --output-path Fonts/AmstelvarA2-Roman_DEBUG.ttf --keep-direction --verbose WARNING --feature-writer None
fontmake -m Sources/Roman/AmstelvarA2-Roman_avar2-DEBUG.designspace -o variable --output-path Fonts/AmstelvarA2-Roman_DEBUG-DS.ttf --keep-direction --verbose WARNING --feature-writer None
echo "done!"

deactivate