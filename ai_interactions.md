# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

AI helped me implement 2 playlist creation modes:
* Song Diversity - users looking for a non-homogenous playlist they'd enjoy
* Top N - users looking for the top song recommendations

**How did AI help you brainstorm or implement it?**
This was a collaborative effort with Claude, resulting in an entirely AI-driven implementation.

After describing the desired outcome, Claude pitched various implementations, allowing for a back-and-forth conversation style to fine-tune the performance and behavior.
I used an intentionally iterative approach, monitoring each suggested change for correctness and performance.

**How does the pattern appear in your final code?**

This pattern appears in the distinction between [_rank_by_score](./src/recommender.py#69) and [_rank_by_diversity](./src/recommender.py#75).
Ultimately, these are derived from preferences stored in the `ranking_strategy` of the [user profile](./data/user_profiles.csv).