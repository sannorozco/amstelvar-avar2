Overview of the AmstelvarA2 repository
======================================


Folder structure
----------------

```
AmstelvarA2
├── Fonts/
├── Proofs/
├── Sources/
├── Tools/
├── OFL.txt
├── README.md
└── build.sh
```


Fonts
-----

```
Fonts
├── legacy/
├── AmstelvarA2-Roman_avar2.ttf
└── AmstelvarA2-Italic_avar2.ttf
```

The `Fonts` folder contains Roman and Italic variable fonts in avar2 format.

The `legacy` subfolder contains the original avar1 version of Amstelvar for use in proofs.


Proofs
------

```
Proofs
├── HTML/
├── PDF/
└── fontra-test-strings.txt
```

The `HTML` subfolder contains Interactive proofs in HTML/CSS/JS format.

The `PDF` subfolder contains static proofs in PDF format.

The text file `fontra-test-strings.txt` contains test strings for previewing glyph sets in Fontra.


Sources
-------

The `Sources` folder contains two subfolders with separate files for Roman and Italic, and project-level files which are used by both styles.

```
Sources
├── Italic/
└── Roman/
```


Tools
-----

```
Tools
├── blending/
├── production/
├── proofing/
└── build-designspace.py
```

The `production` subfolder contains various scripts used during the development of the fonts.
