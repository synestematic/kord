from bestia.iterate import LoopedList

from .intervals import Intervals

from ..errors import InvalidNote, InvalidAlteration, InvalidOctave

__all__ = [
    'NotePitch',
    'notes_by_alts',
]

# put enharmonic matrix and note bya lts inside note pitch class

# PRELEVARE SOLDI X TAXI

C3 = NotePitch('C', '' , 3)
D3 = NotePitch('D', '' , 3)
E3 = NotePitch('E', '' , 3)
F3 = NotePitch('F', '' , 3)
G3 = NotePitch('G', '' , 3)
A3 = NotePitch('A', '' , 3)
B3 = NotePitch('B', '' , 3)


def notes_by_alts():
    ''' yields all 35 possible notes in following order:
        * 7 notes with alt ''
        * 7 notes with alt 'b'
        * 7 notes with alt '#'
        * 7 notes with alt 'bb'
        * 7 notes with alt '##'
    '''
    # sort alts
    alts = list(
        NotePitch.input_alterations()
    )
    alts.sort(key=len) # '', b, #, bb, ##

    # get all notes
    notes = []
    for ehns in _EnharmonicMatrix:
        for ehn in ehns:
            notes.append(ehn)

    # yield notes
    for alt in alts:
        for note in notes:
            if note.alt == alt:
                # note.oct = 3
                yield note
