# kord
kord is a python framework that provides programmers with a simple api for the creation of music-based applications. While it's mainly focused for theoretical purposes, some of it's more visually oriented features are well-suited for the generation of plucked-string instruments.


## installation

The only dependency for `kord` is the pip package `bestia`, my own library for creating command-line applications. It will be automatically downloaded when you install using pip:

```
$   python3 -m pip install kord
```



# api reference:

First, let me say that all of the following will only make sense to you if you already have some background on music theory|harmony.

## kord.notes module:

### class Note(object):

Note instances are the lowest-level objects of the framework and have 3 main attributes:

```
* chr: str   ('C', 'D', 'E', 'F', 'G', 'A', 'B')
* alt: str   ('b', 'bb', '', '#', '##')
* oct: int   (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```


Only the `chr` argument is required to create an instance. Arguments `alt` and `oct` will default to `''` and `3` respectively.

```
>>> from kord.notes import Note
>>> e3, f3 = Note('e'), Note('f')
>>> e3, f3
(E³, F³) 
>>> Note('B', 'b', 7)
B♭⁷
>>> Note('C', '#', 0)
C♯⁰
```

Notes with double alterations are supported but Notes with triple (or more) alterations raise InvalidAlteration Exceptions:

```
>>> n3 = Note('A', 'bb', 1)
>>> n3
A𝄫¹
>>> n4 = Note('F', '##', 1)
>>> n4
F𝄪¹
>>> Note('G', '###')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
kord.errors.InvalidAlteration: ###
```


 
Intervals between note objects can be evaluated using the following operators:  ```-   < >   <= >=   == !=   >>   ** ```
 
These allow calculation of semitone deltas between notes as well as insights into their enharmonic relationships. Let's take a quick look at each operator separately:

#### - operator

The substraction operator allows you to calculate the difference in semitones between two notes:

```
>>> f3 - e3
1
>>> Note('a', 'b', 2) - Note('g', '#', 2)
0
>>> Note('a', 8) - Note('c', 4)
57
>>> Note('a', 8) - Note('c', '##', 4)
55
```


####  < >   <= >=   == !=  operators

Comparison operators return boolean values based on the interval between 2 notes. 

```
>>> f3 > e3
True
>>> f3 >= e3
True
```

While the concept is seemingly straightforward, special attention needs to be taken when using `== !=` with enharmonic notes.

```
>>> n1 = Note('F', '#', 5)
>>> n2 = Note('G', 'b', 5)
>>> n1, n2
(F♯⁵, G♭⁵)
>>> n1 == n2
True
```

The notes F#5 and Gb5 are not the same but `==` checks their interval and since its a unison,  the comparison evaluates True. This might seem a bit counter-intuitive at first but `kord` uses different operators to check for exact note matches.

#### >> ** operators

The power and right-shift operators allow you to compare Notes for equality based not on their intervals, but on their internal properties. The strictest operator is `>>` which compares note, alteration and octave attributes while `**` is less strict and only compares note and alteration. 

```
>>> ab1, ab5 = Note('A', 'b', 1),  Note('A', 'b', 5)
>>> ab1 == ab5
False
>>> ab1 ** ab5
True
```

Notice that `**` evaluated True because both instances are A flat notes, even though there is a wide interval between them.

```
>>> ab1 >> ab5
False
>>> ab1.oct = 5
>>> ab1 >> ab5
True
```

For the `>>` operator to evaluate True, the octave of the notes has to match as well.



<hr/>




## kord.keys module:


### class MusicKey(object):

Think of MusicKey objects as generators of Note objects. You can define a new class which inherits MusicKey and use any theoretical arrangement of `intervals` from the root note in order to create chords, scales, modes. You can further restrict these child classes by restricting `degrees` to specific values.

These are a couple of pre-defined examples to give you an idea of how it works:

```
class ChromaticScale(MusicKey):
    intervals = (
        UNISON,
        MINOR_SECOND,
        MAJOR_SECOND,
        MINOR_THIRD,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH,
        MAJOR_SEVENTH,
	)

class MajorScale(MusicKey):
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )
    
class MajorPentatonicScale(MajorScale):
    degrees = (1, 2, 3, 5, 6)

class MajorTriad(MajorScale):
    degrees = (1, 3, 5)
```

When we create an instance of a MusicKey subclass, we can then access it's items using list index notation:

```
>>> from kord.keys import ChromaticScale
>>> c_chromatic_scale = ChromaticScale('C')
>>> c_chromatic_scale[2]
C♯⁰
>>> c_chromatic_scale[12]
B⁰
```

### MusicKey.spell() method

Using list index notation is fine but perhaps it is more interesting to look at a different and more dynamic way of getting the items of our MusicKey instances. The `spell()` method provides a simple interface that generates Note instances on the fly. Let's take a look at a couple of examples and the several arguments that we can use when calling this method:

```
>>> for note in c_chromatic_scale.spell():
...     print(note, end=' ')
...
C⁰ C♯⁰ D⁰ D♯⁰ E⁰ F⁰ F♯⁰ G⁰ G♯⁰ A⁰ A♯⁰ B⁰ C¹ >>> 
```


The `note_count` argument is an `int` that allows us to specify the amount of notes we want:

```
>>> from kord.keys import MinorScale
>>> a_minor_scale = MinorScale('A')
>>> for note in a_minor_scale.spell(note_count=4):
...     print(note, end=' ')
...
A⁰ B⁰ C¹ D¹ >>> 
```


The `yield_all` argument is a `bool` that will make the method yield not just Note instances, but also None instances for every non-diatonic semitone found:

```
>>> for note in a_minor_scale.spell(note_count=4, yield_all=True):
...     print(note, end=' ')
...
A⁰ None B⁰ C¹ None D¹ >>> 
```


The `start_note` argument is a `Note` object that can be used to start getting notes from a specific note. This can be done even if the note is not part of the scale:

```
>>> Db1 = Note('D', 'b', 1)
>>> for note in a_minor_scale.spell(note_count=4, yield_all=True, start_note=Db1):
...     print(note, end=' ')
...
None D¹ None E¹ F¹ None G¹ >>> 
```


## fretboard sample application

A sample application `fretboard.py` comes built-in with the kord framework and gives some insight into it's possibilities. It displays a representation of the fretboard of your instrument, tuned to your preference along as where to find the notes for any given mode for any given root note.

```
usage: fretboard.py [-h] [-m] [-i] [-t] [-f] [-v] ROOT

<<< Fretboard visualizer sample tool for the kord music framework >>>

positional arguments:
  ROOT                select a root note

optional arguments:
  -h, --help          show this help message and exit
  -m , --mode         mode to visualize: ['major', 'minor', 'natural_minor', 'melodic_minor', 'harmonic_minor', 'ionian', 'lydian', 'mixo', 'aeolian', 'dorian', 'phrygian', 'chromatic']
  -i , --instrument   instrument fretboard to visualize: ['banjo', 'guitar', 'bass', 'ukulele']
  -t , --tuning       instrument tuning: check your .json files for available options
  -f , --frets        number of displayed frets: [0, 1, 2, .. , 36]
  -v , --verbosity    application verbosity: [0, 1, 2]

```

You will find some pre-defined instrument tunings in the `tunings` directory in the form of .json files. Feel free to modify these or add your own following the correct syntax and they will immediately become available to the fretboard tool.

I'm pretty sure guitar/bass players may find it very handy as a means to develop their knowledge of their instrument. Have fun!
