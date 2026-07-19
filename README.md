# 🎵 Music Recommender Simulation

## Project Summary

## KeyPlay 1.0

KeyPlay recommends songs based on a user's favorite genre, current mood, and energy level. It uses a 60-song catalog spanning 41 genres and 21 moods, scored by three weighted features: genre match (35 pts), mood match (50 pts), and energy proximity (0-15 pts). Two ranking modes let users pick between pure top-N recommendations or a diversity-first algorithm that balances relevance with playlist variety. Built as a classroom exploration of how real-world systems like Spotify balance personalization, simplicity, and bias.

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

#### Input Data

My song recommender leverages 3 core features:

1. **Genre** — broad buckets (pop vs lofi vs rock = different vibes)
1. **Mood** — maps to user taste directly. User says "I want chill" = match mood=chill
1. **Energy** — separates intensity within genre (pop happy 0.82 vs pop intense 0.93)

We focused on these 3 because of their correlation to the valence, tempo, and acousticness metrics.

Each **UserProfile** stores simple data about the user including favorite genre, mood, energy level, and acoustic preference.

#### Scoring and Ranking

There are separate scoring and ranking rules to separate concerns.
The scoring rule is responsible for figuring out the best recommendations while the ranking rule is responsible for actually making the recommendation.
This gives us maximum flexibility to adjust how we select songs and the scoring weights independently. 

The recommender computes song scores with a weighted sum:

```
Score = (genre_match × 35) + (mood_match × 50) + (energy_distance × 15)

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
     combined = (0.55 × relevance) + (0.45 × diversity)
3. Pick highest combined, repeat until top N
```
While this is slower than strictly taking the top N or some simpler algorithms, it prioritizes offering our users a broader exposure to songs. As long as the algorithm is not unreasonably slow, I believe users will appreciate better recommendations over faster but worse playlists.

---

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
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

### Output

**Alex** (pop/happy, energy=0.8, diversity ranking):
```
============================================================
Top Recommendations for Alex
============================================================

1. Sunrise City
   Artist: Neon Echo
   Genre:  pop
   Score:  99.7/100
   Why:    matches genre pop
           matches mood happy
           energy 0.8 fits your preference

2. Rooftop Lights
   Artist: Indigo Parade
   Genre:  indie pop
   Score:  64.4/100
   Why:    matches mood happy
           energy 0.8 fits your preference

3. Afrobeats
   Artist: African Rhythms
   Genre:  afrobeats
   Score:  64.1/100
   Why:    matches mood happy
           energy 0.9 fits your preference

4. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  48.0/100
   Why:    matches genre pop
           energy 0.9 fits your preference

5. K-Pop Glory
   Artist: K-Stars
   Genre:  K-pop
   Score:  64.8/100
   Why:    matches mood happy
           energy 0.8 fits your preference

============================================================
```
 - **Explanation:**
 Alex is a happy, high-energy pop fan looking for a diversity songs. Because of this preference, we don't always recommend pop songs or purely happy songs, leading to the `Afrobeats` and `Gym Hero` recommendations mixed in.

**Jordan** (lofi/chill, energy=0.4, top_n ranking):
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
- **Explanation:**
 Jordan is a chill lofi fan desiring purely the most-relevant songs. Because of this preference, we don't look for anything outside the best matching songs, recommending them in a descending scored order.
 Notice that each song stays closely related to Jordan's mood and genre preference, resulting in a homogeneous playlist.

**Casey** (rock/intense, energy=0.92, top_n ranking):
```
============================================================
Top Recommendations for Casey
============================================================

1. Storm Runner
   Artist: Voltline
   Genre:  rock
   Score:  99.8/100
   Why:    matches genre rock
           matches mood intense
           energy 0.9 fits your preference

2. Riff Raff
   Artist: Hard Rockers
   Genre:  rock
   Score:  99.5/100
   Why:    matches genre rock
           matches mood intense
           energy 0.9 fits your preference

3. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  64.8/100
   Why:    matches mood intense
           energy 0.9 fits your preference

4. Hardcore Bass
   Artist: Bass Drop
   Genre:  dubstep
   Score:  64.4/100
   Why:    matches mood intense
           energy 0.9 fits your preference

5. Techno Underground
   Artist: Techno Master
   Genre:  techno
   Score:  64.2/100
   Why:    matches mood intense
           energy 0.9 fits your preference

============================================================
```
- **Explanation:**
Casey is an intense rock fan using top-N ranking to get the best pure matches. The algorithm favors genre and mood hits, which is why the top two recommendations are rock songs. Lower-scoring picks like Gym Hero and Hardcore Bass appear because they match the intense mood and high energy (0.9), even though they're not rock—the mood weight (50 pts) overrides genre mismatches.

**Morgan** (jazz/relaxed, energy=0.45, top_n ranking):
```
============================================================
Top Recommendations for Morgan
============================================================

1. Coffee Shop Stories
   Artist: Slow Stereo
   Genre:  jazz
   Score:  98.8/100
   Why:    matches genre jazz
           matches mood relaxed
           energy 0.4 fits your preference

2. Acoustic Guitar
   Artist: Acoustic Artist
   Genre:  acoustic
   Score:  64.2/100
   Why:    matches mood relaxed
           energy 0.4 fits your preference

3. Blues at Midnight
   Artist: Delta Soul
   Genre:  blues
   Score:  15.0/100
   Why:    energy 0.5 fits your preference

4. Midnight Coding
   Artist: LoRoom
   Genre:  lofi
   Score:  14.5/100
   Why:    energy 0.4 fits your preference

5. Sunset Horizon
   Artist: Indie Dreams
   Genre:  indie rock
   Score:  14.5/100
   Why:    energy 0.5 fits your preference

============================================================
```
- **Explanation:**
Morgan is a relaxed jazz fan using top-N ranking, which explains the homogeneous output. Coffee Shop Stories dominates with a near-perfect score by matching all three criteria (jazz + relaxed + close energy). The steep score drop after song 2 reveals the catalog gap: few songs match both relaxed mood and target energy (0.45). Songs 3–5 get minimal points because they miss mood or genre, making pure energy proximity insufficient to score high.

**River** (pop/happy, energy=0.28, diversity ranking):
```
============================================================
Top Recommendations for River
============================================================

1. Sunrise City
   Artist: Neon Echo
   Genre:  pop
   Score:  91.9/100
   Why:    matches genre pop
           matches mood happy
           energy 0.8 fits your preference

2. Rooftop Lights
   Artist: Indigo Parade
   Genre:  indie pop
   Score:  57.8/100
   Why:    matches mood happy
           energy 0.8 fits your preference

3. Afrobeats
   Artist: African Rhythms
   Genre:  afrobeats
   Score:  56.3/100
   Why:    matches mood happy
           energy 0.9 fits your preference

4. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  40.2/100
   Why:    matches genre pop
           energy 0.9 fits your preference

5. K-Pop Glory
   Artist: K-Stars
   Genre:  K-pop
   Score:  57.0/100
   Why:    matches mood happy
           energy 0.8 fits your preference

============================================================
```
- **Explanation:**
River is a happy pop fan using diversity ranking despite low target energy (0.28). Sunrise City leads with high relevance, but diversity ranking pulls in Rooftop Lights, Afrobeats, and K-Pop Glory to expose different genres. All maintain happy mood, but the algorithm intentionally picks varied genres over pure energy matches, giving River a richer playlist than strict top-N would allow.

#### Comments about Outputs
For each recommendation, we're heavily weighting towards current mood and genre preference. This helps explain why each persona's top song is of their favorite genre. Additionally, these users are rather congruent with their genre, meaning that those who like pop are "happy," the person who likes rock is "intense," and the lofi fan is "chill." These match nicely, lending themselves to straightforward music recommendations.

Tests breaking this genre-and-mood pairing are listed below, offering better overall tests of the recommendation system.

### Adversarial Test Results

These profiles test edge cases and potential scoring vulnerabilities:

**Shadow** (darkwave/celebratory, energy=0.75 — impossible genre/mood combo):
```
============================================================
Top Recommendations for Shadow
============================================================

1. Night Drive Loop
   Artist: Neon Echo
   Genre:  synthwave
   Score:  15.0/100
   Why:    energy 0.8 fits your preference

2. Quiet Moments
   Artist: Soft Piano
   Genre:  classical
   Score:  6.7/100
   Why:    energy 0.2 fits your preference

3. Thunderstorm
   Artist: Iron Anvil
   Genre:  metal
   Score:  12.0/100
   Why:    energy 0.9 fits your preference

4. Rooftop Lights
   Artist: Indigo Parade
   Genre:  indie pop
   Score:  14.8/100
   Why:    energy 0.8 fits your preference

5. Neon Nights
   Artist: Synth Wave Master
   Genre:  synth-pop
   Score:  14.5/100
   Why:    energy 0.7 fits your preference

============================================================
```

**Absolute Min** (pop/happy, energy=0.01 — minimum energy boundary):
```
============================================================
Top Recommendations for Absolute min
============================================================

1. Sunrise City
   Artist: Neon Echo
   Genre:  pop
   Score:  87.8/100
   Why:    matches genre pop
           matches mood happy
           energy 0.8 fits your preference

2. Rooftop Lights
   Artist: Indigo Parade
   Genre:  indie pop
   Score:  53.8/100
   Why:    matches mood happy
           energy 0.8 fits your preference

3. K-Pop Glory
   Artist: K-Stars
   Genre:  K-pop
   Score:  53.0/100
   Why:    matches mood happy
           energy 0.8 fits your preference

4. Afrobeats
   Artist: African Rhythms
   Genre:  afrobeats
   Score:  52.2/100
   Why:    matches mood happy
           energy 0.9 fits your preference

5. Major Success
   Artist: Pop Stars Inc
   Genre:  pop
   Score:  38.1/100
   Why:    matches genre pop
           energy 0.8 fits your preference

============================================================
```

**Absolute Max** (pop/happy, energy=0.99 — maximum energy boundary):
```
============================================================
Top Recommendations for Absolute max
============================================================

1. Sunrise City
   Artist: Neon Echo
   Genre:  pop
   Score:  97.5/100
   Why:    matches genre pop
           matches mood happy
           energy 0.8 fits your preference

2. Afrobeats
   Artist: African Rhythms
   Genre:  afrobeats
   Score:  63.0/100
   Why:    matches mood happy
           energy 0.9 fits your preference

3. K-Pop Glory
   Artist: K-Stars
   Genre:  K-pop
   Score:  62.3/100
   Why:    matches mood happy
           energy 0.8 fits your preference

4. Rooftop Lights
   Artist: Indigo Parade
   Genre:  indie pop
   Score:  61.5/100
   Why:    matches mood happy
           energy 0.8 fits your preference

5. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  49.1/100
   Why:    matches genre pop
           energy 0.9 fits your preference

============================================================
```

**Acoustic Lover** (jazz/relaxed, likes_acoustic=True):
```
============================================================
Top Recommendations for Acoustic lover
============================================================

1. Coffee Shop Stories
   Artist: Slow Stereo
   Genre:  jazz
   Score:  98.8/100
   Why:    matches genre jazz
           matches mood relaxed
           energy 0.4 fits your preference

2. Acoustic Guitar
   Artist: Acoustic Artist
   Genre:  acoustic
   Score:  64.2/100
   Why:    matches mood relaxed
           energy 0.4 fits your preference

3. Thunderstorm
   Artist: Iron Anvil
   Genre:  metal
   Score:  7.5/100
   Why:    energy 0.9 fits your preference

4. Quiet Moments
   Artist: Soft Piano
   Genre:  classical
   Score:  11.2/100
   Why:    energy 0.2 fits your preference

5. Blues at Midnight
   Artist: Delta Soul
   Genre:  blues
   Score:  15.0/100
   Why:    energy 0.5 fits your preference

============================================================
```

**Acoustic Hater** (jazz/relaxed, likes_acoustic=False — IDENTICAL RESULTS):
```
============================================================
Top Recommendations for Acoustic hater
============================================================

1. Coffee Shop Stories
   Artist: Slow Stereo
   Genre:  jazz
   Score:  98.8/100
   Why:    matches genre jazz
           matches mood relaxed
           energy 0.4 fits your preference

2. Acoustic Guitar
   Artist: Acoustic Artist
   Genre:  acoustic
   Score:  64.2/100
   Why:    matches mood relaxed
           energy 0.4 fits your preference

3. Thunderstorm
   Artist: Iron Anvil
   Genre:  metal
   Score:  7.5/100
   Why:    energy 0.9 fits your preference

4. Quiet Moments
   Artist: Soft Piano
   Genre:  classical
   Score:  11.2/100
   Why:    energy 0.2 fits your preference

5. Blues at Midnight
   Artist: Delta Soul
   Genre:  blues
   Score:  15.0/100
   Why:    energy 0.5 fits your preference

============================================================
```

**Genre-Energy Clash** (folk/melancholic, energy=0.95 — contradiction):
```
============================================================
Top Recommendations for Genre-energy clash
============================================================

1. Morning Dew
   Artist: Folk Wanderer
   Genre:  folk
   Score:  90.5/100
   Why:    matches genre folk
           matches mood melancholic
           energy 0.3 fits your preference

2. Indie Vibes
   Artist: Indie Band
   Genre:  indie
   Score:  58.5/100
   Why:    matches mood melancholic
           energy 0.5 fits your preference

3. Sunset Horizon
   Artist: Indie Dreams
   Genre:  indie rock
   Score:  58.0/100
   Why:    matches mood melancholic
           energy 0.5 fits your preference

4. Soul Searching
   Artist: Soul Explorers
   Genre:  soul
   Score:  58.0/100
   Why:    matches mood melancholic
           energy 0.5 fits your preference

5. Ballad Story
   Artist: Emotional Singer
   Genre:  ballad
   Score:  55.0/100
   Why:    matches mood melancholic
           energy 0.3 fits your preference

============================================================
```

**High Energy Rocker vs Low Energy Rocker** (same genre/mood, opposite energy):

High Energy (rock/intense, energy=0.92):
```
============================================================
Top Recommendations for High energy rocker
============================================================

1. Storm Runner
   Artist: Voltline
   Genre:  rock
   Score:  99.8/100
   Why:    matches genre rock
           matches mood intense
           energy 0.9 fits your preference

2. Riff Raff
   Artist: Hard Rockers
   Genre:  rock
   Score:  99.5/100
   Why:    matches genre rock
           matches mood intense
           energy 0.9 fits your preference

3. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  64.8/100
   Why:    matches mood intense
           energy 0.9 fits your preference

4. Techno Underground
   Artist: Techno Master
   Genre:  techno
   Score:  64.2/100
   Why:    matches mood intense
           energy 0.9 fits your preference

5. Hardcore Bass
   Artist: Bass Drop
   Genre:  dubstep
   Score:  64.4/100
   Why:    matches mood intense
           energy 0.9 fits your preference

============================================================
```

Low Energy (rock/intense, energy=0.35):
```
============================================================
Top Recommendations for Low energy rocker
============================================================

1. Riff Raff
   Artist: Hard Rockers
   Genre:  rock
   Score:  91.9/100
   Why:    matches genre rock
           matches mood intense
           energy 0.9 fits your preference

2. Storm Runner
   Artist: Voltline
   Genre:  rock
   Score:  91.6/100
   Why:    matches genre rock
           matches mood intense
           energy 0.9 fits your preference

3. Quiet Moments
   Artist: Soft Piano
   Genre:  classical
   Score:  12.8/100
   Why:    energy 0.2 fits your preference

4. Techno Underground
   Artist: Techno Master
   Genre:  techno
   Score:  57.2/100
   Why:    matches mood intense
           energy 0.9 fits your preference

5. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  56.3/100
   Why:    matches mood intense
           energy 0.9 fits your preference

============================================================
```

**Alex Clone** (identical to Alex — confirms determinism):
```
============================================================
Top Recommendations for Alex clone
============================================================

1. Sunrise City
   Artist: Neon Echo
   Genre:  pop
   Score:  99.7/100
   Why:    matches genre pop
           matches mood happy
           energy 0.8 fits your preference

2. Rooftop Lights
   Artist: Indigo Parade
   Genre:  indie pop
   Score:  64.4/100
   Why:    matches mood happy
           energy 0.8 fits your preference

3. Afrobeats
   Artist: African Rhythms
   Genre:  afrobeats
   Score:  64.1/100
   Why:    matches mood happy
           energy 0.9 fits your preference

4. Gym Hero
   Artist: Max Pulse
   Genre:  pop
   Score:  48.0/100
   Why:    matches genre pop
           energy 0.9 fits your preference

5. K-Pop Glory
   Artist: K-Stars
   Genre:  K-pop
   Score:  64.8/100
   Why:    matches mood happy
           energy 0.8 fits your preference

============================================================
```

### Key Findings from Adversarial Testing

- **likes_acoustic field unused**: Acoustic Lover and Acoustic Hater get identical recommendations (99% match). The `likes_acoustic` field in UserProfile is never used in scoring logic—this is dead code.
- **Impossible combinations handled gracefully**: Shadow (darkwave/celebratory) scores only by energy since no songs match the genre+mood combo.
- **Energy boundary behavior**: Extreme energy values (0.01, 0.99) don't break scoring; the energy_distance formula handles boundaries correctly.
- **Genre+mood dominate**: Genre-Energy Clash (folk + 0.95 energy) still picks folk songs despite energy mismatch because genre+mood rewards (35+50=85 points) far exceed energy penalty.
- **Deterministic output**: Alex vs Alex Clone return identical results (Storm Runner, etc.) in same order, confirming no randomness.
- **Diversity algorithm working**: High/Low Energy Rockers (same genre/mood, different energy targets) do diverge slightly when using diversity ranking strategy.

---

## Experiments You Tried

The experiments I focused on were:
* Introducing Adversarial user profiles (i.e. genre and mood conflicts)
* Finding an appropriate song diversity weight
* Adjusting mood, genre, and energy weights

Each of these required multiple iterations to fine-tune the playlist creation.

One big takeaway was the implementation's binary nature. Genre matched or it didn't. Mood matched or it didn't. Due to time constraints, I didn't change the implementation, requiring drastic weight changes to impact the scoring.

---

## Limitations and Risks

More limitations are documented in the [Limitations and Bias](./model_card.md#6-limitations-and-bias) section.

Some limitations to note are
* Song database does not include global genres
* No fuzzy genre or mood matching
* Strong favoring of mood

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

I describe this some in my [Personal Reflection](./model_card.md#9-personal-reflection), but recommendation engines are an interesting blend of static and dynamic data wrapped in linear algebra.
Static information can be properties like genre, BPM, or maker, while dynamic data is the number of plays or user ratings.
The fun part of recommendation engines is determining the weighting of the data you have.
Do you recommend products or songs because the maker matches something about the user's prior actions, or do you recommend others because the BPM or price is similar to what they are currently viewing?
How a recommender answers these and similar questions is what differentiates them, and it's where bias or unfairness can be introduced.
Popular brands can stay popular because they are already popular, even if a less well-known maker is offering a superior product.
Undiscovered artists will never be found because they don't already have a high play count.
Balancing "easy" or "safe" recommendations with meaningful ones is a tricky paradigm that take significant fine-tuning to perfect. Even then, the algorithm may need to be personalizable as user preferences differ and change over time.
Once those questions are answered and the weights are determined, the recommendation problem becomes a mathematical optimization problem.
The true problem comes in determining the scoring as that necessitates finding what is most important in a sea of useful data.

The biggest learning moment during this project was trying to differentiate the playlist creation modes. `Diversity` and `Top N` stubbornly returned the same playlists, identifying the limitation of an all-or-nothing scoring system. It really showed how important how ranking spectrums are to these kinds of systems. Even with this limitation, the recommendation engine still feels like an informed recommendation. Any kind of personalization scoring gives better results than a random list.

AI tools were responsible for the entire implementation with manual approval for each line change. I opt for consistent verification methodology to ensure the agent doesn't spiral off-track.

If I extended this project, I'd first work on adding fuzzy genre and mood matching algorithms. Beyond this, I'd like to integrate the system with a more robust and real song database, necessitating more scoring performance optimizations as well.