#!/bin/sh

fonttools varLib.instancer Fonts/AmstelvarA2-Roman_avar2.ttf wght=700 -o Fonts/AmstelvarA2-Roman_wght700.ttf --static
fonttools varLib.instancer Fonts/AmstelvarA2-Roman_avar2.ttf wght=300 wdth=50 -o Fonts/AmstelvarA2-Roman_wght300_wdth50.ttf --static
fonttools varLib.instancer Fonts/AmstelvarA2-Roman_avar2.ttf wght=200 wdth=125 opsz=144 -o Fonts/AmstelvarA2-Roman_wght200_wdth125_opsz144.ttf --static
fonttools varLib.instancer Fonts/AmstelvarA2-Roman_avar2.ttf XTLC=420 -o Fonts/AmstelvarA2-Roman_XTLC420.ttf --static
fonttools varLib.instancer Fonts/AmstelvarA2-Roman_avar2.ttf XOUC=20 XOLC=20 -o Fonts/AmstelvarA2-Roman_XOUC20_XOLC20.ttf --static
