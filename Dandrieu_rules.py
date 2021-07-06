import music21 as m21
from music21.figuredBass import rules
from music21.figuredBass import examples
from music21.figuredBass import realizer


def dandrieu_octave_rule(notes, keySig: m21.key.Key,
                         timeSig: m21.meter.TimeSignature) -> m21.figuredBass.realizer.FiguredBassLine:
    """creates a composition after Dandrieu's Octave rule"""
    # keySig = m21.key.Key(key, mode)
    fbLine = realizer.FiguredBassLine(keySig, timeSig)  # create a fbLine object

    if keySig.mode == 'major':
        dandrieu_rules = {1: '', (2, 3): '6,4,3', 3: '6', (4, 5): '6,5',
                          5: '', (6, 7): '6', (7, 1): '5,6,3', (7, 6): '6',
                          (6, 5): '#6,4,3', (4, 3): '4,6,2', (2, 1): '6,4,3'}

    elif keySig.mode == 'minor':
        dandrieu_rules = {1: '', (2, 3): '#6,4,3', 3: '6', (4, 5): '6,5',
                          5: '', (6, 7): '6', (7, 1): '6', (7, 6): '6',
                          (6, 5): '6', (4, 3): '4,6', (2, 1): '6'}

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
            this_note_degree = keySig.getScaleDegreeFromPitch(bass_note.pitch)
            following_note_degree = keySig.getScaleDegreeFromPitch(following_note.pitch)

            if this_note_degree in dandrieu_rules:
                fbLine.addElement(bass_note, dandrieu_rules[this_note_degree])

            elif (this_note_degree, following_note_degree) in dandrieu_rules:
                fbLine.addElement(bass_note, dandrieu_rules[(this_note_degree, following_note_degree)])

        except IndexError:
            fbLine.addElement(bass_note)  # no notation added, always end on the naturel


    return fbLine


if __name__ == '__main__':
    # create example
    c_major = "C1 D E F G A B c c B A G F E D C"
    d_major = "D1 E F# G A B c# d d c# B A G F# E D"
    #mstr_minor = 'C1 D E- F G A B c c B- A- G F E- D C'
    bass = m21.converter.parse('tinynotation: 4/4 ' + d_major)
    # bass = m21.converter.parse('c_major.musicxml')

    # get the notes, for now getting all the notes
    notes = bass.recurse().notes
    # set parameters manually
    keySig = m21.key.Key('D', 'major')
    timeSig = m21.meter.TimeSignature('4/4')

    # get the fb_line with the figures
    fbLine = dandrieu_octave_rule(notes, keySig, timeSig)
    fbLine.realize()

    # realizing the chords from the created figures
    fbRules = rules.Rules()  # in case you want to change the rules?
    # fbRules.partMovementLimits = [(1, 3), (2, 4), (3, 5)]
    allSols = fbLine.realize(fbRules)  # get all solutions
    print(allSols.getNumSolutions())
    allSols.generateRandomRealization().show()  # generate a solution

