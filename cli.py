import argparse
import sys
from Dandrieu_rules import *
import music21 as m21

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser('harmonize_bass',
                                     description='A commandline tool for harmonizing \
                                                  bass lines')


    parser.add_argument('input_files',
                        help='musicxml files containing a bass line',
                        type=str,
                        nargs='*',
                        default=[sys.stdin])

    parser.add_argument('-seventh',
                        help='whether to add 7th in case of fiths steps',
                        action = 'store_true')


    return parser

def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    for i, infile in enumerate(args.input_files):
        print(infile)
        inbass = m21.converter.parse(infile)
        notes, keySig, timeSig = parse_bass(inbass)
        # get the fb_line with the figures
        fbLine = dandrieu_octave_rule(notes, keySig, timeSig, args.seventh)
        fbLine.realize()

        # realizing the chords from the created figures
        fbRules = rules.Rules()  # in case you want to change the rules?
        # fbRules.partMovementLimits = [(1, 5), (2, 5), (3, 5)]
        allSols = fbLine.realize(fbRules)  # get all solutions
        print('number of solutions:')
        print(allSols.getNumSolutions())
        # allSols.generateAllRealizations().show()
        solution = allSols.generateRandomRealization()  # generate a solution
        solution.write('musicxml', f'solution_file{i+1}.musicxml') # write file with the solution
        # solution.write('musicxml', fp=f'data/Homework_assignments/Computer_Solution_Ex0{str(i+1)}.musicxml')
        print('\n')

if __name__=='__main__':
    main()