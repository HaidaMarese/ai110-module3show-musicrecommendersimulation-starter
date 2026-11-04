"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog and displays ranked recommendations for three
taste profiles. Optional Challenge 2 lets users choose a scoring mode
with the --mode command-line argument.
"""

import argparse

from .recommender import SCORING_MODES, load_songs, recommend_songs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rank songs for three taste profiles."
    )
    parser.add_argument(
        "--mode",
        choices=SCORING_MODES,
        default="genre-first",
        help="Choose a scoring mode for Optional Challenge 2 (default: genre-first).",
    )
    parser.add_argument(
        "--diversity",
        action="store_true",
        help="Prefer different artists by subtracting 0.50 after an artist is selected.",
    )
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.25,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
        },
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(
            user_prefs,
            songs,
            k=5,
            mode=args.mode,
            diversity=args.diversity,
        )

        print(f"\n{profile_name} - Top 5 Recommendations")
        print(
            f"Favorite genre: {user_prefs['favorite_genre']} | "
            f"Favorite mood: {user_prefs['favorite_mood']} | "
            f"Target energy: {user_prefs['target_energy']:.2f}"
        )

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} | Score: {score:.2f}")
            print(f"   Reasons: {explanation}")


if __name__ == "__main__":
    main()