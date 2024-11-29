
__all__ = [
    'InvalidInstrument',
    'InvalidScale',
    'InvalidChord',
    'InvalidNote',
    'InvalidAlteration',
    'InvalidOctave',
]


class InvalidInstrument(Exception):
    pass

class InvalidScale(Exception):
    pass

class InvalidChord(Exception):
    pass

class InvalidNote(Exception):
    pass

class InvalidAlteration(Exception):
    pass

class InvalidOctave(Exception):
    pass
