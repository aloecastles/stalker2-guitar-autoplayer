# Song format

Songs are JSON files with a list of chord events. Each event has a chord name and a duration in seconds.

## Schema

```json
{
  "title": "string (required) - song name",
  "tempo_bpm": "number (optional) - reference tempo",
  "comment": "string (optional) - notes for humans",
  "chords": [
    {
      "name": "string (required) - chord name from the list below",
      "duration": "number (required) - seconds to hold before next chord",
      "lyrics": "string (optional) - shown in console as a sync aid"
    }
  ]
}
```

## Allowed chord names

### Scale 1 (C major family)

| Chord | Sector |
|-------|--------|
| `C`   | top (12 o'clock) |
| `G`   | top-right |
| `Dm`  | bottom-right |
| `Am`  | bottom |
| `Em`  | bottom-left |
| `F`   | left (10 o'clock) |

### Scale 2 (D major family)

| Chord | Sector |
|-------|--------|
| `A`   | top |
| `E`   | top-right |
| `Bm`  | bottom-right |
| `F#m` | bottom |
| `C#m` | bottom-left |
| `D`   | left |

## Tips for writing songs

- **Pick a tonality covered by one scale** when possible. Mixing scales works but inserts a ~0.3s pause when swapping.
- **Find chord charts** on sites like Ultimate Guitar, Chordify, or Songsterr. Many simple songs use only 3-4 chords.
- **Map unsupported chords to the nearest available one.** If a song has Cmaj7, use C. If it has Dsus4, use D.
- **Duration in seconds**, not beats. At 80 BPM, one beat = 0.75s, so a chord held for 4 beats = 3.0 seconds.

## Example: 4-chord song

```json
{
  "title": "Generic 4-chord pop song",
  "tempo_bpm": 100,
  "chords": [
    {"name": "C",  "duration": 1.8},
    {"name": "G",  "duration": 1.8},
    {"name": "Am", "duration": 1.8},
    {"name": "F",  "duration": 1.8}
  ]
}
```

Loop the array in a tool of your choice if you want the progression to repeat.
