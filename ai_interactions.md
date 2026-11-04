# AI Interactions Log

> **Stretch features only.** This log covers Optional Challenge 2 — Multiple Scoring Modes.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI assistant to help turn my weight experiment into a feature
that users could select from the command line. I wanted to keep Genre-First
as the default and add an Energy-Focused mode. I applied the suggested
changes in VS Code and ran the verification commands myself.

**Prompts used:**

These are paraphrases of my requests during the coding session.

- Give me the complete `src/recommender.py` with both scoring modes and
  one shared scoring function.
- Update `src/main.py` so users can select a mode from the command line.
  Keep the existing output format and identify this as an optional challenge.
- Help me fix the circular import shown in the terminal traceback.

**What did the agent generate or change?**

- In `src/recommender.py`, the assistant proposed a `SCORING_MODES`
  dictionary that maps each mode to its genre, mood, and energy weights.
- It updated `score_song()` to use the selected weights for both the score
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
that the score explanations showed the points awarded in each mode.

| Song | Genre-First | Energy-Focused |
|---|---|---|
| Focus Flow | #3, 2.85 | #4, 2.70 |
| Spacewalk Thoughts | #4, 1.97 | #3, 2.94 |

I also ran `python -m pytest`. Both starter tests passed.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

I used a lightweight, Strategy-style design. Each mode supplies a named
set of weights to the same scoring function.

**How did AI help you brainstorm or implement it?**

The assistant suggested using a dictionary of named weight sets because
the two modes use the same formula and differ only in their weights.
This let me reuse the scoring and ranking code while keeping the original
Genre-First behavior as the default.

**How does the pattern appear in your final code?**

`SCORING_MODES` in `src/recommender.py` stores the weights in genre, mood,
and energy order. `genre-first` uses `(2.0, 1.0, 1.0)` and
`energy-focused` uses `(1.0, 1.0, 2.0)`. `src/main.py` reads `--mode`
and passes it to `recommend_songs()`. That function passes the mode to
`score_song()`, which looks up the weights and uses them to calculate
the score and explain each contribution.