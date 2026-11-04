# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 recommends songs based on a listener's favorite genre,
favorite mood, and target energy. It compares those preferences with song
attributes in a CSV catalog, ranks the songs by score, and explains what
contributed to each recommendation.

The catalog contains 18 songs, including 10 starter songs and eight
fictional additions. Optional flags let users include advanced song
features, select a scoring mode, encourage artist diversity, or display
the results as a table.

---

## How The System Works

Real-world recommenders can use collaborative filtering to suggest items
that people with similar listening habits enjoy. They can also use
content-based filtering to compare item features with a listener's
preferences. VibeFinder uses content-based filtering with taste profiles
defined in the program.

- **Song.** The original CSV fields are `id`, `title`, `artist`, `genre`,
  `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
  The default score uses genre, mood, and energy. The artist diversity
  option uses `artist` during ranking. Advanced scoring uses five
  additional fields documented below.
- **UserProfile.** The default scoring rule reads `favorite_genre`,
  `favorite_mood`, and `target_energy` from the profile.
- **Recommender.** The recommender scores each song, ranks the candidates,
  and returns the top five with an explanation for each score.

### Taste Profiles

| Profile | Favorite genre | Favorite mood | Target energy |
|---|---|---|---:|
| High-Energy Pop | `pop` | `happy` | 0.85 |
| Chill Lofi | `lofi` | `chill` | 0.25 |
| Deep Intense Rock | `rock` | `intense` | 0.90 |

Storm Runner matches the Deep Intense Rock profile's genre and mood.
Its energy of `0.91` is `0.01` above the target. Library Rain matches
the Chill Lofi profile's genre and mood. Its energy of `0.35` is `0.10`
above that profile's target.

### Algorithm Recipe

The default Genre-First run uses these rules.

1. Add **2.0 points** for an exact genre match.
2. Add **1.0 point** for an exact mood match.
3. Add `1.0 - abs(song_energy - target_energy)` for energy similarity.
   Songs closer to the target earn more points. An exact energy match
   earns **1.0 point**.
4. Sort the songs from highest to lowest score and show the top five.
   Songs with equal scores keep their original CSV order.

The maximum base score is **4.0** before advanced feature contributions
or artist diversity adjustments. In Genre-First mode, the two-point
genre bonus can put a song from the preferred genre above one that better
matches the requested mood. Gym Hero earns the genre bonus for `pop`,
while Rooftop Lights earns zero genre points for its `indie pop` label.

**Data flow**

`Song catalog + taste profile → score each song and record reasons → rank candidates → display the top five`

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

### Optional Challenge 1 — Advanced Song Features

Use `--advanced` to include five additional fields in scoring. All 18
songs have values for these fields. The values are illustrative metadata
for the simulation.

| CSV field | Contribution to the advanced score |
|---|---|
| `popularity` | Adds points based on a popularity value from 0 to 100. |
| `release_decade` | Adds a bonus when the release decade matches the profile's preference. |
| `detailed_mood` | Adds a bonus when the more specific mood label matches the profile's preference. |
| `instrumentalness` | Adds similarity points based on how close the song's 0–1 value is to the profile's target. |
| `vocal_language` | Adds a bonus when the vocal-language label matches the profile's preference. The catalog uses `Instrumental` for tracks tagged without vocals. |

```cmd
python -m src.main --advanced
python -m src.main --advanced --mode energy-focused --diversity --table
```

For Chill Lofi, Midnight Coding moved from **#2 at 3.83** in the default
run to **#1 at 4.81** with `--advanced`. Its explanation showed
contributions from all five fields. A separate check held the profile
fixed and changed one field at a time on a copy of Midnight Coding.
Each of the five changes affected the score independently.

The combined command also worked. Midnight Coding ranked **#1 at 4.64**,
and Focus Flow ranked **#4 at 2.99** with `artist diversity penalty (-0.50)`
visible in the table.

See the [AI Interactions Log](ai_interactions.md) for the prompts and
individual feature checks.

### Optional Challenge 2 — Multiple Scoring Modes

The app defaults to Genre-First. Select Energy-Focused with `--mode` to
give energy similarity more weight. Both modes use the same base scoring
formula with different weights.

| Mode | Genre weight | Mood weight | Energy weight |
|---|---:|---:|---:|
| Genre-First (default) | 2.0 | 1.0 | 1.0 |
| Energy-Focused | 1.0 | 1.0 | 2.0 |

```cmd
python -m src.main
python -m src.main --mode energy-focused
```

For Chill Lofi, Focus Flow ranks third in Genre-First mode. In
Energy-Focused mode, Spacewalk Thoughts moves from fourth to third.

### Optional Challenge 3 — Artist Diversity

Use `--diversity` to apply a **0.50-point penalty** when a candidate's
artist already appears in the selected recommendations. The app selects
one song at a time using the adjusted scores. The penalty applies once
per candidate and appears in the explanation. A repeat artist can still
appear if the adjusted score is high enough.

```cmd
python -m src.main --diversity
python -m src.main --mode energy-focused --diversity
```

For Chill Lofi, Midnight Coding was selected before Focus Flow. Both
songs are by LoRoom, so Focus Flow received the penalty in both modes.

| Scoring mode | Focus Flow without diversity | Focus Flow with diversity |
|---|---|---|
| Genre-First | Rank 3, score 2.85 | Rank 3, score 2.35 |
| Energy-Focused | Rank 4, score 2.70 | Rank 4, score 2.20 |

Both diversity runs displayed `artist diversity penalty (-0.50)` in
Focus Flow's explanation.

### Optional Challenge 4 — Visual Summary Table

Use `--table` to display **Rank**, **Song**, **Artist**, **Score**, and
**Reasons** in aligned columns. Long explanations wrap within the Reasons
column. The default command uses the original list format. Both formats
display the same rankings and scores for the selected options.

```cmd
python -m src.main --table
python -m src.main --mode energy-focused --diversity --table
```

I verified the table for all three profiles. In the Energy-Focused run
with artist diversity and table output, Focus Flow ranked fourth for
Chill Lofi at **2.20**. Its wrapped explanation included
`artist diversity penalty (-0.50)`.

### Running Tests

Run the starter tests from the project folder. If your virtual environment
needs `pytest`, install it with `python -m pip install pytest`.

```cmd
python -m pytest
```

Both starter tests in `tests/test_recommender.py` passed after the advanced
song features update.

---

## Sample Recommendation Output

Running `python -m src.main` produced the following results in the default
list format, with Genre-First weights and the optional scoring adjustments
disabled.

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
weight stayed at `1.0`. I later verified the same results using the
selectable Energy-Focused mode.

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

---

## Limitations and Risks

- The small catalog limits the range of songs the system can suggest.
- Each baseline profile represents one favorite genre, one favorite mood,
  and one energy target. Someone who enjoys both chill lofi and chill
  ambient can specify only one favorite genre per profile.
- Exact genre matching treats `pop` and `indie pop` as separate labels.
  Combined with the two-point genre bonus in the default mode, this can
  limit discovery across related genres.
- The artist penalty considers repeat artists within a recommendation
  list. A track with a strong base score can still rank ahead of a track
  by a different artist after the penalty.
- The advanced metadata is illustrative. Popularity points can favor
  songs with higher assigned values, and evaluating whether the rankings
  fit real listeners would require their feedback.

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
and came closer to the target energy. The advanced run showed how
additional preferences could move Midnight Coding ahead of Library Rain
even though both tracks already matched the requested genre and mood.
Next, I would collect listener ratings to compare which scoring choices
people find more relevant.