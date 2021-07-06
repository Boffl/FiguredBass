import music21 as m21
from typing import List
from music21.figuredBass import rules
from music21.figuredBass import examples
from music21.figuredBass import realizer


def dandrieu_octave_rule(notes: List[m21.note.Note], keySig: m21.key.Key,
                         timeSig: m21.meter.TimeSignature) -> m21.figuredBass.realizer.FiguredBassLine:
    """ applies Dandrieus Rules to harmonize a bass line.
    :ivar: a list of bass notes as well as key and time signature
    :return: a ~music21.figuredBass.realizer.FiguredBassLine object"""
    # keySig = m21.key.Key(key, mode)
    fbLine = realizer.FiguredBassLine(keySig, timeSig)  # create a fbLine object

    if keySig.mode == 'major':
        dandrieu_rules = {
            1: '', 5: '',  # the naturel (empty string defaults to 3,5)
            (2, 3): '6,4,3', (2, 1): '6,4,3', (6, 5): '#6,4,3',  # petite sixte
            3: '6', (6, 7): '6', (7, 6): '6',  # sixte simple / sixte doublee
            (4, 5): '6,5', # quinte et sixte
            (7, 1): '5,6,3', # fausse quinte
            (4, 3): '4,6,2',  # l'accord de tritone
            (6, 4): '3,6,4', # Terztausch
            
              }


    elif keySig.mode == 'minor':
        # TODO: implement minor
        dandrieu_rules = {
            1: '', 5: '#3,5,8',
            (2, 3): '#6,4,3', (6, 5): '6,4,3', (2, 1): '#6,4,3',
            3: '6', (6, 7): '6', (7, 6): '6',
            (4, 5): '6,5',
            (7, 1): '5,6,3',
            (4, 3): '#4,2,6',
            (6, 4): '3,6,4',  # Terztausch
        }

    else:
        # TODO:
        # raise an error, quit the program
        print('only major and minor are supported modes')

    # iterating over the bass notes:
    for i, bass_note in enumerate(notes):
        # print(len([x for x in bass.recurse().notes]))
        # solve the try except with a while loop, would be more elegant!!!!

        try:  # since the last note wont have a note at i+1
            following_note = notes[i + 1]
            this_note_degree = keySig.getScaleDegreeAndAccidentalFromPitch(bass_note.pitch)[0]
            # have to use the long one, getting also the accidental, because of melodic minor...
            following_note_degree = keySig.getScaleDegreeAndAccidentalFromPitch(following_note.pitch)[0]

            if this_note_degree in dandrieu_rules:
                fbLine.addElement(bass_note, dandrieu_rules[this_note_degree])

            elif (this_note_degree, following_note_degree) in dandrieu_rules:
                fbLine.addElement(bass_note, dandrieu_rules[(this_note_degree, following_note_degree)])

        except IndexError:
            fbLine.addElement(bass_note)  # no notation added, always end on the naturel


    return fbLine


if __name__ == '__main__':
    # create examples:
    # scales
    c_major = "C1 D E F G A B c c B A G F E D C"
    d_major = "D1 E F# G A B c# d d c# B A G F# E D"
    d_minor = 'D1 E F G A B c# d d c B- A G F E D'
    c_minor = 'C1 D E- F G A B c c B- A- G F E- D C'

    # special movements:
    terztausch = 'A1 F G GG C'  # Dandrieu page 20, example in c major
    terztausch_moll = 'A-1 F GG C'
    #mstr_minor = 'C1 D E- F G A B c c B- A- G F E- D C'
    bass = m21.converter.parse('tinynotation: 4/4 ' + terztausch_moll)
    # bass = m21.converter.parse('c_major.musicxml')

    # get the list of notes
    notes = bass.recurse().notes
    # set parameters manually
    keySig = m21.key.Key('C', 'minor')
    timeSig = m21.meter.TimeSignature('4/4')

    # get the fb_line with the figures
    fbLine = dandrieu_octave_rule(notes, keySig, timeSig)
    fbLine.realize()

    # realizing the chords from the created figures
    fbRules = rules.Rules()  # in case you want to change the rules?
    fbRules.partMovementLimits = [(1, 5), (2, 5), (3, 5)]
    allSols = fbLine.realize(fbRules)  # get all solutions
    print(allSols.getNumSolutions())
    # allSols.generateAllRealizations().show()
    allSols.generateRandomRealization().show()  # generate a solution

