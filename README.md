# Python Code Collection

A collection of Python scripts covering simulations, games, calculators, visualizations, and utilities.

---

## Root Scripts

| Script | Dependencies | Description |
|--------|-------------|-------------|
| `arrow.py` | `numpy`, `matplotlib` | Draws an arrow over a colored grid, highlights which cells it passes through, and computes a weighted sum using time-of-flight values. |
| `arrow_grid.py` | `numpy`, `matplotlib` | Exhaustively searches all edge-to-edge arrow paths across a grid to find the one with the minimum cell-value sum, then plots the result. |
| `bike_calc.py` | stdlib only | Prints a repair invoice for an Ariel Rider e-bike and calculates the total cost of parts across two invoices. |
| `blueflower.py` | stdlib only | Uses the `turtle` module to draw 50 randomly placed blue flowers made of overlapping circles. |
| `chinesetest.py` | `pandas`, `tkinter` (stdlib) | Gamified Chinese flashcard app. Player fights a dragon by selecting the correct Chinese translation via a Tkinter GUI. Supports easy/hard modes and a dictionary lookup mode. Reads from `words.csv`. |
| `computational_geometry.py` | `Shapely`, `matplotlib` | Demonstrates computational geometry using Shapely: creates points, lines, rings, and polygons; computes areas and lengths; plots an event park layout with an info booth and stage. |
| `dancingparticles.py` | `numpy`, `matplotlib` | Simulates bouncing particles with elastic collisions and sphere-of-influence attraction. Renders an animation and saves it as `dancingparticles.mp4`. |
| `drawheart.py` | `numpy`, `matplotlib` | Plots a parametric heart curve using trigonometric equations and saves it to `heart.png`. |
| `ecc.py` | `numpy` | Expected Casualty Calculator for space vehicle failures. Models failure probabilities across flight regimes (deorbit, free flight, parachute) and computes expected casualties against an accepted limit. |
| `evcar_calc.py` | stdlib only | Compares the per-mile fuel cost of a Polestar 2 EV versus a Toyota Corolla given user-supplied electricity and gas prices. |
| `game.py` | stdlib only | Skeleton for a text-based RPG called "Blood World Final Battle." |
| `gratitudes.py` | `numpy` | Defines a `Friend` class and prints a formatted table of friends with their affiliations and contact info. |
| `imagemetadata.py` | `exif`, `reverse-geocoder`, `pycountry` | Reads EXIF metadata from JPEG images (device info, timestamps, GPS coordinates), reverse-geocodes GPS to a location name, and opens the location in Google Maps. |
| `pygame_test.py` | `pygame` | Minimal pygame window that draws a blue circle. Used as a basic pygame sanity check. |
| `tracker_income.py` | stdlib only | Tracks tutoring and miscellaneous income by client and date, prints per-client totals, and summarizes Roth IRA contributions. |
| `tracker_timeoff.py` | stdlib only | Tracks PTO hours used by date and prints milestone warnings as weekly thresholds are crossed. |
| `vector_assess.py` | `numpy` | Loads a `.npy` file produced by `vector_calc.py` and validates that the nominal + fixed-offset + proportional-offset vectors reconstruct correctly. |
| `vector_calc.py` | `numpy`, `matplotlib` | Generates randomized 3D vectors by combining a nominal vector with fixed-magnitude and proportional-magnitude Gaussian offsets, plus transverse dispersion. Plots a 3D quiver chart and saves results to a `.npy` file. |

---

## Subdirectories

### `cardgame/`

A turn-based creature card game playable by human or AI.

| File | Dependencies | Description |
|------|-------------|-------------|
| `main.py` | `PyYAML`, `rich` | Entry point. Sets up players and runs the game loop. |
| `creature.py` | `PyYAML` | Defines `Creature`, `Player`, `AIPlayer`, and `HumanPlayer` classes. Loads creature definitions from a YAML file. |
| `display.py` | `rich` | Renders game state to the terminal using Rich panels, tables, and progress bars. |
| `turn.py` | `PyYAML`, `rich` | Handles game turn logic: buy phase, activate phase, and attack phase. |
| `turn_print.py` | `rich` | Utilities for printing turn-related output. |

### `gymnasium_test/`

| File | Dependencies | Description |
|------|-------------|-------------|
| `gym_test.py` | `gymnasium`, `pygame` | Tests a Gymnasium reinforcement learning environment with a pygame-based display. |

### `socialnetwork/socialchart/`

| File | Dependencies | Description |
|------|-------------|-------------|
| `socialchart.py` | `networkx`, `matplotlib` | Builds and visualizes a social network graph using NetworkX and matplotlib. |

### `teachpython/`

| File | Dependencies | Description |
|------|-------------|-------------|
| `hello.py` | stdlib only | Basic hello world / teaching script. |
