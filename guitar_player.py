"""
S.T.A.L.K.E.R. 2 Guitar Auto-Player

Automatically plays chord accompaniment on the in-game guitar by simulating
mouse movement to radial menu sectors.

Usage:
    python guitar_player.py calibrate          - calibrate sector coordinates
    python guitar_player.py play <song.json>   - play a song

Dependencies:
    pip install -r requirements.txt
"""

import json
import sys
import time
from pathlib import Path

import pyautogui
from pynput import keyboard as pkeyboard

# === Configuration ===

CONFIG_FILE = Path(__file__).parent / 'guitar_config.json'

# Six radial menu sectors, clockwise from top
SECTORS = ['top', 'top_right', 'bottom_right', 'bottom', 'bottom_left', 'top_left']

# Scale 1 (C major diatonic chords)
SCALE_1 = {
    'C':  'top',
    'G':  'top_right',
    'Dm': 'bottom_right',
    'Am': 'bottom',
    'Em': 'bottom_left',
    'F':  'top_left',
}

# Scale 2 (D major diatonic chords)
SCALE_2 = {
    'A':   'top',
    'E':   'top_right',
    'Bm':  'bottom_right',
    'F#m': 'bottom',
    'C#m': 'bottom_left',
    'D':   'top_left',
}

# Key to swap scales (TAB by default; change if your keybind differs)
SCALE_SWAP_KEY = 'tab'

# Timing
SETTLE_DELAY = 0.05      # Pause after mouse move before click
SCALE_SWAP_DELAY = 0.3   # Pause after pressing scale swap


# === Calibration ===

def calibrate():
    """Interactive calibration of radial menu sector positions."""
    print("=" * 60)
    print("RADIAL MENU CALIBRATION")
    print("=" * 60)
    print()
    print("How it works:")
    print("1. Launch S.T.A.L.K.E.R. 2 in windowed or borderless mode")
    print("2. Sit by a campfire, take out the guitar (TAB -> G)")
    print("3. Alt+Tab to this window (do NOT close the guitar menu)")
    print("4. For each sector: hover over its center and press F8")
    print()
    print("IMPORTANT: Keep the guitar menu open in-game during calibration.")
    print()
    input("Press Enter to begin...")

    config = {
        'screen_size': list(pyautogui.size()),
        'sectors': {}
    }

    sector_labels = {
        'top':          'TOP (12 o\'clock) - chord C / A',
        'top_right':    'TOP-RIGHT (2 o\'clock) - chord G / E',
        'bottom_right': 'BOTTOM-RIGHT (4 o\'clock) - chord Dm / Bm',
        'bottom':       'BOTTOM (6 o\'clock) - chord Am / F#m',
        'bottom_left':  'BOTTOM-LEFT (8 o\'clock) - chord Em / C#m',
        'top_left':     'LEFT (10 o\'clock) - chord F / D',
    }

    captured = {'pos': None}

    def on_press(key):
        if key == pkeyboard.Key.f8:
            captured['pos'] = pyautogui.position()
            return False

    for sector in SECTORS:
        print(f"\n[{sector}] {sector_labels[sector]}")
        print("Hover the mouse and press F8...")

        captured['pos'] = None
        with pkeyboard.Listener(on_press=on_press) as listener:
            listener.join()

        x, y = captured['pos']
        config['sectors'][sector] = [x, y]
        print(f"  -> Saved: ({x}, {y})")
        time.sleep(0.4)

    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    print()
    print("=" * 60)
    print(f"Calibration complete. Saved to {CONFIG_FILE}")
    print("=" * 60)


# === Playback ===

def play_song(song_path):
    """Play a song loaded from a JSON file."""
    if not CONFIG_FILE.exists():
        print(f"ERROR: Run calibration first:")
        print(f"  python {sys.argv[0]} calibrate")
        sys.exit(1)

    config = json.loads(CONFIG_FILE.read_text())
    sectors = config['sectors']

    song = json.loads(Path(song_path).read_text(encoding='utf-8'))
    chords = song['chords']

    # Validate that all chords are recognized
    unknown = [c['name'] for c in chords
               if c['name'] not in SCALE_1 and c['name'] not in SCALE_2]
    if unknown:
        print(f"ERROR: Unknown chords: {set(unknown)}")
        print(f"Available: {list(SCALE_1) + list(SCALE_2)}")
        sys.exit(1)

    print("=" * 60)
    print(f"SONG: {song.get('title', 'Untitled')}")
    print(f"Chords: {len(chords)}")
    total = sum(c['duration'] for c in chords)
    print(f"Duration: {total:.1f} s")
    print("=" * 60)
    print()
    print("Switch to the game with the guitar menu open.")
    print("Playback starts in 5 seconds...")
    print("To STOP: move the cursor to the top-left corner of the screen.")
    print()

    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    pyautogui.FAILSAFE = True
    current_scale = 1

    print()
    print("PLAYING...")
    print()

    for idx, chord_entry in enumerate(chords, 1):
        chord = chord_entry['name']
        duration = chord_entry['duration']
        lyrics = chord_entry.get('lyrics', '')

        if chord in SCALE_1:
            target_scale = 1
            sector = SCALE_1[chord]
        else:
            target_scale = 2
            sector = SCALE_2[chord]

        # Swap scale if needed
        if target_scale != current_scale:
            print(f"  [scale swap -> {target_scale}]")
            pyautogui.press(SCALE_SWAP_KEY)
            current_scale = target_scale
            time.sleep(SCALE_SWAP_DELAY)
            duration -= SCALE_SWAP_DELAY

        x, y = sectors[sector]
        pyautogui.moveTo(x, y, duration=0.03)
        time.sleep(SETTLE_DELAY)

        print(f"  [{idx:2d}/{len(chords)}] {chord:4s} ({duration:.1f}s)  {lyrics}")
        pyautogui.click()

        time.sleep(max(0.05, duration - SETTLE_DELAY))

    print()
    print("Done.")


# === Entry point ===

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == 'calibrate':
        calibrate()
    elif cmd == 'play':
        if len(sys.argv) < 3:
            print("Specify a song file: python guitar_player.py play song.json")
            sys.exit(1)
        play_song(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
