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


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


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
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    with open(csv_path, encoding="utf-8-sig", newline="") as csv_file:
        songs = list(csv.DictReader(csv_file))

    for song in songs:
        song["id"] = int(song["id"])
        for field in numeric_fields:
            song[field] = float(song[field])

    return songs


def score_song(
    user_prefs: Dict, song: Dict, *, mode: str = "genre-first"
) -> Tuple[float, List[str]]:
    """Return a song's relevance score and the reasons for its points."""
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

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    *,
    mode: str = "genre-first",
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs with their scores and explanations."""
    recommendations = []

    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        recommendations.append((song, score, ", ".join(reasons)))

    recommendations.sort(key=lambda result: result[1], reverse=True)
    return recommendations[:max(0, k)]