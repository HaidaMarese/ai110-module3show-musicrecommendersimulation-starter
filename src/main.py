"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog and displays ranked recommendations for three
taste profiles. Optional Challenge 2 lets users choose a scoring mode
with the --mode command-line argument.
"""

import argparse
import textwrap

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
    parser.add_argument(
        "--table",
        action="store_true",
        help="Display recommendations in aligned table format.",
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

        if args.table:
            print_recommendation_table(recommendations)
        else:
            for rank, (song, score, explanation) in enumerate(recommendations, start=1):
                print(f"{rank}. {song['title']} | Score: {score:.2f}")
                print(f"   Reasons: {explanation}")


def print_recommendation_table(recommendations) -> None:
    """Print recommendations as aligned columns with wrapped explanations."""
    columns = (4, 24, 20, 7, 42)
    headers = ("Rank", "Song", "Artist", "Score", "Reasons")

    def format_row(values):
        return "  ".join(
            str(value).ljust(width)[:width]
            for value, width in zip(values, columns)
        ).rstrip()

    print(format_row(headers))
    print(format_row(("-" * columns[0], "-" * columns[1], "-" * columns[2], "-" * columns[3], "-" * columns[4])))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        song_lines = textwrap.wrap(str(song["title"]), width=columns[1], break_long_words=False, break_on_hyphens=False) or [""]
        artist_lines = textwrap.wrap(str(song["artist"]), width=columns[2], break_long_words=False, break_on_hyphens=False) or [""]
        reason_lines = textwrap.wrap(explanation, width=columns[4], break_long_words=False, break_on_hyphens=False) or [""]
        row_height = max(len(song_lines), len(artist_lines), len(reason_lines))

        for line_index in range(row_height):
            rank_value = rank if line_index == 0 else ""
            score_value = f"{score:.2f}" if line_index == 0 else ""
            print(format_row((
                rank_value,
                song_lines[line_index] if line_index < len(song_lines) else "",
                artist_lines[line_index] if line_index < len(artist_lines) else "",
                score_value,
                reason_lines[line_index] if line_index < len(reason_lines) else "",
            )))


if __name__ == "__main__":
    main()