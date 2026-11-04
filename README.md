# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a music recommender simulation that suggests songs based
on a listener's favorite genre, favorite mood, and target energy. It
compares those preferences with song attributes in a CSV catalog, ranks
the songs by score, and explains what contributed to each recommendation.

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
defined in the program.

- **Song.** Each record contains `id`, `title`, `artist`, `genre`, `mood`,
  `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
  The scoring rule uses `genre`, `mood`, and `energy`.
- **UserProfile.** The scoring rule reads `favorite_genre`, `favorite_mood`,
  and `target_energy` from the profile.
- **Recommender.** The recommender scores each song, records the reasons
  for its score, and returns the five highest-scoring songs.

### Taste Profiles

| Profile | Favorite genre | Favorite mood | Target energy |
|---|---|---|---:|
| High-Energy Pop | `pop` | `happy` | 0.85 |
| Chill Lofi | `lofi` | `chill` | 0.25 |
| Deep Intense Rock | `rock` | `intense` | 0.90 |

Storm Runner matches the Deep Intense Rock profile's genre and mood.
Its energy of `0.91` is only `0.01` above the target. Library Rain matches
the Chill Lofi profile's genre and mood and has an energy of `0.35`,
which is `0.10` above its target.

### Algorithm Recipe

1. Add **2.0 points** for an exact genre match.
2. Add **1.0 point** for an exact mood match.
3. Add `1.0 - abs(song_energy - target_energy)` for energy similarity.
   Songs closer to the target earn more points. An exact energy match
   earns **1.0 point**.
4. Sort the songs from highest to lowest score and show the top five.
   Songs with equal scores keep their original CSV order.

The maximum score is **4.0**. The two-point genre bonus can put a song
from the preferred genre above one that better matches the requested
mood. Gym Hero gets the full genre bonus for `pop`, while Rooftop Lights
receives zero genre points because its label is `indie pop`.

**Data flow**

`Song catalog + taste profile → score each song and record reasons → sort by score → display the top five`

---

## Getting Started

### Setup

Run these commands from the project folder on Windows.

1. Create a virtual environment if you need one.

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

Run the starter tests from the project folder. If your virtual environment
needs `pytest`, install it with `python -m pip install pytest`.

```cmd
python -m pytest
```

The two starter tests in `tests/test_recommender.py` passed during baseline
verification.

---

## Sample Recommendation Output

Running `python -m src.main` produced the following results with the
baseline weights.

```text
Loaded songs: 18

High-Energy Pop - Top 5 Recommendations
Favorite genre: pop | Favorite mood: happy | Target energy: 0.85
1. Sunrise City | Score: 3.97
   Reasons: genre match (+2.00), mood match (+1.00), energy similarity (+0.97)
2. Gym Hero | Score: 2.92
   Reasons: genre match (+2.00), energy similarity (+0.92)
3. Rooftop Lights | Score: 1.91
   Reasons: mood match (+1.00), energy similarity (+0.91)
4. Dancing After Dark | Score: 0.99
   Reasons: energy similarity (+0.99)
5. Neon Tide | Score: 0.97
   Reasons: energy similarity (+0.97)

Chill Lofi - Top 5 Recommendations
Favorite genre: lofi | Favorite mood: chill | Target energy: 0.25
1. Library Rain | Score: 3.90
   Reasons: genre match (+2.00), mood match (+1.00), energy similarity (+0.90)
2. Midnight Coding | Score: 3.83
   Reasons: genre match (+2.00), mood match (+1.00), energy similarity (+0.83)
3. Focus Flow | Score: 2.85
   Reasons: genre match (+2.00), energy similarity (+0.85)
4. Spacewalk Thoughts | Score: 1.97
   Reasons: mood match (+1.00), energy similarity (+0.97)
5. Coffee Shop Stories | Score: 0.88
   Reasons: energy similarity (+0.88)

Deep Intense Rock - Top 5 Recommendations
Favorite genre: rock | Favorite mood: intense | Target energy: 0.90
1. Storm Runner | Score: 3.99
   Reasons: genre match (+2.00), mood match (+1.00), energy similarity (+0.99)
2. Gym Hero | Score: 1.97
   Reasons: mood match (+1.00), energy similarity (+0.97)
3. Winter Signal | Score: 1.00
   Reasons: energy similarity (+1.00)
4. Neon Tide | Score: 0.98
   Reasons: energy similarity (+0.98)
5. Dancing After Dark | Score: 0.96
   Reasons: energy similarity (+0.96)
```

---

## Experiments You Tried

### Manual Scoring Check

I applied the baseline scoring rule by hand to three songs for the
High-Energy Pop profile. Sunrise City scored highest because it matched
both genre and mood and was only `0.03` away from the energy target.
Gym Hero scored higher than Rooftop Lights because its exact `pop` match
earned two points, while Rooftop Lights earned one point for matching the
`happy` mood.

### Manual Weight Comparison

I compared two weighting strategies by hand for the High-Energy Pop
profile. Both used the same energy similarity formula and kept the
energy weight at `1.0`.

| Strategy | Genre weight | Mood weight | Energy weight | Gym Hero | Rooftop Lights |
|---|---:|---:|---:|---:|---:|
| Baseline | 2.0 | 1.0 | 1.0 | 2.92 | 1.91 |
| Mood-first | 1.0 | 2.0 | 1.0 | 1.92 | 2.91 |

Gym Hero ranked higher with the baseline because its genre matched.
Rooftop Lights ranked higher with the mood-first weights because its
mood matched. Their energy similarity scores differed by only `0.01`,
so the change in genre and mood weights reversed their order.

### CLI Weight Experiment

I ran the same 18-song catalog and three taste profiles with two sets
of weights. In the second run, I reduced the genre weight from `2.0`
to `1.0` and increased the energy weight from `1.0` to `2.0`. The mood
weight stayed at `1.0`.

| Chill Lofi recommendation | Baseline rank | Baseline score | Experiment rank | Experiment score |
|---|---:|---:|---:|---:|
| Spacewalk Thoughts | 4 | 1.97 | 3 | 2.94 |
| Focus Flow | 3 | 2.85 | 4 | 2.70 |

Spacewalk Thoughts overtook Focus Flow because it matched the `chill`
mood and its energy of `0.28` was only `0.03` away from the target of
`0.25`. Focus Flow matched the `lofi` genre, had a `focused` mood, and
its energy of `0.40` was `0.15` away from the target. The revised order
better reflects the requested mood and low energy. The baseline order
gives the listener's genre preference more influence.

Library Rain stayed first for Chill Lofi. High-Energy Pop and Deep
Intense Rock kept the same top-five order, although their scores changed.
The sample output above uses the baseline weights.

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

See the [Model Card](model_card.md) for the profile comparisons, edge-case
test, and further discussion of the system's limitations.

Calculating scores by hand helped me understand how a recommender turns
song attributes and user preferences into a ranked list. I used an AI
coding assistant to compare scoring strategies and work through the
implementation. I checked the sample scores by hand, verified the catalog
size, and ran the starter tests.

I was surprised that Gym Hero ranked above Rooftop Lights for a listener
looking for happy pop. The exact genre bonus outweighed the mood match.
The CLI experiment showed how weighting energy more heavily could bring
a song from another genre higher in the list when it matched the mood
and came closer to the target energy. Next, I would collect listener
ratings to compare which weighting strategy people find more relevant.