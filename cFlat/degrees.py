from bestia.iterate import LoopedList
from bestia.output import echo
from collections import deque

class Degrees(object):

    def __init__(self, *degrees):
        self.original_length = len(degrees)
        self.original_order  = tuple(degrees)
        self.reset()

    def __repr__(self):
        return str(self.current_order)

    def __getitem__(self, i):
        return self.current_order[i]


    def reset(self):
        ''' ALWAYS iterate thru items in original_order
            BUT do not modify its contents
        '''
        self.current_order = list(self.original_order)

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
        ''' exact Note in order:
            == enforces exact note match
        '''
        self.reset()
        for degree in self.original_order:
            if degree == note:
                return True
            self.rotate()

    def _rotate_by_magnitude(self, note):
        ''' exact Note NOT in order:
            >= allows enharmonic equality
            octs from original_order degrees MUST BE
            increased by note.oct for >= evaluation
        '''
        self.reset()
        for degree in self.original_order:

            degree.oct += note.oct
            if degree >= note:
                degree.oct -= note.oct
                return True

            degree.oct -= note.oct
            self.rotate()
