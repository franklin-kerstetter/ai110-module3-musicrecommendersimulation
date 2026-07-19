# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**KeyPlay 1.0**


## 2. Intended Use  

The recommender is designed to leverage a user's favorite genre, current mood, and energy level to create a simple playlist of songs they may enjoy. The system offers 2 modes:
* **Song Diversity**: A more varied selection of songs, promoting songs outside their usual preferences.
* **Top N**: The standard top N recommended songs.

There's a lot of data not collected about the user that could be incorporated for an enhanced recommendation algorithm. One of the big assumptions it makes is that users typically want to hear songs in their favorite genre. The mode separations is an attempt to offer users a means out of this, but it still heavily influences the decision logic.

This is mostly a classroom exploration model, not intended for production use as is. It could certainly be productionalized with more robust logic leveraging more user data such as "last 5 songs listed to" or "last 5 songs skipped."


## 3. How the Model Works  

Song scoring is a simple sum of 3 weighted values: genre match, mood match, and energy distance.
* If the song matches a user's favorite genre, it scores 35 points
* If the song matches a user's mood, it scores 50 points
* The closer the song's energy is to the user's energy, the more points it receives (up to 15).

If we're in Top N mode, the songs are ordered and the top few songs are returned.

If we're in Song Diversity mode, the songs are then re-scored with points given to how they differ from other, already-selected songs. This way, users can end with a diverse playlist.

## 4. Data  

The model leverages a dataset of 60 songs spanning 41 genres and 21 moods.

**Genre coverage:** Pop variants (5), rock variants (5), electronic subgenres (7), hip-hop variants (3), plus jazz, soul, classical, ambient, indie, funk, folk, country, reggae, blues, acoustic, ballad, afrobeats, dream pop, experimental, cyberpunk.

**Mood coverage:** Happy, chill, intense, focused, energetic, aggressive, relaxed, moody, peaceful, melancholic, mellow, dark, uplifting, dreamy, smooth, mysterious, playful, epic, ethereal, seductive, nostalgic.

**Known gaps:** Latin genres (reggaeton, bachata, salsa) completely absent. Asian music limited to K-pop. Middle Eastern, Indian/Bollywood, and deeper world music underrepresented. Gospel/spiritual music missing. Electronic subgenres thin beyond broad categories. No fuzzy genre boundaries—41 genres across 60 songs creates mismatch issues (noted in Limitations section).



## 5. Strengths  

My system works well when there is congruence between a user's genre preference and current mood. For example, pop + happy, lofi + chill, and rock + intense. This results in high-confidence recommendations better matching expected outcomes.


## 6. Limitations and Bias 


There are several limitations of the current recommendation system. This is not an exhaustive list but some immediate issues.
1. Binary genre & mood matching - There are no fuzzy match capabilities for close or related genres (i.e. "alt-rock" scores 0 for a match with "rock")
2. Unused acoustic preference - We don't take into account this user preference even though it's collected
3. Mood dominance - Mood is a significantly dominant attribute. If the mood is niche, this could lead to over-indexing.
4. No popularity data - There's no indication of whether a song is widely played or not. We risk recommending unpopular songs.
5. Too many genres in the songs list - There are 41 genres and 60 total songs. With no fuzzy genre match, we are limited in the success of the recommendations without an improved genre matching scoring.


## 7. Evaluation  

All profiles are tested and documented in the [Sample Recommendation Output](./README.md#sample-recommendation-output) and [Adversarial Test Results](./README.md#adversarial-test-results) sections.

In terms of the recommendations, I evaluated the genre and energy relevance to determine correctness.

There is significant work left to improve the recommendation engine (e.g. genre approximation), but I was mostly testing around differentiating the different playlist modes. Choosing the top N is straightforward, but it took several iterations to determine a workable diversity weighting when constructing a less homogenous playlist. The system struggled to weight this appropriately, often leading to both modes producing the exact same playlists. This probably a fault on 2 fronts with one being the scoring being so all-or-nothing and the other being an incorrect diversity weighting. With time constraints, I opted for changing the diversity weighting, but a production-ready product would need a more robust scoring algorithm.


## 8. Future Work  

This model needs significant improvement to be production-ready.
Some immediate feature and functionality ideas include
* Fuzzy genre matching scoring
* Fuzzy mood matching scoring
* User listening history to inform future playlists
* User-specified playlist creations
* Specifying length of playlist capabilities
* More modes (e.g. "Discovery" for finding all new genres)
* More automation


## 9. Personal Reflection  

Recommender systems are complex.
I expected this going in, but actually working with one really identified how complicated and data-intensive they can become.

For example, one aspect I took for granted is genre classification. New genres are constantly being created, so recommendation algorithms need to stay up-to-date and correct in how they manage these classifications.
* Is pop-rock more like pop or more like rock? 
* Is it equally both? 
* Do qualities of the actual song impact whether a pop-rock song is more of one than the other?
* Do artists classify their own songs, and if so, what if they are inaccurate or wrong?

There is so much that can go into scoring genre classifications that I never considered.

Also, I never thought about how recommendations are computed. Before this, it was a bit like magic, but now it's clear (and almost obvious) that it breaks down to a math optimization problem.

