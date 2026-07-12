import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class RankingStrategy(Enum):
    """Ranking strategy for song recommendations."""
    DIVERSITY = "diversity"
    TOP_N = "top_n"

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    ranking_strategy: RankingStrategy = RankingStrategy.DIVERSITY

class Recommender:
    """
    Core recommendation engine with scoring and ranking logic.
    Required by tests/test_recommender.py
    """
    DIVERSITY_WEIGHT = 0.45
    GENRE_WEIGHT = 35
    MOOD_WEIGHT = 50
    ENERGY_WEIGHT = 15

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_dict(self, user_prefs: Dict, song: Dict) -> float:
        """Score a song against user preferences (0-100 scale)."""
        genre_match = 1.0 if song["genre"] == user_prefs.get("genre", "") else 0.0
        mood_match = 1.0 if song["mood"] == user_prefs.get("mood", "") else 0.0
        target_energy = user_prefs.get("energy", 0.5)
        energy_distance = 1.0 - abs(float(song["energy"]) - target_energy)  # Penalizes energy mismatch

        return (genre_match * self.GENRE_WEIGHT) + (mood_match * self.MOOD_WEIGHT) + (energy_distance * self.ENERGY_WEIGHT)

    def _song_distance(self, song1: Dict, song2: Dict) -> float:
        """Measure dissimilarity between two songs (0-1 scale)."""
        genre_diff = 0.0 if song1["genre"] == song2["genre"] else 1.0
        mood_diff = 0.0 if song1["mood"] == song2["mood"] else 1.0
        energy_diff = abs(float(song1["energy"]) - float(song2["energy"]))
        return (genre_diff + mood_diff + energy_diff) / 3.0

    def _rank_by_score(self, user_prefs: Dict, song_dicts: List[Dict], k: int) -> List[int]:
        """Return top k songs ranked by relevance score only."""
        scores = {i: self._score_dict(user_prefs, song) for i, song in enumerate(song_dicts)}
        sorted_indices = sorted(range(len(song_dicts)), key=lambda i: scores[i], reverse=True)
        return sorted_indices[:k]

    def _rank_by_diversity(self, user_prefs: Dict, song_dicts: List[Dict], k: int) -> List[int]:
        """Greedily select k songs balancing relevance and dissimilarity from already-picked songs."""
        scores = {song["id"]: self._score_dict(user_prefs, song) for song in song_dicts}

        picked_indices = []
        remaining = set(range(len(song_dicts)))

        for _ in range(min(k, len(song_dicts))):
            best_idx = None
            best_combined = -1.0

            for idx in remaining:
                song = song_dicts[idx]
                relevance = scores[song["id"]]

                # Distance defaults to 1.0 (max diversity) for first pick
                if picked_indices:
                    avg_distance = sum(
                        self._song_distance(song, song_dicts[p])
                        for p in picked_indices
                    ) / len(picked_indices)
                else:
                    avg_distance = 1.0

                # Weighted combo of relevance (normalized 0-1) and dissimilarity
                combined = (
                    (1 - self.DIVERSITY_WEIGHT) * (relevance / 100.0) +
                    self.DIVERSITY_WEIGHT * avg_distance
                )

                if combined > best_combined:
                    best_combined = combined
                    best_idx = idx

            if best_idx is not None:
                picked_indices.append(best_idx)
                remaining.remove(best_idx)

        return picked_indices

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Generate k song recommendations based on user profile and selected strategy."""
        song_dicts = [
            {
                "id": s.id,
                "genre": s.genre,
                "mood": s.mood,
                "energy": s.energy,
            }
            for s in self.songs
        ]

        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }

        if user.ranking_strategy == RankingStrategy.TOP_N:
            picked_indices = self._rank_by_score(user_prefs, song_dicts, k)
        else:
            picked_indices = self._rank_by_diversity(user_prefs, song_dicts, k)
        return [self.songs[idx] for idx in picked_indices]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate human-readable explanation for why a song was recommended."""
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
        }
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }

        score = self._score_dict(user_prefs, song_dict)

        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({user.favorite_genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your favorite mood ({user.favorite_mood})")
        reasons.append(f"energy level {song.energy:.1f} fits your preference")

        return f"Score: {score:.1f}/100. {', '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["energy"] = float(row["energy"])
                row["tempo_bpm"] = float(row["tempo_bpm"])
                row["valence"] = float(row["valence"])
                row["danceability"] = float(row["danceability"])
                row["acousticness"] = float(row["acousticness"])
                row["id"] = int(row["id"])
                songs.append(row)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found")
    return songs

def load_user_profiles(csv_path: str) -> Dict[str, Dict]:
    """
    Loads user profiles from CSV file.
    Returns dict mapping user name to preferences.
    """
    profiles = {}
    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").lower()
                if name:
                    row["target_energy"] = float(row.get("target_energy", 0.5))
                    row["likes_acoustic"] = row.get("likes_acoustic", "False").lower() == "true"
                    profiles[name] = row
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found")
    return profiles

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Uses Recommender core logic.
    Required by recommend_songs() and src/main.py
    """
    # Minimal Song objects for Recommender
    dummy_songs = [
        Song(
            id=song.get("id", 0),
            title=song.get("title", ""),
            artist=song.get("artist", ""),
            genre=song.get("genre", ""),
            mood=song.get("mood", ""),
            energy=float(song.get("energy", 0)),
            tempo_bpm=float(song.get("tempo_bpm", 0)),
            valence=float(song.get("valence", 0)),
            danceability=float(song.get("danceability", 0)),
            acousticness=float(song.get("acousticness", 0)),
        )
    ]

    recommender = Recommender(dummy_songs)
    score = recommender._score_dict(user_prefs, song)

    reasons = []
    if song["genre"] == user_prefs.get("genre", ""):
        reasons.append(f"matches genre {user_prefs.get('genre')}")
    if song["mood"] == user_prefs.get("mood", ""):
        reasons.append(f"matches mood {user_prefs.get('mood')}")
    reasons.append(f"energy {float(song['energy']):.1f} fits your preference")

    return score, reasons

def print_recommendations(recommendations: List[Tuple[Dict, float, str]], user_name: str = "User") -> None:
    """
    Print recommendations in clean, readable terminal layout.
    """
    print(f"\n{'='*60}")
    print(f"Top Recommendations for {user_name}")
    print(f"{'='*60}\n")

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        title = song.get("title", "Unknown")
        artist = song.get("artist", "Unknown Artist")
        genre = song.get("genre", "Unknown Genre")
        reasons = explanation.split("; ")

        print(f"{i}. {title}")
        print(f"   Artist: {artist}")
        print(f"   Genre:  {genre}")
        print(f"   Score:  {score:.1f}/100")
        print(f"   Why:    {reasons[0]}")
        for reason in reasons[1:]:
            print(f"           {reason}")
        print()

    print(f"{'='*60}\n")


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional wrapper for recommendation.
    Uses Recommender core logic.
    Supports ranking_strategy in user_prefs (default: diversity).
    Required by src/main.py
    """
    if not songs:
        return []

    # Convert dicts to Song objects for Recommender
    song_objects = [
        Song(
            id=song.get("id", 0),
            title=song.get("title", ""),
            artist=song.get("artist", ""),
            genre=song.get("genre", ""),
            mood=song.get("mood", ""),
            energy=float(song.get("energy", 0)),
            tempo_bpm=float(song.get("tempo_bpm", 0)),
            valence=float(song.get("valence", 0)),
            danceability=float(song.get("danceability", 0)),
            acousticness=float(song.get("acousticness", 0)),
        )
        for song in songs
    ]

    recommender = Recommender(song_objects)

    song_dicts = [
        {
            "id": s["id"],
            "genre": s["genre"],
            "mood": s["mood"],
            "energy": s["energy"],
        }
        for s in songs
    ]

    strategy_str = user_prefs.get("ranking_strategy", "diversity").lower()
    try:
        strategy = RankingStrategy(strategy_str)
    except ValueError:
        strategy = RankingStrategy.DIVERSITY

    if strategy == RankingStrategy.TOP_N:
        picked_indices = recommender._rank_by_score(user_prefs, song_dicts, k)
    else:
        picked_indices = recommender._rank_by_diversity(user_prefs, song_dicts, k)

    results = []
    for idx in picked_indices:
        song = songs[idx]
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        results.append((song, score, explanation))

    return results
