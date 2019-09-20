# kord
kord is a python framework exposing a simple api that enables programmers to create music-based applications. It focuses mainly on plucked-string, tempered instruments such as guitars, basses, ukuleles and such...

<hr/>

## API

### class Note():
Note instances are the lowest-level objects of the framework and have 3 main attributes:

* (str) tone
* (str) alt
* (int) oct

Only the tone attribute is required to create an instance. Default values for .alt and .oct are "" and 3.

```
>>> from kord import Note
>>> e = Note('e')
>>> e
E³
```

Note objects implement comparison operators based on their semitone intervals:

```
>>> f = Note('F')
>>> f 
F³
>>> f > e
True
```

Therefore, enharmonic relationships can be evaluated as follows:

```
>>> n1 = Note('F', '#', 5)
>>> n2 = Note('G', 'b', 5)
>>> n1, n2
(F♯⁵, G♭⁵)
>>> n1 != n2
False
```

Notes with double alterations are also supported:

```
>>> n3 = Note('A', 'bb', 1)
>>> n3
A𝄫¹
>>> n4 = Note('F', '##', 1)
>>> n4
F𝄪¹

```

Given that python lacks a `===` operator, Notes can be compared for a "stricter" equality using their `is_note()` method:

```
>>> n3 == n4
True
>>> n3.is_note(n4)
False
```

This method compares the attributes of the notes directly (not the semitone interval between them). Set the `ignore_oct` argument appropriately for a less strict comparison:

```
>>> n1
F♯⁵
>>> n1.is_note(Note('F', '#', 3))
False
>>> n1.is_note(Note('F', '#', 3), ignore_oct=False)
True
```


### DiatonicKey: (class)
### ChromaticKey: (class)


### String: (class)
### Tuning: (class)


### Arguments

* -h --help  

* -f --frets [int] 
* -v --verbose [int] 

