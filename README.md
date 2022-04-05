## Harmonizing a Bass line 18th century style

This module an attempts to automatically harmonize a bass line after the rules as specified by the French composer Jean-Francois Dandrieu (For a Wikipedia article about the composer see [here](https://en.wikipedia.org/wiki/Jean-Fran%C3%A7ois_Dandrieu), the original document specifying the harmonization rules can be found [here](https://imslp.org/wiki/Principes_de_l%27Acompagnement_du_Clavecin_(Dandrieu%2C_Jean-Fran%C3%A7ois)). To use it clone this repository and run \
`python cli.py yourfile.musicxml` \
where `yourfile.musicxml` is a score with just a single bass line. In order for the program to find the desired key, the last note needs to be the root. You can provide as many input files as you want. The program will write the solutions to files called `solution_yourfile_i.musicxml`, where i is a counter for the scipts that have been given as arguments.

#### How it works:
The program first parses the bassline and applies the figures as they are specified by Dandrieu to the score. It then uses the music21 package to realize the chords according to the figures.
