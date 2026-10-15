import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BINS = [-1, 0, 5, 10, 20, 500]
LABELS = ["Free", "Under £5", "£5–10", "£10–20", "£20+"]
ACCENT, MUTED = "#2a78d6", "#898781"
RECOMMENDED_PRICE = "£10–20"


@st.cache_data
def load_indie_rpg():
    df = pd.read_csv("data/steam.csv")
    df["total_ratings"] = df["positive_ratings"] + df["negative_ratings"]
    df["review_score"] = df["positive_ratings"] / df["total_ratings"]
    is_indie_rpg = (df["genres"].str.contains("Indie", regex=False)
                    & df["genres"].str.contains("RPG", regex=False))
    return df[is_indie_rpg]


def bootstrap_ci(scores, rng, n=2000):
    medians = [np.median(rng.choice(scores, size=len(scores), replace=True))
               for _ in range(n)]
    return np.percentile(medians, [2.5, 97.5])


@st.cache_data
def price_band_table(indie_rpg_all):
    rated = indie_rpg_all[indie_rpg_all["total_ratings"] >= 50]
    rated = rated.assign(price_band=pd.cut(rated["price"], bins=BINS, labels=LABELS))
    rng = np.random.default_rng(42)
    rows = []
    for band, group in rated.groupby("price_band", observed=True):
        low, high = bootstrap_ci(group["review_score"].to_numpy(), rng)
        rows.append({"price_band": band, "games": len(group),
                     "median_score": group["review_score"].median(),
                     "ci_low": low, "ci_high": high})
    return pd.DataFrame(rows)


indie_rpg_all = load_indie_rpg()
table = price_band_table(indie_rpg_all)
excluded = (indie_rpg_all["total_ratings"] < 50).mean()

# --- 1. The answer first ---
st.title("What should an indie RPG cost on Steam?")
st.caption("Steam store data, May 2019 · Indie + RPG games with 50+ ratings · "
           "Data: Nik Davis, CC BY 4.0")
st.markdown("**Indie RPGs on Steam priced £10–20 got the best reviews**")

# --- 2. Key numbers ---
best = table[table["price_band"] == RECOMMENDED_PRICE].iloc[0]
free = table[table["price_band"] == "Free"].iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric(f"{RECOMMENDED_PRICE} median score", f"{best['median_score']:.2f}")
c1.caption(f"95% range {best['ci_low']:.2f}–{best['ci_high']:.2f}")
c2.metric("Free median score", f"{free['median_score']:.2f}")
c2.caption(f"95% range {free['ci_low']:.2f}–{free['ci_high']:.2f}")
c3.metric("Games analysed", f"{table['games'].sum():,}")
c3.caption(f"{excluded:.0%} of Indie RPGs had under 50 ratings")

# --- 3. The evidence ---
colors = [ACCENT if band == RECOMMENDED_PRICE else MUTED for band in table["price_band"]]
fig = go.Figure(go.Scatter(
    x=table["price_band"], y=table["median_score"], mode="markers",
    marker=dict(size=12, color=colors),
    error_y=dict(type="data", symmetric=False,
                 array=table["ci_high"] - table["median_score"],
                 arrayminus=table["median_score"] - table["ci_low"],
                 color=MUTED, thickness=2, width=6),
    customdata=table[["ci_low", "ci_high", "games"]],
    hovertemplate=("%{x}<br>Median score %{y:.2f}"
                   "<br>95% range %{customdata[0]:.2f}–%{customdata[1]:.2f}"
                   "<br>%{customdata[2]} games<extra></extra>"),
))
fig.update_layout(xaxis_title="Launch price",
                  yaxis_title="Median review score (share positive)",
                  yaxis=dict(range=[0.6, 0.9]), showlegend=False)
st.plotly_chart(fig, width="stretch")
st.caption("Dots are medians; bars are 95% bootstrap ranges. "
           "Wider bar = less precise.")

# --- 4. Caveats ---
st.subheader("How sure is this?")
st.markdown("""
            - Indie RPGs priced £10–20 were rated higher than free ones, but the data can't tell us whether £5–10 was better than £10–20, or how £20+ compares.
            - The analysis only includes games with 50+ ratings, which is about half of all Indie RPGs on Steam.
            - The data is from May 2019, so it may not reflect the current state of the market. so these results describe games that already found an audience, and a new game starts outside that group.
            """)

# --- 5. Details ---
with st.expander("Data table"):
    st.dataframe(table.round(2), hide_index=True)