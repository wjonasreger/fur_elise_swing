# ABC to Jazz Transformation of "Für Elise"

## Origin Story

One night, in the deep dark hours when everyone was likely sleeping and I should've been sleeping as well, I was sluggishly and lazily playing out a segment of "Für Elise" to quench my boredom as I felt restless and couldn't sleep. "Für Elise" is a song that I've played rather consistently over the many years I've played piano, and as such it is almost ritualistic that I play it everyday when possible because it helps centers my mind from time to time. This one late night I was playing it with complete disregard to the standard temporal measures and accidentally discovered a fun variant: a jazzed up "Für Elise". Thus, I became very interested in hearing what this would sound like. Unfortunately, I'm rigidly familiar with the traditional feel of the song, so generating it by playing the piano myself was a big challenge... And this is how this project came to be — I could synthetically create this using another skillset of mine: writing code and manipulating data.

## Overview

The ABC to Jazz Transformation is a Python project designed to transform ABC notation of classical music, specifically "Für Elise" in this case, into jazzed-up versions with swing beats and a faster tempo. This project processes the ABC notation (a simplified, manually edited version), converts it into vectors representing frequencies and durations, applies temporal modifications, and outputs jazz versions of the music with the help of SuperCollider (a platform for audio synthesis and algorithmic composition).

## Samples



## Features

- Converts ABC notation of "Für Elise" into vectors of frequencies and durations.
- Applies swing beats and faster tempo to generate jazzed-up versions.
- Outputs transformed music data in a format compatible with audio synthesis software for audio recordings.

## Usage

1. **Input:** Provide the ABC notation of "Für Elise" in the input file.
2. **Processing:** Run the Python jupyter notebook to process the ABC notation to generate SuperCollider code.
3. **Output:** Generate and record the jazzed-up versions of "Für Elise" with swing beats and increased tempo.

## Documents

- `fur-elise-swing.ipynb` — Demo document containing the full process of converting "Für Elise" to a swing version.
- `process.py` — All supporting functions and variables for music processing.
- `fur-elise.abc` — Original ABC file for "Für Elise".
- `audio/` — All generated audio samples of "Für Elise" variants.
- `sc/` — All generated SuperCollider code samples of "Für Elise" variants.
- `imgs/` — Images to show concept of Jazz swing time measures.

## Dependencies

- Python 3.x
- SuperCollider (for music processing)
- ABC notation input (manually edited from original ABC file)

## Getting Started

1. Clone the repository or download the script.
2. Install the required software (i.e., Python and SuperCollider).
3. Place your ABC notation of "Für Elise" in the notebook. Or experiment with other songs, or extend the project code to handle more ABC notations and music manipulation criteria.
4. Run the script and enjoy the transformed jazz versions!

## License

This project is licensed under the [MIT License](link-to-license).