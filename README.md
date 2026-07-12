# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How Systems Usually Work

Systems such as Spotify and Youtube use a variety of factors for recommending songs to users but both leverage vector embeddings.
These embeddings combine both direct media features (tempo, energy, acousticness, etc.) with some aspect of personalization (skipped, repeated, watched for X minutes).
Overall, they rely more heavily on implicit signals (time spent and interactions) to predict satisfaction better than direct ratings metrics.

Audio features include:
* Tempo — BPM. Fast vs. slow.
* Energy — intensity/activity. 0-1 scale. Rock = high, ballad = low.
* Danceability — rhythmic regularity. How groove-friendly.
* Acousticness — unplugged. 0-1, 1 = fully acoustic.
* Valence — mood brightness. High = happy/upbeat, low = sad/angry.
* Instrumentalness — no vocals. 0-1, 1 = pure instrumental.
* Speechiness — spoken words ratio. Podcasts = high, songs = low.
* Liveness — crowd/live performance detected.
* Loudness — decibels. Normalized across catalog.
* Key — musical key (C, D, E, etc.). 0-11 encoding.
* Mode — major vs. minor. 0 or 1.

Metadata features, on the other hand, include:
* Genre — broad category (indie, hip-hop, metal, pop)
* Subgenre — finer classification
* Artist — creator. Enables artist-to-artist similarity.
* Popularity — 0-100 score from streams. Bias risk.
* Release date — recency
* Duration — song length

### How My System Works

<!-- Explain your design in plain language.

Some prompts to answer: -->

<!-- - What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo -->
<!-- - What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend -->

<!-- You can include a simple diagram or bullet list if helpful. -->

#### Input Data

My song recommender leverages 4 core features:

1. **Genre** — broad buckets (pop vs lofi vs rock = different vibes)
1. **Mood** — maps to user taste directly. User says "I want chill" = match mood=chill
1. **Energy** — separates intensity within genre (pop happy 0.82 vs pop intense 0.93)
1. **Danceability** — captures rhythm appeal independent of genre/mood

We focused on these 4 because of their correlation to the valence, tempo, and accousticness metrics.

Each **UserProfile** stores simple data about the user including favorite genre, mood, energy level, and acoustic preference.

#### Scoring and Ranking

There are separate scoring and ranking rules to separate concerns.
The scoring rule is responsible for figuring out the best recommendations while the ranking rule is responsible for actually making the recommendation.
This gives us maximum flexibility to adjust how we select songs and the scoring weights independently. 

The recommender computes song scores with a simple greatest sum:

```
Score = (genre_match × 25) + (mood_match × 50) + (energy_distance × 25)

where:
  genre_match = 1 if song.genre == user.genre, else 0
  mood_match = 1 if song.mood == user.mood, else 0
  energy_distance = 1 - |song.energy - user.target_energy|
```
Once we have the scores, the recommendation follows a mood-dominant approach to match the intended user sentiment. This way we can offer users a variety of songs they'd enjoy without locking them into a single genre.

The ranking algorithm follows as
```
1. Pick song with highest score → add to results
2. For each remaining song:
     relevance = score
     diversity = distance from all picked songs (genre/mood/energy)
     combined = (0.7 × relevance) + (0.3 × diversity)
3. Pick highest combined, repeat until top N
```
While this is slower than strictly taking the top N or some simpler algorithms, it prioritizes offering our users a broader exposure to songs. As long as the algorithm is not unreasonably slow, I believe users will appreciate better recommendations over faster but worse playlists.

---

### Sample Recommendation Output

```
============================================================
Top Recommendations for Jordan
============================================================

1. Midnight Coding
   Artist: LoRoom
   Genre:  lofi
   Score:  99.7/100
   Why:    matches genre lofi
           matches mood chill
           energy 0.4 fits your preference

2. Library Rain
   Artist: Paper Lanterns
   Genre:  lofi
   Score:  99.2/100
   Why:    matches genre lofi
           matches mood chill
           energy 0.3 fits your preference

3. Spacewalk Thoughts
   Artist: Orbit Bloom
   Genre:  ambient
   Score:  63.2/100
   Why:    matches mood chill
           energy 0.3 fits your preference

4. Deep House
   Artist: House Vibes
   Genre:  deep house
   Score:  60.8/100
   Why:    matches mood chill
           energy 0.7 fits your preference

5. Focus Flow
   Artist: LoRoom
   Genre:  lofi
   Score:  50.0/100
   Why:    matches genre lofi
           energy 0.4 fits your preference

============================================================
```

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



