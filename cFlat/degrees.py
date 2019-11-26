from bestia.output import echo

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
        return self._rotate_by_char(note)
        # return self._rotate_by_magnitude(note)

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
            input(degree)
            if degree >= note:
                degree.oct -= note.oct
                return True

            degree.oct -= note.oct
            self.rotate()

    def _rotate_by_char(self, note):

        self.reset()

        for d, _ in enumerate(self.original_order):

            # B0
            for rc in self.degree_char_check(d, note):

                echo(self.original_order[d], 'red')
                input()

                # try degree's next adj_char
                if rc == 'next_d':
                    self.rotate()
                    break

                # match check note
                elif rc == 'match':
                    return True

                # reached next degree_order.chr
                # elif rc == 'next_c':
                #     pass


    def degree_char_check(self, degree=0, note=None):

        this_deg = self.original_order[degree]
        next_deg = self.original_order[degree +1]

        c = 1
        while True:

            echo(this_deg, 'green')
            input()

            if this_deg.adjacent_chr(c) == note.chr:
                # match check note
                yield 'match'

            if this_deg.adjacent_chr(c) == next_deg.chr:
                # reached next degree_order.chr
                yield 'next_d'

            # try degree's next adj_char
            # yield 'next_c'
            c += 1
