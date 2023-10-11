# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,.ju.py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
#  # Quick Polars Local Test.

# %%
import polars as pl
import numpy as np


# %% [markdown]
# # Read Data (eager/at-mention)

# %%
iris_data = pl.read_csv("data/iris.csv")

# %% [markdown]
# # Print vs Engine-Render

# %% [markdown]
# ### Print (terminal-style)

# %%
print(iris_data)

# %% [markdown]
# # Combining DataFrames

# %% [markdown]
# ### Joining
# (Left, Right, Inner, Outer)

# %%
for_comb_df1 = pl.DataFrame(
    {
        "a": np.arange(0, 8),
        "b": np.random.rand(8),
        "d": [1, 2.0, np.NaN, np.NaN, 0, -5, -42, None],
    }
)

for_comb_df2 = pl.DataFrame(
    {
        "x": np.arange(0, 8),
        "y": ["A", "A", "A", "B", "B", "C", "X", "X"],
    }
)
joined = for_comb_df1.join(for_comb_df2, left_on="a", right_on="x")
print(joined)

# %% [markdown]
# ### Concatination 
# (Horizontal or vertical)

# %%
stacked = for_comb_df1.hstack(for_comb_df2)
print(stacked)

# %% [markdown]
# ## Render (engine style; e.g. Jupyter or VSCode)

# %%
iris_data

# %% [markdown]
# # Various

# %%
type(iris_data)

# %% [markdown]
# # Quick Views
# (Head, Tail, Sample, Describe)

# %% [markdown]
# ### Some Data to Look at

# %%
from datetime import datetime

for_desc_df = pl.DataFrame(
    {
        "integer": [1, 2, 3, 4, 5],
        "date": [
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            datetime(2022, 1, 3),
            datetime(2022, 1, 4),
            datetime(2022, 1, 5),
        ],
        "float": [4.0, 5.0, 6.0, 7.0, 8.0],
        "words": ["alpha", "beta", "gaga", "delta", "eps"]
    }
)

print(for_desc_df)

# %%
print(for_desc_df.head(2))
print(for_desc_df.tail(2))
print(for_desc_df.sample(2))

# %%
print(for_desc_df.describe())

# %% [markdown]
# # GroupBy

# %%
scores = {
    "Zone": [
        "North",
        "North",
        "North",
        "South",
        "South",
        "East",
        "East",
        "West",
        "West",
    ],
    "School": [
        "Rushmore",
        "Rushmore",
        "Rushmore",
        "Bayside",
        "Rydell",
        "Shermer",
        "Shermer",
        "Ridgemont",
        "Hogwarts",
    ],
    "Name": ["Jonny", "Mary", "Jim", "Joe", "Jakob", "Jimmy", "Erik", "Lam", "Yip"],
    "Math": [78, 39, 798, 76, 56, 67, 89, 100, 55],
    "Science": [80, 45, 80, 68, 90, 45, 66, 89, 32],
}


school_df = pl.DataFrame(scores)
print(school_df)

# %%
q = (
    school_df.lazy()
    .group_by(by="Zone")
    .agg(
        "School",
        "Name",
        "Math",
        "Science",
    )
)
q.collect()

# %%
q = (
    school_df.lazy()
    .group_by(by="Zone")
    .agg(
        "School",
        "Name",
        "Math",
        "Science",
    )
    .filter(pl.col("Zone") == "East")
)
q.collect()

# %%
q = (
    school_df.lazy()
    .group_by(by="Zone")
    .agg(
        pl.col("Science").std().alias("Science_std"),
    )
)
q.collect()


# %% [markdown]
# ### Note: order returned by groupby is effectively random (presumably due to split-threading)

# %%
q = (
    school_df.lazy()
    .group_by(by="Zone")
    .agg(
        [
            pl.col("Science").count().alias("Number of Schools"),
            pl.col("Science").max().alias("Science(Max)"),
            pl.col("Science").min().alias("Science(Min)"),
            pl.col("Science").mean().alias("Science(Mean)"),
            pl.col("Math").max().alias("Math(Max)"),
            pl.col("Math").min().alias("Math(Min)"),
            pl.col("Math").mean().alias("Math(Mean)"),
        ]
    )
)
print(q.collect())

# %% [markdown]
# ### .sort() can be used to deal with the variable ordering

# %%
q = (
    school_df.lazy()
    .group_by(by="Zone")
    .agg(
        [
            pl.col("Science").count().alias("Number of Schools"),
            pl.col("Science").max().alias("Science(Max)"),
            pl.col("Science").min().alias("Science(Min)"),
            pl.col("Science").mean().alias("Science(Mean)"),
            pl.col("Math").max().alias("Math(Max)"),
            pl.col("Math").min().alias("Math(Min)"),
            pl.col("Math").mean().alias("Math(Mean)"),
        ]
    )
    .sort(by="Zone")
)
print(q.collect())

# %% [markdown]
# ### Here's one hack to create custom ordering : joining another dataframe and hiding an invisible ordering column

# %%
df_sortorder = pl.DataFrame(
    {
        "Zone": ["North", "South", "East", "West"],
        "Zone_order": [0, 1, 2, 3],
    }
).lazy()

q = (
    school_df.lazy()
    .join(df_sortorder, on="Zone", how="left")
    .group_by(by=["Zone", "Zone_order"])
    .agg([pl.max("Science").alias("Science(Max)")])
    .sort("Zone_order")
    .select(pl.exclude("Zone_order"))
)
q.collect()

# %% [markdown]
# # Insurance CSV

# %%
insurance_df = pl.scan_csv("data/insurance.csv")
insurance_df.collect()

# %%
(
    pl.scan_csv("data/insurance.csv")
    .group_by(by="sex")
    .agg(
        [pl.col("charges").sum()]
        )
).collect()

# %%
q = (
    pl.scan_csv("data/insurance.csv")
    .group_by(by="region")
    .agg(
        [
            (pl.col("sex") == "male").sum().alias("male"),
            (pl.col("sex") == "female").sum().alias("female"),
        ]
    )
    .sort(by="region")
)
q.collect()

# %%
q = (
    pl.scan_csv("data/insurance.csv")
    .group_by(by="region")
    .agg(
        [
            (pl.col("charges").filter(pl.col("sex") == "male"))
            .mean()
            .alias("male_mean_charges"),
            (pl.col("charges").filter(pl.col("sex") == "female"))
            .mean()
            .alias("female_mean_charges"),
        ]
    )
    .sort(by="region")
)
q.collect()

# %%
q = (
    pl.scan_csv("data/insurance.csv")
    .group_by(by="region")
    .agg(
        [
            pl.col("smoker").count().alias("smoker_Q_count"),
            (pl.col("smoker") == "yes").sum().alias("yes_smoker_count"),
            (pl.col("smoker") == "no").sum().alias("no_smoker_count"),
        ]
    )
)

q.collect()

# %% [markdown]
# ### NOTE: `.count()` counts all entries, `.sum()` counts all values that are true (assuming a boolean on column)

# %%
q = (
    pl.scan_csv("data/insurance.csv")
    .group_by(by="region")
    .agg([(pl.col("smoker") == "yes").sum()])
    .sort(by="region")
)
q.collect()

# %%

# %%
