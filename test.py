from kord.tests import *

# so using relative imports in my modules means that I can NOT run them directly
# because I need to import the parent beforehand... like from this script

if __name__ == '__main__':
    '''
    TDD:
        * write test
        * fail test RED
        * write code
        * pass test GREEN
        * remove duplication REFACTOR
        * pass test
    '''
    try:
        # b0 = Note('B', 0)
       
        # a0 = Note('A', 0)
        # c1 = Note('C', 1)
        # e1 = Note('E', 1)        

        # degrees = Degrees(
        #     a0, c1, e1
        # )
        # print(degrees)

        # degrees.rotate_by_note(e1)
        # print(degrees)

        # degrees.rotate_by_note(b0)
        # print(degrees)


        # degrees.rotate_by_note(c1)
        # print(degrees)
        
        # degrees.rotate()
        # print(degrees)


        # s = MajorKey('B')
        # non = Note('D', 1)
        # for note in s._spell(
        #     note_count=1, start_note=non, yield_all=False
        # ):
        #     # should be D#1 ,  not C#2
        #     print(note)

        unittest.main()

        # for note in MinorKey('A').ninth(note_count=17, yield_all=False):
        #     print(note)


    except KeyboardInterrupt:
        print()

# https://docs.python.org/3/library/operator.html
# https://stackoverflow.com/questions/39754808/overriding-not-operator-in-python
