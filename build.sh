#!/bin/sh

echo "Building variable fonts..."

echo "  Building AmstelvarA2 Roman..."
fontmake -m Sources/Roman/AmstelvarA2-Roman_avar2.designspace -o variable --output-path Fonts/AmstelvarA2-Roman_avar2.ttf --feature-writer None --keep-direction --verbose DEBUG

# echo "  Building AmstelvarA2 Italic..."
# fontmake -m Sources/Italic/AmstelvarA2-Italic_avar2.designspace -o variable --output-path Fonts/AmstelvarA2-Italic_avar2.ttf --feature-writer None --keep-direction --verbose WARNING

echo "done!"
