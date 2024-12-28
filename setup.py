import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kord",
    version="5.2",
    author="Federico Rizzo",
    author_email="synestem@ticATgmail.com",
    description='programming framework for developing music applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synestematic/kord",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    data_files=[
        ('fretboard', [  #  ~/.local/fretboard/
            'app/fretboard.py',
            'app/tuner.py',
            ],
        ),
        ('fretboard/tunings', [
            'app/tunings/banjo.json',
            'app/tunings/bass.json',
            'app/tunings/guitar.json',
            'app/tunings/ronroco.json',
            'app/tunings/ukulele.json',
            ],
        ),
    ],
    install_requires=[
        'bestia',
    ],
)
