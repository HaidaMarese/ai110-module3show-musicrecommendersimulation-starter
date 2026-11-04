# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is a classroom simulation that recommends up to five songs
for a given taste profile. Each result includes a score and an explanation
of what contributed to that score.

The model assumes that a listener can describe what they want using one
favorite genre, one favorite mood, and one target energy level. It is
designed to demonstrate how song attributes and user preferences affect
a ranked list. Production music personalization and predictions about
what real listeners will enjoy are outside its intended use.

---

## 3. How the Model Works

VibeFinder compares each song with the listener's favorite genre,
favorite mood, and target energy.

- A song earns **2 points** when its genre matches the preferred genre.
- It earns **1 point** when its mood matches the preferred mood.
- It earns **up to 1 point** for energy similarity. The model takes the
  distance between the song's energy and the listener's target and
  subtracts that distance from one. An exact match earns the full point.

The model adds these points for a maximum score of **4 points**. It ranks
the songs from highest to lowest score and displays the top five. Songs
with equal scores keep their original catalog order. Each result explains
which features earned points.

I replaced the starter placeholders with logic that loads song records
from the CSV, scores each track, and generates ranked recommendations
with explanations.

---

## 4. Data

The catalog contains **18 songs**. I kept all 10 starter songs and added
eight fictional tracks to expand the range of genres and moods.

The CSV stores each song's ID, title, artist, genre, mood, energy, tempo,
valence, danceability, and acousticness. The model uses genre, mood, and
energy for scoring. Genres include pop, lofi, rock, ambient, jazz, and
indie pop. The additions include electronic, country, soul, metal,
classical, disco, folk, and reggae. Moods include happy, chill, intense,
sad, and nostalgic.

The catalog contains song labels and attributes. Listener ratings,
listening history, and feedback about recommendation quality are absent.

---

## 5. Strengths

The model gives clear results when a track matches the requested genre
and mood and has energy close to the target. **Sunrise City** ranked
first for High-Energy Pop with **3.97**. Its happy mood and energy of
`0.82` fit the profile's target of `0.85`.

**Library Rain** ranked first for Chill Lofi with **3.90**, while
**Storm Runner** ranked first for Deep Intense Rock with **3.99**.
These results fit my intuition because a relaxed lofi profile and an
intense rock profile should produce different suggestions.

The explanations also show why the same song can appeal to different
profiles. **Gym Hero** earned genre points for High-Energy Pop and mood
points for Deep Intense Rock.

---

## 6. Limitations and Bias

The catalog is small, and several genres, including rock, ambient, and
classical, have only one track each. Each profile captures one favorite
genre and mood, which limits how well it represents listeners whose
preferences change with the situation. In the Sad and High Energy test,
the genre bonus placed **Storm Runner** above **Winter Signal**, even
though Winter Signal matched the requested mood and energy exactly.
Repeatedly favoring exact genre matches could create a filter bubble
by reducing exposure to tracks from other genres that fit the listener's
mood. The ranking also leaves out features such as tempo, danceability,
and acousticness.

---

## 7. Evaluation

I ran the CLI with the baseline weights and confirmed that it loaded
18 songs and displayed five recommendations with scores and reasons for
each profile. Both starter tests passed. The README shows the full
baseline output for the three regular profiles.

| Profile | Preferred genre | Preferred mood | Target energy | First recommendation | Score |
|---|---|---|---:|---|---:|
| High-Energy Pop | `pop` | `happy` | 0.85 | Sunrise City | 3.97 |
| Chill Lofi | `lofi` | `chill` | 0.25 | Library Rain | 3.90 |
| Deep Intense Rock | `rock` | `intense` | 0.90 | Storm Runner | 3.99 |

### Profile Comparisons

- **High-Energy Pop and Chill Lofi.** Sunrise City led the pop list
  because it matched both categories and was close to the higher energy
  target. Library Rain led the lofi list because it matched both
  categories and had lower energy.
- **High-Energy Pop and Deep Intense Rock.** Gym Hero ranked second in
  both lists. It earned the genre bonus for the pop profile and the mood
  bonus for the rock profile. Its high energy helped it in both.
- **Chill Lofi and Deep Intense Rock.** Spacewalk Thoughts ranked fourth
  for Chill Lofi because it matched the chill mood and was close to the
  energy target. Winter Signal ranked third for Deep Intense Rock because
  its energy exactly matched the target, earning all of its points from
  energy similarity.

### Manual Weight Comparison

I compared Gym Hero and Rooftop Lights by hand for the High-Energy Pop
profile. With baseline weights, Gym Hero scored **2.92** and Rooftop Lights
scored **1.91**. Giving mood two points and genre one point reversed
their order. Rooftop Lights scored **2.91**, and Gym Hero scored **1.92**.
This showed how a change in weights can change the recommendation even
when the songs and listener preferences stay the same.

### Edge-Case Test

I ran a fourth profile that requested rock, a sad mood, and an energy
level of `0.90`.

```text
Sad and High Energy - Top 5 Recommendations
Favorite genre: rock | Favorite mood: sad | Target energy: 0.90
1. Storm Runner | Score: 2.99
   Reasons: genre match (+2.00), energy similarity (+0.99)
2. Winter Signal | Score: 2.00
   Reasons: mood match (+1.00), energy similarity (+1.00)
3. Rainwashed Letters | Score: 1.51
   Reasons: mood match (+1.00), energy similarity (+0.51)
4. Neon Tide | Score: 0.98
   Reasons: energy similarity (+0.98)
5. Gym Hero | Score: 0.97
   Reasons: energy similarity (+0.97)
```

Storm Runner ranked first because it matched rock and its energy was
only `0.01` above the target. Winter Signal matched the sad mood and hit
the energy target exactly, but it ranked second because its genre is
classical. Rainwashed Letters also matched the sad mood and ranked
third because its energy was farther from the target.

### Planned CLI Weight Experiment

I will rerun the three regular profiles with genre worth one point,
mood worth one point, and energy similarity worth up to two points.
I will keep the catalog and profiles the same for both runs. For Chill
Lofi, I will compare the ranks and scores of Spacewalk Thoughts and
Focus Flow and explain whether the new order fits the profile better
based on my musical judgment.

<!-- Replace this subsection with the observed ranks, scores, and your
     interpretation after running the CLI weight experiment. -->

---

## 8. Future Work

- Allow multiple preferred genres and moods so a profile can reflect more
  than one listening preference.
- Expand the catalog and test whether including a strong cross-genre match
  makes the top five more varied while keeping the recommendations relevant.
- Collect listener ratings to evaluate whether people find the results
  relevant and use that feedback to compare weighting strategies.

---

## 9. Personal Reflection

My biggest learning moment was seeing Gym Hero rank above Rooftop Lights
for the High-Energy Pop profile. I expected a happy song to have an
advantage, but the exact genre match was worth more than the mood match.
Seeing the points separately helped me understand how a few simple rules
can produce recommendations that feel personal and still miss part of
what the listener wants.

I used an AI coding assistant to compare scoring strategies and work
through the Python implementation. I checked the sample scores by hand,
verified that the CSV contained 18 songs, and ran the starter tests.
The project made me think more about how the features and weights behind
a music app shape which songs I discover. Next, I would compare the
rankings with listener ratings to see which weighting choices fit real
preferences.