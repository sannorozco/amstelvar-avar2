Blending AmstelvarA2 with parametric measurements
=================================================

The appropriate values for blending `opsz` `wght` `wdth` from parametric axes are produced on a [separate repository][Amstelvar] which is a fork of the original Amstelvar source. [The naming of UFO files was adjusted for easier parameter parsing (using underscores to separate parameters instead of hyphens), and all unnecessary files were deleted.]

A separate measurements file was added for Amstelvar, with the same parameters used for measuring AmstelvarA2. This file is needed because the contour structures of the two versions are different, and in most measurements different point indexes must be used.

Extracting measurements
-----------------------

Using this separate measurements file, the original Amstelvar sources are then measured to produce the `blends.json` file which is used by the AmstelvarA2 designspace builder.

[Amstelvar]: http://github.com/gferreira/amstelvar