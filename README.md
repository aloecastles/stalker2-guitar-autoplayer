# 🎸 STALKER 2 Guitar Auto-Player

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()

A Python script that plays chord accompaniment on the in-game guitar in **S.T.A.L.K.E.R. 2: Heart of Chornobyl**. Reads a song from a JSON file and automates mouse movement to the radial menu sectors to play chords in time.

## How it works

The in-game guitar interface is a radial menu with 6 chord slots × 2 scales = 12 chords total. The script:

1. **Loads a song file** with a list of chords and durations.
2. **Moves the mouse** to the screen coordinate of the required sector (set during calibration).
3. **Clicks** to strum the chord.
4. **Waits** for the duration before moving to the next chord.
5. **Presses the scale-swap key** (TAB by default) when the next chord lives in a different scale.

```
   Scale 1 (C major)              Scale 2 (D major)
        C                                A
   F         G                      D         E
    Dm     Em                        Bm     C#m
        Am                              F#m
```

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set the game to borderless windowed mode

`Settings → Graphics → Window Mode → Borderless`

Fullscreen Exclusive will close the guitar menu on Alt+Tab.

### 3. Calibrate (once per monitor / resolution)

In-game: sit by a campfire, take out the guitar (`TAB → G`). Then Alt+Tab to your terminal:

```bash
python guitar_player.py calibrate
```

Hover the mouse over each sector when prompted and press **F8** to save its coordinate. Coordinates are written to `guitar_config.json`.

### 4. Play a song

```bash
python guitar_player.py play songs/twinkle.json
```

You get a 5-second countdown to Alt+Tab back into the game with the guitar menu open.

**Emergency stop:** move the cursor to the top-left corner of the screen (PyAutoGUI failsafe).

## Song format

Songs are plain JSON files:

```json
{
  "title": "Song name",
  "chords": [
    {"name": "C", "duration": 2.0, "lyrics": "optional line"},
    {"name": "F", "duration": 2.0},
    {"name": "G", "duration": 1.5}
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Chord name. Must be one of the 12 available chords. |
| `duration` | yes | How long to hold the chord in seconds. |
| `lyrics` | no | Printed to console as a sync aid. |

### Available chords

**Scale 1:** `C`, `G`, `Dm`, `Am`, `Em`, `F`
**Scale 2:** `A`, `E`, `Bm`, `F#m`, `C#m`, `D`

Scale swaps are automatic.

## Included songs

| File | Description | Uses |
|------|-------------|------|
| `songs/twinkle.json` | Twinkle Twinkle Little Star | Scale 1 only |
| `songs/house_of_rising_sun.json` | House of the Rising Sun (simplified) | Both scales (tests auto-swap) |

## Configuration

Edit constants at the top of `guitar_player.py`:

| Constant | Default | Purpose |
|----------|---------|---------|
| `SCALE_SWAP_KEY` | `'tab'` | Keyboard key bound to scale swap in-game |
| `SETTLE_DELAY` | `0.05` | Pause between mouse move and click |
| `SCALE_SWAP_DELAY` | `0.3` | Pause after pressing scale swap |

## Troubleshooting

<details>
<summary><b>TAB doesn't swap scales</b></summary>

In the screenshots the prompt shows `LB` (gamepad). Open the game's keyboard bindings, find the **Scale swap** action, and either rebind it to TAB or set `SCALE_SWAP_KEY` to whatever key is actually bound.
</details>

<details>
<summary><b>Mouse hits the wrong sector</b></summary>

Re-run calibration. The HUD position can shift if you change resolution, FOV, or scale settings.
</details>

<details>
<summary><b>Guitar menu closes mid-song</b></summary>

Almost always caused by Fullscreen Exclusive mode. Switch to Borderless.
</details>

<details>
<summary><b>Game ignores synthetic clicks</b></summary>

Some games block input from non-hardware sources via DirectInput hooks. If clicks do nothing, try running the terminal as Administrator. If still nothing, the script won't work for this build of the game without a lower-level input driver (e.g., Interception or a virtual HID device).
</details>

## Limitations

- **Chords only, not single notes.** The game's guitar UI exposes chords, not individual pitches. You can't play melodies like solo lead lines - only accompaniment.
- **MIDI files don't translate directly.** A MIDI file with melody notes can't be played as-is. You need a chord chart (e.g., from Ultimate Guitar) converted to the JSON format above.
- **Timing is OS-level.** Sub-50ms accuracy is not guaranteed. Fine for ballads and folk songs, not for fast strumming patterns.

## Roadmap

- [ ] Strumming patterns (multiple clicks per chord with rhythm)
- [ ] MIDI-to-chord-chart converter (best-effort chord detection)
- [ ] GUI for editing songs
- [ ] More included songs

## License

MIT - see [LICENSE](LICENSE).

## Disclaimer

This is a personal automation tool for an offline single-player feature. Not affiliated with GSC Game World.
