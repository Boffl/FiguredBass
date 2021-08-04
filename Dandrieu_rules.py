import music21 as m21
from typing import List
from music21.figuredBass import rules
from music21.figuredBass import examples
from music21.figuredBass import realizer
from collections import deque


def pairwise(iterable):
    '''for pairwise iteration'''
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield (a, b)
        a = b


def triplewise(iterable):
    '''for iteration over triplets'''
    it = iter(iterable)
    a = next(it, None)
    b = next(it, None)

    for c in it:
        yield (a, b, c)
        a = b
        b = c






def dandrieu_octave_rule(notes: List[m21.note.Note], keySig: m21.key.Key,
                         timeSig: m21.meter.TimeSignature) -> m21.figuredBass.realizer.FiguredBassLine:
    """ applies Dandrieus Rules to harmonize a bass line.
    :ivar: a list of bass notes as well as key and time signature
    :return: a ~music21.figuredBass.realizer.FiguredBassLine object"""
    # keySig = m21.key.Key(key, mode)

    dandrieu_dictionary = {
        'major': {
            # 1: '', 5: '',  # the naturel (empty string defaults to 3,5), # note I add the empty string anyway
            (2, 3): '6,4,3', (2, 1): '6,4,3', (6, 5): '#6,4,3',  # petite sixte
            3: '6', (6, 7): '6', (7, 6): '6',  # sixte simple / sixte doublee
            (4, 5): '6,5',  # quinte et sixte
            (7, 1): '5,6,3',  # fausse quinte
            (4, 3): '4,6,2',  # l'accord de tritone
            (6, 4): '3,6,4',  # Terztausch
            (1, 1, 7): '4,6,2',  # initialformel

        },
        'minor': {
            1: '', 5: '#3,5,8',
            (2, 3): '#6,4,3', (6, 5): '6,4,3', (2, 1): '#6,4,3',
            3: '6', (6, 7): '6', (7, 6): '6',
            (4, 5): '6,5',
            (7, 1): '5,6,3',
            (4, 3): '#4,2,6',
            (6, 4): '3,6,4',  # Terztausch
            (2, 7): '5, #6, 3',  # Alternativakkord
            (2, 7, 1): '7, 5, 3',  # die sieben, falls sie durch den Alternativakkord auf der 2 vorbereitet ist
            (1, 1, 7): '4,6,2',  # initialformel
        }
    }

    fbLine = realizer.FiguredBassLine(keySig, timeSig)  # create a fbLine object

    try:
        dandrieu_rules = dandrieu_dictionary[keySig.mode]

    except KeyError:
        # TODO: raise an error, quit the program
        print('only major and minor are supported modes')

    # iterating over the bass notes:
    notes = deque(notes)
    notes.appendleft(None) # since we use triplets an always wan
    notes.append(None)

    for previous_note, this_note, following_note in triplewise(notes):
        # print(len([x for x in bass.recurse().notes]))
        # solve the try except with a while loop, would be more elegant!!!!
        figures = '' # string to add to the fb_line, start with empty string

        this_note_degree = keySig.getScaleDegreeAndAccidentalFromPitch(this_note.pitch)[0]
        # have to use the long one, getting also the accidental, because of melodic minor...

        if previous_note:
            previous_note_degree = keySig.getScaleDegreeAndAccidentalFromPitch(previous_note.pitch)[0]
        else:
            previous_note_degree = None

        if following_note:
            following_note_degree = keySig.getScaleDegreeAndAccidentalFromPitch(following_note.pitch)[0]
        else:
            following_note_degree = None


        # Start looking up patterns in the dandrieu rule set

        if (previous_note_degree, this_note_degree, following_note_degree) in dandrieu_rules:
            figures = dandrieu_rules[(previous_note_degree, this_note_degree, following_note_degree)]
            # fbLine.addElement(this_note, dandrieu_rules[(previous_note_degree, this_note_degree, following_note_degree)])

        elif (this_note_degree, following_note_degree) in dandrieu_rules:
            figures = dandrieu_rules[(this_note_degree, following_note_degree)]
            # fbLine.addElement(this_note, dandrieu_rules[(this_note_degree, following_note_degree)])

        elif this_note_degree in dandrieu_rules:
            figures = dandrieu_rules[this_note_degree]
            # fbLine.addElement(this_note, dandrieu_rules[this_note_degree])

        # quintfall:
        if previous_note_degree and following_note_degree:  # make sure we do not have none types
            if previous_note_degree-this_note_degree in (-3,4) and this_note_degree-following_note_degree in (-3, 4):
                figures += ',7'

        # add the note and the figures to the fbline object
        fbLine.addElement(this_note, figures)

    return fbLine


def test_dandrieu_rules():
    # create examples:
    # scales
    c_major = "C1 D E F G A B c c B A G F E D C"
    d_major = "D1 E F# G A B c# d d c# B A G F# E D"
    d_minor = 'D1 E F G A B c# d d c B- A G F E D'
    c_minor = 'C1 D E- F G A B c c B- A- G F E- D C'

    # special movements:
    terztausch = 'A1 F G GG C'  # Dandrieu page 20, example in c major
    terztausch_moll = 'A-1 F GG C'

    # initialformel:
    initial = "C1 C BB C"
    initial_moll = "D1 D C# D"
    #mstr_minor = 'C1 D E- F G A B c c B- A- G F E- D C'

    zwei_7_1 = 'D1 E C# D'

    # quintfälle:
    d_quintfall1 = "E1 AA D"
    d_quintfall2 = "D1 G C# D"
    d_quintfall3 = "F1 BB- E2 C# D1"

    # create a bass, with the example I want to test
    bass = m21.converter.parse('tinynotation: 4/4 ' + d_quintfall3)
    # bass = m21.converter.parse('c_major.musicxml')

    # get the list of notes
    notes = bass.recurse().notes
    # set parameters manually
    keySig = m21.key.Key('D', 'Minor')
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

def parse_bass(inbass: m21.stream.Score):
    '''
    for now it just takes the time signature from the beginning, and finds the key by looking at the last note
    and the key signature. If the key signature and the last note do not match up it prints out an error
    :param inbass:
    :return:
    '''

    bass_line = inbass.parts[0] # take first part of the score, it should be a single line
    timeSig = bass_line.getTimeSignatures()[0] # for now it does not work with changing timeSigs in the piece

    Key_signature = bass_line.recurse().getElementsByClass(m21.key.KeySignature)[0]
    Key = Key_signature.asKey()
    
    if bass_line.recurse().notes[-1].name != m21.note.Note(Key.tonic).name:
        Key = Key.relative

        if bass_line.recurse().notes[-1].name != m21.note.Note(Key.tonic).name:
            # Todo: raise an Error
            print("Can not figure out over all key")

    return bass_line.recurse().notes, Key, timeSig


if __name__ == '__main__':
    inbass = m21.converter.parse('d_minor.musicxml')
    notes, keySig, timeSig = parse_bass(inbass)
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