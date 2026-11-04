# AI Interactions Log

> **Stretch features only.** This log covers all four optional challenges.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

### Optional Challenge 1 — Advanced Song Features

**What task did you give the agent?**

I asked the VS Code coding assistant to add five illustrative attributes
to all 18 songs and use them in scoring when `--advanced` is enabled.
I wanted the default rankings preserved and the new flag to work with
both scoring modes, artist diversity, and table output.

**Prompts used**

> Implement Optional Challenge 1. Add five new columns to all 18 songs in `data/songs.csv`: `popularity` (0–100), `release_decade`, `detailed_mood`, `instrumentalness` (0–1), and `vocal_language`. Preserve the existing rows and columns, and treat the added values as illustrative metadata. Add an `--advanced` option that uses all five attributes in scoring and explains how each contributed. Keep the existing scores and rankings when `--advanced` is omitted. Make the option work with `--mode`, `--diversity`, and `--table`. Show me how to verify that each new attribute can affect a score.

For the follow-up check, I asked the assistant to use the existing scoring
function with the Chill Lofi profile and Midnight Coding. I asked it to
start with a fresh copy of the song for each trial, change one field at a
time, and report the original score, modified score, and difference.

**What did the agent generate or change?**

- In `data/songs.csv`, the assistant added `popularity`, `release_decade`,
  `detailed_mood`, `instrumentalness`, and `vocal_language` as illustrative
  metadata.
- In `src/recommender.py`, it added scoring and explanations for the five
  attributes.
- In `src/main.py`, it added the `--advanced` flag.

**What did you verify or fix manually?**

I reviewed the CSV diff and confirmed that the original 18 songs and
their existing fields were preserved. I ran the default, advanced, and
combined commands from the project folder.

```cmd
python -m src.main
python -m src.main --advanced
python -m src.main --advanced --mode energy-focused --diversity --table
python -m pytest
git diff --check
```

The default run matched the README baseline. For Chill Lofi, Midnight
Coding moved from #2 at 3.83 in the default run to #1 at 4.81 with
`--advanced`. Its explanation showed contributions from all five new
fields. In the combined run, Midnight Coding ranked #1 at 4.64. Focus Flow
ranked #4 at 2.99, and the table showed its
`artist diversity penalty (-0.50)`.

I reviewed the assistant's individual feature checks. The Chill Lofi
profile stayed fixed, and each trial changed one field on a fresh copy
of Midnight Coding. The original advanced score was **4.814**.

| Field changed | Replacement | Modified score | Change from original |
|---|---|---:|---:|
| Popularity | `50` | 4.749 | -0.065 |
| Release decade | `2010s` | 4.614 | -0.200 |
| Detailed mood | `energetic` | 4.614 | -0.200 |
| Instrumentalness | `0.10` | 4.670 | -0.144 |
| Vocal language | `English` | 4.614 | -0.200 |

Each field changed the score independently in this check. Both starter
tests passed, and `git diff --check` reported no whitespace errors.

### Optional Challenge 2 — Multiple Scoring Modes

**What task did you give the agent?**

I asked the AI assistant to help turn my weight experiment into a feature
users could select from the command line. I wanted Genre-First to remain
the default and Energy-Focused to be available as a second mode.
I applied the suggested changes in VS Code and ran the checks myself.

**Prompts used**

These are paraphrases of my requests during the coding session.

- Give me the complete `src/recommender.py` with both scoring modes and
  one shared scoring function.
- Update `src/main.py` so users can select a mode from the command line.
  Keep the existing output format and identify this as an optional challenge.
- Help me fix the circular import shown in the terminal traceback.

**What did the agent generate or change?**

- In `src/recommender.py`, the assistant proposed a `SCORING_MODES`
  dictionary that maps each mode to its genre, mood, and energy weights.
- It updated `score_song()` to use the selected weights in both the score
  and its explanation. It updated `recommend_songs()` to pass the selected
  mode to `score_song()`.
- In `src/main.py`, it added `argparse` support for `--mode` and set
  `genre-first` as the default.

**What did you verify or fix manually?**

I fixed a circular import after the CLI import ended up in
`src/recommender.py`. I kept that import in `src/main.py`, where the CLI
uses it, and kept the scoring definitions in `src/recommender.py`.

I ran `python -m src.main` and `python -m src.main --mode energy-focused`.
Both runs loaded 18 songs. I compared the Chill Lofi rankings and checked
that each explanation showed the points awarded in the selected mode.

| Song | Genre-First | Energy-Focused |
|---|---|---|
| Focus Flow | #3, 2.85 | #4, 2.70 |
| Spacewalk Thoughts | #4, 1.97 | #3, 2.94 |

I ran `python -m pytest`, and both starter tests passed.

### Optional Challenge 3 — Artist Diversity

**What task did you give the agent?**

I asked the VS Code coding assistant to add an optional artist diversity
penalty that works with both scoring modes and preserves the default
rankings when the flag is omitted.

**Prompts used**

> Add Optional Challenge 3 to my music recommender. Add a `--diversity` flag in `src/main.py` that works with both existing scoring modes. In `recommend_songs()`, score each song once using the selected mode. When diversity is enabled, select recommendations one at a time. Subtract 0.50 points from a candidate’s base score if its artist already appears in the selected results. Use the adjusted score to pick the next song, keep CSV order for ties, and display the penalty in the explanation when applied. Use a single penalty per candidate and leave the default rankings and output unchanged when the flag is omitted. Show me how to verify the change using my Chill Lofi profile.

**What did the agent generate or change?**

- In `src/main.py`, the assistant added the `--diversity` flag and passed
  it to `recommend_songs()` along with the selected scoring mode.
- In `src/recommender.py`, it updated `recommend_songs()` to score each
  song once and select recommendations one at a time when diversity is
  enabled. A candidate receives a single 0.50-point deduction if its
  artist already appears in the selected results.
- The recommender uses the adjusted score to select the next song, keeps
  CSV order for tied scores, and includes the deduction in the explanation.

**What did you verify or fix manually?**

I checked the repository path after the assistant requested an edit in
another copy of the project. I continued in the Foundations project on
`experiment/artist-diversity`.

I ran the default command and both diversity commands. The default run
loaded 18 songs and matched the README baseline.

```cmd
python -m src.main
python -m src.main --diversity
python -m src.main --mode energy-focused --diversity
python -m pytest
```

For Chill Lofi, Midnight Coding was selected before Focus Flow. Both
tracks are by LoRoom, so Focus Flow received the penalty in each scoring
mode when diversity was enabled.

| Scoring mode | Focus Flow without diversity | Focus Flow with diversity |
|---|---|---|
| Genre-First | #3, 2.85 | #3, 2.35 |
| Energy-Focused | #4, 2.70 | #4, 2.20 |

Both diversity runs displayed `artist diversity penalty (-0.50)` in
Focus Flow's explanation. Its score dropped by 0.50 and its rank stayed
the same within each mode. Both starter tests passed.

### Optional Challenge 4 — Visual Summary Table

**What task did you give the agent?**

I asked the VS Code coding assistant to add an optional table view for
the top five recommendations. I wanted the table to make scores and
reasons easier to compare across songs.

**Prompts used**

> Add a `--table` flag to `src/main.py` for Optional Challenge 4. Use Python’s standard library to display Rank, Song, Artist, Score, and Reasons in aligned columns. Wrap long explanations and include the artist diversity penalty whenever it applies. Keep the current list format as the default and make `--table` work with `--mode` and `--diversity`.

**What did the agent generate or change?**

The assistant added `--table` and a `print_recommendation_table()` helper
in `src/main.py`. The helper formats the existing recommendation results
as five aligned columns and wraps long explanations under Reasons. The
default command still uses the list format.

**What did you verify or fix manually?**

I ran these commands after the table update.

```cmd
python -m src.main
python -m src.main --table
python -m src.main --mode energy-focused --diversity --table
python -m pytest
```

I confirmed that the default run loaded 18 songs and still printed the
original list. The table showed all five columns for all three profiles.
The baseline table matched the list rankings and scores.

In the combined run, Focus Flow by LoRoom ranked fourth for Chill Lofi
with a score of 2.20. Its wrapped explanation included
`artist diversity penalty (-0.50)`. Both starter tests passed after the
table update.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

For Challenge 2, I used a lightweight, Strategy-style design. Each mode
supplies a named set of weights to the same scoring function.

**How did AI help you brainstorm or implement it?**

The assistant suggested a dictionary of named weight sets because both
modes use the same formula and differ only in their weights. This let me
reuse the scoring and ranking code and keep Genre-First as the default.

**How does the pattern appear in your final code?**

`SCORING_MODES` in `src/recommender.py` stores the weights in genre, mood,
and energy order. `genre-first` uses `(2.0, 1.0, 1.0)` and
`energy-focused` uses `(1.0, 1.0, 2.0)`. `src/main.py` reads `--mode` and
passes it to `recommend_songs()`. That function passes the mode to
`score_song()`, which uses the selected weights to calculate and explain
each contribution.

Challenge 1 adds optional feature contributions during scoring.
Challenge 3 applies the artist penalty during ranking, after
`score_song()` calculates the base score. Challenge 4 formats the ranked
results for display. These steps let the scoring, diversity, and display
options work together.