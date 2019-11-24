from bestia.iterate import LoopedList
from bestia.output import echo
from collections import deque

def dbg(t, c=''):
    echo(t, c)
    input()

class Degrees(object):

    def __init__(self, *degrees):
        # A0 C1 E1
        self.original_length = len(degrees)
        self.original_order  = [ d for d in degrees ]
        self.reset()

    def __repr__(self):
        return str(self.current_order)

    def __getitem__(self, i):
        return self.current_order[i]


    def reset(self):
        ''' always iterate thru items in original order '''
        self.current_order = [ d for d in self.original_order ]

    def rotate(self):
        self.current_order.insert(
            # pop item0 into last_item
            self.original_length, self.current_order.pop(0)
        )

    def rotate_by_note(self, note):
        if note in self.original_order:
            return self._rotate_by_presence(note)
        return self._rotate_by_magnitude(note)

    def _rotate_by_presence(self, note):
        self.reset()
        for degree in self.original_order:
            if degree == note:
                return True
            self.rotate()

    def _rotate_by_magnitude(self, note):
        self.reset()
        for degree in self.original_order:
            if degree > note:
                return True
            self.rotate()


if __name__ == "__main__":

    degrees = Degrees( 1, 3, 5 )
    # print(degrees)
    degrees.rotate_by_note(5)
    print(degrees)
    degrees.rotate_by_note(2)
    print(degrees)
    degrees.rotate_by_note(3)
    print(degrees)
    degrees.rotate()
    print(degrees)

