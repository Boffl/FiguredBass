### Harmonizing a Bass line 18th century style

This module an attempts to automatically harmonize a bass line after the rules as specified by the French composer Jean-Francois Dandrieu (see [here](https://en.wikipedia.org/wiki/Jean-Fran%C3%A7ois_Dandrieu)). To use it clone this repository and run \
`python cli.py yourfile.musicxml` \
where `yourfile.musicxml` is a score with just a single bass line. In order for the program to find the desired key, the last note needs to be the root. You can provide as many input files as you want. The program will write the solutions to files called `solution_yourfile_i.musicxml`, where i is a counter for the scipts that have been given as arguments.
