import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple


GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0

# Weights are ordered as genre, mood, and energy.
SCORING_MODES = {
    "genre-first": (GENRE_WEIGHT, MOOD_WEIGHT, ENERGY_WEIGHT),
    "energy-focused": (1.0, 1.0, 2.0),
}


@dataclass
class Song:
    """Represents a song and its attributes."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: float = 0.0
    release_decade: str = ""
    detailed_mood: str = ""
    instrumentalness: float = 0.0
    vocal_language: str = ""


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_release_decade: str = ""
    target_detailed_mood: str = ""
    target_instrumentalness: float | None = None
    target_vocal_language: str = ""


class Recommender:
    """Provides the class-based interface for music recommendations."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs in descending score order."""
        user_prefs = asdict(user)
        ranked_songs = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, asdict(song))[0],
            reverse=True,
        )
        return ranked_songs[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain the points a song earned for this user."""
        _, reasons = score_song(asdict(user), asdict(song))
        return ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load song dictionaries from a CSV file and convert numeric fields."""
    numeric_fields = (
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "popularity",
        "instrumentalness",
    )

    with open(csv_path, encoding="utf-8-sig", newline="") as csv_file:
        songs = list(csv.DictReader(csv_file))

    for song in songs:
        song["id"] = int(song["id"])
        for field in numeric_fields:
            song[field] = float(song[field])

    return songs


def score_song(
    user_prefs: Dict, song: Dict, *, mode: str = "genre-first", advanced: bool = False
) -> Tuple[float, List[str]]:
    """Return a song's relevance score and explanation reasons."""
    genre_weight, mood_weight, energy_weight = SCORING_MODES[mode]
    score = 0.0
    reasons = []

    genre = song["genre"].strip().casefold()
    favorite_genre = user_prefs["favorite_genre"].strip().casefold()
    if genre == favorite_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.2f})")

    mood = song["mood"].strip().casefold()
    favorite_mood = user_prefs["favorite_mood"].strip().casefold()
    if mood == favorite_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.2f})")

    energy_gap = abs(song["energy"] - user_prefs["target_energy"])
    energy_points = energy_weight * (1.0 - energy_gap)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    if advanced:
        popularity_points = 0.25 * song.get("popularity", 0.0) / 100.0
        score += popularity_points
        reasons.append(f"popularity (+{popularity_points:.2f})")

        target_decade = str(user_prefs.get("target_release_decade", "")).strip().casefold()
        song_decade = str(song.get("release_decade", "")).strip().casefold()
        if target_decade and song_decade == target_decade:
            score += 0.20
            reasons.append("release decade match (+0.20)")

        target_detailed = str(user_prefs.get("target_detailed_mood", "")).strip().casefold()
        song_detailed = str(song.get("detailed_mood", "")).strip().casefold()
        if target_detailed and song_detailed == target_detailed:
            score += 0.20
            reasons.append("detailed mood match (+0.20)")

        target_instrumental = user_prefs.get("target_instrumentalness")
        if target_instrumental is not None:
            instrumental_gap = abs(song["instrumentalness"] - float(target_instrumental))
            instrumental_points = 0.20 * (1.0 - instrumental_gap)
            score += instrumental_points
            reasons.append(f"instrumentalness similarity (+{instrumental_points:.2f})")

        target_language = str(user_prefs.get("target_vocal_language", "")).strip().casefold()
        song_language = str(song.get("vocal_language", "")).strip().casefold()
        if target_language and song_language == target_language:
            score += 0.20
            reasons.append("vocal language match (+0.20)")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    *,
    mode: str = "genre-first",
    diversity: bool = False,
    advanced: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs with scores and explanations."""
    limit = max(0, k)

    # Score each song once before optional diversity selection begins.
    scored = []
    for csv_index, song in enumerate(songs):
        base_score, reasons = score_song(user_prefs, song, mode=mode, advanced=advanced)
        scored.append((csv_index, song, base_score, reasons))

    if not diversity:
        ranked = sorted(scored, key=lambda result: result[2], reverse=True)
        return [
            (song, score, ", ".join(reasons))
            for _, song, score, reasons in ranked[:limit]
        ]

    remaining = scored.copy()
    selected_artists = set()
    recommendations = []

    while remaining and len(recommendations) < limit:
        best_index = None
        best_tuple = None
        best_adjusted_score = None
        best_penalty_reason = None

        # Iterating in CSV order makes the first best candidate win ties.
        for candidate_index, (_, song, base_score, reasons) in enumerate(remaining):
            artist = song["artist"].strip().casefold()
            adjusted_score = base_score
            penalty_reason = None

            if artist in selected_artists:
                adjusted_score -= 0.50
                penalty_reason = "artist diversity penalty (-0.50)"

            if (
                best_adjusted_score is None
                or adjusted_score > best_adjusted_score
            ):
                best_index = candidate_index
                best_tuple = (_, song, base_score, reasons)
                best_adjusted_score = adjusted_score
                best_penalty_reason = penalty_reason

        _, song, _, reasons = best_tuple
        selected_artist = song["artist"].strip().casefold()
        selected_artists.add(selected_artist)

        explanation_reasons = reasons.copy()
        if best_penalty_reason:
            explanation_reasons.append(best_penalty_reason)
        recommendations.append(
            (song, best_adjusted_score, ", ".join(explanation_reasons))
        )
        remaining.pop(best_index)

    return recommendations