from src.recommender import Song, UserProfile, Recommender, RankingStrategy, EXPLAIN_MATCHES_GENRE, EXPLAIN_MATCHES_MOOD
import pytest
from pytest import approx


def make_small_recommender() -> Recommender:
    """Create test recommender with 2 diverse songs."""
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def make_genre_mood_catalog() -> Recommender:
    """Create test recommender with multiple genre/mood combinations."""
    songs = [
        Song(id=1, title="Happy Pop", artist="Artist1", genre="pop", mood="happy", energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi", artist="Artist2", genre="lofi", mood="chill", energy=0.3, tempo_bpm=80, valence=0.5, danceability=0.4, acousticness=0.8),
        Song(id=3, title="Intense Rock", artist="Artist3", genre="rock", mood="intense", energy=0.9, tempo_bpm=140, valence=0.4, danceability=0.6, acousticness=0.1),
        Song(id=4, title="Happy Lofi", artist="Artist4", genre="lofi", mood="happy", energy=0.5, tempo_bpm=90, valence=0.7, danceability=0.5, acousticness=0.7),
        Song(id=5, title="Chill Pop", artist="Artist5", genre="pop", mood="chill", energy=0.4, tempo_bpm=100, valence=0.6, danceability=0.6, acousticness=0.3),
    ]
    return Recommender(songs)


# =============================================================================
# SCORING LOGIC TESTS
# =============================================================================

def test_score_dict_perfect_match():
    """Score should be 100 when genre, mood, and energy all match perfectly."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}

    score = rec._score_dict(user_prefs, song)

    # genre (35) + mood (50) + energy distance (15 * 1.0) = 100
    assert score == 100.0


def test_score_dict_no_matches():
    """Score should be low when nothing matches."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "rock", "mood": "sad", "energy": 0.2}

    score = rec._score_dict(user_prefs, song)

    # 0 + 0 + energy_distance = 15 * (1 - |0.2 - 0.8|) = 15 * 0.4 = 6.0
    # Use approx() to handle floating-point rounding errors from intermediate calculations
    assert score == approx(6.0)


def test_score_dict_genre_match_only():
    """Score should reward genre match while penalizing mood/energy mismatch."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "sad", "energy": 0.2}

    score = rec._score_dict(user_prefs, song)

    # 35 (genre) + 0 (mood) + 15 * (1 - |0.2 - 0.8|) = 35 + 0 + 6 = 41
    assert score == 41.0


def test_score_dict_mood_match_only():
    """Score should heavily reward mood match (50 pts vs 35 for genre)."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "rock", "mood": "happy", "energy": 0.2}

    score = rec._score_dict(user_prefs, song)

    # 0 (genre) + 50 (mood) + 15 * (1 - 0.6) = 0 + 50 + 6 = 56
    assert score == 56.0


def test_score_dict_energy_boundary_min():
    """Energy distance should be clamped correctly at energy=0.0."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.0}
    song = {"genre": "pop", "mood": "happy", "energy": 1.0}

    score = rec._score_dict(user_prefs, song)

    # 35 + 50 + 15 * (1 - |1.0 - 0.0|) = 85 + 0 = 85
    assert score == 85.0


def test_score_dict_energy_boundary_max():
    """Energy distance should be clamped correctly at energy=1.0."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 1.0}
    song = {"genre": "pop", "mood": "happy", "energy": 0.0}

    score = rec._score_dict(user_prefs, song)

    # 35 + 50 + 15 * (1 - |0.0 - 1.0|) = 85 + 0 = 85
    assert score == 85.0


# =============================================================================
# SONG DISTANCE TESTS
# =============================================================================

def test_song_distance_identical_songs():
    """Distance should be 0 for identical songs."""
    rec = make_small_recommender()
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}

    distance = rec._song_distance(song, song)

    assert distance == 0.0


def test_song_distance_different_genre():
    """Distance increases by 1/3 when genre differs."""
    rec = make_small_recommender()
    song1 = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song2 = {"genre": "rock", "mood": "happy", "energy": 0.8}

    distance = rec._song_distance(song1, song2)

    # (1.0 + 0 + 0) / 3 = 0.333...
    assert abs(distance - (1.0 / 3.0)) < 0.001


def test_song_distance_different_mood():
    """Distance increases by 1/3 when mood differs."""
    rec = make_small_recommender()
    song1 = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song2 = {"genre": "pop", "mood": "chill", "energy": 0.8}

    distance = rec._song_distance(song1, song2)

    # (0 + 1.0 + 0) / 3 = 0.333...
    assert abs(distance - (1.0 / 3.0)) < 0.001


def test_song_distance_different_energy():
    """Distance measures energy difference as absolute value."""
    rec = make_small_recommender()
    song1 = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song2 = {"genre": "pop", "mood": "happy", "energy": 0.5}

    distance = rec._song_distance(song1, song2)

    # (0 + 0 + |0.8 - 0.5|) / 3 = 0.3 / 3 = 0.1
    assert abs(distance - 0.1) < 0.001


def test_song_distance_all_different():
    """Distance should be high when all attributes differ."""
    rec = make_small_recommender()
    song1 = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song2 = {"genre": "rock", "mood": "chill", "energy": 0.2}

    distance = rec._song_distance(song1, song2)

    # (1.0 + 1.0 + |0.8 - 0.2|) / 3 = 2.6 / 3 = 0.867
    assert abs(distance - (2.6 / 3.0)) < 0.001


# =============================================================================
# RANKING STRATEGY TESTS
# =============================================================================

def test_rank_by_score_returns_top_n():
    """TOP_N ranking should return k highest-scoring songs."""
    rec = make_genre_mood_catalog()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    top_3 = rec._rank_by_score(user_prefs, song_dicts, 3)

    assert len(top_3) == 3
    # Song 1 (pop, happy, 0.8) should be first
    assert top_3[0] == 0  # id=1 is at index 0


def test_rank_by_score_respects_k():
    """TOP_N should return exactly k songs when k < catalog size."""
    rec = make_genre_mood_catalog()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    for k in [1, 2, 3]:
        results = rec._rank_by_score(user_prefs, song_dicts, k)
        assert len(results) == k


def test_rank_by_score_k_exceeds_catalog():
    """TOP_N should cap at catalog size when k > available songs."""
    rec = make_small_recommender()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    results = rec._rank_by_score(user_prefs, song_dicts, k=100)

    assert len(results) == 2  # Only 2 songs available


def test_rank_by_diversity_first_pick_highest_score():
    """Diversity ranking should pick highest score first."""
    rec = make_genre_mood_catalog()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    picked = rec._rank_by_diversity(user_prefs, song_dicts, 5)

    # Song 1 (pop, happy, 0.8) should be first pick
    assert picked[0] == 0


def test_rank_by_diversity_balances_relevance_and_diversity():
    """Diversity ranking should avoid picking similar songs consecutively."""
    rec = make_genre_mood_catalog()
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.3}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    picked = rec._rank_by_diversity(user_prefs, song_dicts, 3)

    assert len(picked) == 3
    # Songs should have variety in genre/mood, not all lofi/chill
    genres = [rec.songs[idx].genre for idx in picked]
    assert len(set(genres)) > 1  # At least 2 different genres


def test_rank_by_diversity_respects_k():
    """Diversity ranking should return exactly k songs."""
    rec = make_genre_mood_catalog()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    for k in [1, 2, 3]:
        results = rec._rank_by_diversity(user_prefs, song_dicts, k)
        assert len(results) == k


def test_rank_by_diversity_deterministic():
    """Diversity ranking should be deterministic (same results on re-run)."""
    rec = make_genre_mood_catalog()
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song_dicts = [
        {"id": s.id, "genre": s.genre, "mood": s.mood, "energy": s.energy}
        for s in rec.songs
    ]

    result1 = rec._rank_by_diversity(user_prefs, song_dicts, 3)
    result2 = rec._rank_by_diversity(user_prefs, song_dicts, 3)

    assert result1 == result2


# =============================================================================
# RECOMMENDATION INTEGRATION TESTS
# =============================================================================

def test_recommend_top_n_strategy():
    """Recommend with TOP_N strategy should use score-only ranking."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        ranking_strategy=RankingStrategy.TOP_N,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_recommend_diversity_strategy():
    """Recommend with DIVERSITY strategy should balance relevance and variety."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        ranking_strategy=RankingStrategy.DIVERSITY,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2


def test_recommend_returns_songs_sorted_by_score():
    """Original test: TOP_N ranking should have pop/happy first."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_recommend_k_equals_zero():
    """Recommend with k=0 should return empty list."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=0)

    assert len(results) == 0


def test_recommend_k_exceeds_catalog():
    """Recommend with k > catalog size should cap at available songs."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=100)

    assert len(results) == 2


def test_recommend_deterministic():
    """Recommend should be deterministic for same user/strategy."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        ranking_strategy=RankingStrategy.TOP_N,
    )
    rec = make_small_recommender()

    results1 = rec.recommend(user, k=2)
    results2 = rec.recommend(user, k=2)

    assert [s.id for s in results1] == [s.id for s in results2]


# =============================================================================
# EXPLANATION GENERATION TESTS
# =============================================================================

def test_explain_recommendation_returns_non_empty_string():
    """Original test: explain_recommendation should return non-empty string."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_explain_includes_genre_match():
    """Explanation should mention genre match when applicable."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]  # Pop song

    explanation = rec.explain_recommendation(user, song)

    assert "pop" in explanation.lower()


def test_explain_includes_mood_match():
    """Explanation should mention mood match when applicable."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]  # Happy song

    explanation = rec.explain_recommendation(user, song)

    assert "happy" in explanation.lower()


def test_explain_includes_energy():
    """Explanation should always mention energy level."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)

    assert "energy" in explanation.lower()


def test_explain_no_genre_match():
    """Explanation should not mention genre when it doesn't match."""
    user = UserProfile(
        favorite_genre="rock",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]  # Pop song, not rock

    explanation = rec.explain_recommendation(user, song)

    assert EXPLAIN_MATCHES_GENRE not in explanation.lower()


def test_explain_no_mood_match():
    """Explanation should not mention mood when it doesn't match."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="chill",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]  # Happy song, not chill

    explanation = rec.explain_recommendation(user, song)

    assert EXPLAIN_MATCHES_MOOD not in explanation.lower()
