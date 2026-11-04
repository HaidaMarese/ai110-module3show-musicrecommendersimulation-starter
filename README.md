# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a music recommender simulation that suggests songs based
on a listener's favorite genre, favorite mood, and preferred energy level.
It compares those preferences with song attributes in a CSV catalog, ranks
the songs by score, and explains how each recommendation earned its points.

The catalog contains 18 songs, including 10 starter songs and eight
fictional additions. The expanded catalog covers more genres and moods
and helps illustrate how scoring choices affect which songs a listener
discovers.

---

## How The System Works

Real-world recommenders can use collaborative filtering to suggest items
that people with similar listening habits enjoy. They can also use
content-based filtering to compare item features with a listener's
preferences. VibeFinder uses content-based filtering with taste profiles
defined directly in the program.

- **Song.** Each record contains `id`, `title`, `artist`, `genre`, `mood`,
  `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
  The scoring rule uses `genre`, `mood`, and `energy`.
- **UserProfile.** Each profile stores `favorite_genre`, `favorite_mood`,
  and `target_energy`.
- **Recommender.** The recommender scores each song, records the reasons
  for its score, and returns the five highest-scoring songs.

### Taste Profiles

| Profile | Favorite genre | Favorite mood | Target energy |
|---|---|---|---:|
| High-Energy Pop | `pop` | `happy` | 0.85 |
| Chill Lofi | `lofi` | `chill` | 0.25 |
| Deep Intense Rock | `rock` | `intense` | 0.90 |

Storm Runner matches the Deep Intense Rock profile's genre and mood.
Its energy of `0.91` is close to the `0.90` target. Library Rain matches
the Chill Lofi profile's genre and mood and has an energy of `0.35`,
which is `0.10` above its target.

### Algorithm Recipe

1. Add **2.0 points** for an exact genre match.
2. Add **1.0 point** for an exact mood match.
3. Add `1.0 - abs(song_energy - target_energy)` for energy similarity.
   Songs closer to the target earn more points. An exact energy match
   earns **1.0 point**.
4. Sort the songs from highest to lowest score and show the top five.
   If songs have the same score, keep their original CSV order.

The maximum score is **4.0**. The two-point genre bonus can put a song
from the preferred genre above a song that better matches the requested
mood. For example, Gym Hero gets the full genre bonus for `pop`, while
Rooftop Lights receives zero genre points because its label is `indie pop`.

**Data flow**

`Song catalog + taste profile → score each song and record reasons → sort by score → display the top five`

---

## Getting Started

### Setup

Run these commands from the project folder on Windows.

1. Create a virtual environment if `.venv` does not already exist.

   ```cmd
   py -3 -m venv .venv
   ```

2. Activate it using the command for your terminal.

   **Command Prompt**

   ```cmd
   .venv\Scripts\activate.bat
   ```

   **PowerShell**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies.

   ```cmd
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Run the app.

   ```cmd
   python -m src.main
   ```

### Running Tests

Run the starter tests from the project folder.

```cmd
python -m pytest
```

The starter test file is `tests/test_recommender.py`.

---

## Sample Recommendation Output

This example shows hand-calculated scores for three starter songs.
The CLI will score and rank the full catalog.

```text
User profile: High-Energy Pop
Favorite genre: pop | Favorite mood: happy | Target energy: 0.85

1. Sunrise City | Score: 3.97
   Reasons: genre match (+2.00), mood match (+1.00), energy similarity (+0.97)

2. Gym Hero | Score: 2.92
   Reasons: genre match (+2.00), energy similarity (+0.92)

3. Rooftop Lights | Score: 1.91
   Reasons: mood match (+1.00), energy similarity (+0.91)
```

<!-- Replace the manual example with actual CLI output showing the top five
     songs, scores, and reasons for each of the three taste profiles. -->

<!-- Optional screenshot or video link. -->

---

## Experiments You Tried

### Manual Scoring Check

I applied the baseline scoring rule by hand to three songs for the
High-Energy Pop profile. Sunrise City scored highest among the three
because it matched both genre and mood and was only `0.03` away from the
energy target. Gym Hero scored higher than Rooftop Lights because its
exact `pop` match earned two points, while Rooftop Lights earned one point
for matching the `happy` mood.

### Manual Weight Comparison

I compared two weighting strategies by hand for the High-Energy Pop
profile. Both strategies used the same energy similarity formula and
kept the energy weight at `1.0`.

| Strategy | Genre weight | Mood weight | Energy weight | Gym Hero | Rooftop Lights |
|---|---:|---:|---:|---:|---:|
| Baseline | 2.0 | 1.0 | 1.0 | 2.92 | 1.91 |
| Mood-first | 1.0 | 2.0 | 1.0 | 1.92 | 2.91 |

Gym Hero ranked higher under the baseline because its genre matched.
Rooftop Lights ranked higher under the mood-first strategy because its
mood matched. Their energy similarity scores differed by only `0.01`.
Changing the genre and mood weights reversed their order. The simulation
will use the baseline weights.

### Planned Weight Experiment

I will compare the baseline with a version that lowers the genre weight
from `2.0` to `1.0` and raises the energy weight from `1.0` to `2.0`.
The mood weight will stay at `1.0`. I will use the same catalog and
profiles for both runs to see how the new weights affect the scores
and top-five rankings.

<!-- After running the CLI experiment, record before-and-after ranks or
     scores for specific songs and explain what changed. -->

---

## Limitations and Risks

- The small catalog limits the range of songs the system can suggest.
- Each profile represents one favorite genre, one favorite mood, and one
  energy target. Someone who enjoys both chill lofi and chill ambient
  can specify only one favorite genre per profile.
- Exact genre matching treats `pop` and `indie pop` as separate labels.
  Combined with the two-point genre bonus, this can limit discovery
  across related genres.
- The score relies on the catalog's labels and energy values. Evaluating
  whether the suggestions fit real listeners would require their feedback.

---

## Reflection

See the [Model Card](model_card.md) for the evaluation and further
discussion of the system's limitations.

Calculating the scores by hand helped me see how a recommender turns song
attributes and user preferences into a ranked list. The individual scores
showed how each song fit the profile, and comparing the totals showed why
some songs appeared above others.

The comparison between Gym Hero and Rooftop Lights showed me how the
weights and genre labels can shape what a listener discovers. With the
baseline weights, an intense pop song ranked above a happy indie-pop song
for someone looking for happy pop. Giving mood more weight reversed their
order in my hand calculation. Next, I want to see whether increasing the
energy weight changes which songs appear in the top five.