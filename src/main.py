"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Usage:
    python -m src.main              # Uses "alex" as default user
    python -m src.main jordan       # Uses "jordan" user profile
    python -m src.main casey        # Uses "casey" user profile
"""

import sys
from .recommender import load_songs, load_user_profiles, recommend_songs, print_recommendations


def main(user_name: str = "alex") -> None:
    songs = load_songs("data/songs.csv")
    profiles = load_user_profiles("data/user_profiles.csv")

    user_name_lower = user_name.lower()
    if user_name_lower in profiles:
        profile = profiles[user_name_lower]
        user_prefs = {
            "genre": profile.get("favorite_genre", "pop"),
            "mood": profile.get("favorite_mood", "happy"),
            "energy": float(profile.get("target_energy", 0.8)),
            "ranking_strategy": profile.get("ranking_strategy", "diversity"),
        }
        print(f"Using profile for {profile.get('name', user_name)}")
    else:
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "ranking_strategy": "diversity"}
        print(f"Profile '{user_name}' not found. Using default preferences.")

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(recommendations, user_name=user_name)


if __name__ == "__main__":
    user_name = sys.argv[1] if len(sys.argv) > 1 else "alex"
    main(user_name)
