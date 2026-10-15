# What should an indie RPG cost on Steam?

**Answer:** Indie RPGs on Steam priced £10–20 got the best reviews

## The question
- **Stakeholder:** A small indie studio Looking to release their new indie RPG on Steam
- **Decision:** What price point would be best to use for their game

## What I found
- I found that Indie RPG games in the price range of £10–20 got the best review scores.
- Review scores rise from 0.72 (free) to 0.81 at £10–20. The £20+ median is 0.76, but its range (0.69–0.81) is so wide that I wouldn't trust it, because the data doesn't support a drop.

## Recommendation
- Based on 2019 Steam data, I'd suggest pricing in the £10–20 range, because it had the highest score and the narrowest range. I'm confident that Indie RPGs priced £10–20 were rated higher than free ones, but the data can't tell us whether £5–10 was better than £10–20, or how £20+ compares.

## How sure is this?
- The difference between Free and £10–20 is real; £5–10 and £10–20 overlap, so we can't separate them.
- This data excludes Indie RPGs with fewer than 50 ratings, about half the genre. The results describe games that already found an audience, and a new game starts outside that group. They don't show whether price caused that success.
- The data is from May 2019, so it may not reflect the current market.


## Method
Steam store data (May 2019), Indie + RPG games with 50+ ratings, grouped
into price bands; medians with 95% bootstrap ranges.
Full analysis: [analysis.ipynb](analysis.ipynb)

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Data
[Steam Store Games](https://www.kaggle.com/datasets/nikdavis/steam-store-games)
by Nik Davis, licensed CC BY 4.0.