# %% imports
import os
import pandas as pd
import seaborn as sns
import numpy as np

from collections import Counter

# %% read the results
def parse_outfile(path: str, run: int, mode: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.rename(columns={" sequence": "sequence"}, inplace=True)
    df["run"] = run
    df["mode"] = mode
    return filter_bz(df)


def detect_bz(row):
    val = str(row.sequence)
    return ("B" in val) or ("Z" in val)


def filter_bz(df) -> pd.DataFrame:
    """ drop any results with 'B' or 'Z', which are conflations 
    Thanks a lot, https://www.fao.org/3/Y2775E/y2775e0e.htm"""
    drop_filter = [detect_bz(row) for _, row in df.iterrows()]
    df["to_drop"] = drop_filter
    return df[~df.to_drop].drop(columns="to_drop")


def parse_results(suffix: str, mode: str) -> pd.DataFrame:
    files = [os.path.join("output",  mode, l) for l in os.listdir(f"output/{mode}")]
    files = [f for f in  files if f.endswith(f"{suffix}.csv")]
    runs = [f.split("_")[1] for f in files]
    dfs = [parse_outfile(f, r,  mode) for f,r in zip(files, runs)]
    return pd.concat(dfs)


top10_df = pd.concat((parse_results("10", "svi"), parse_results("10", "mcmc")))
top200_df = pd.concat((parse_results("200", "svi"), parse_results("200", "mcmc")))

# %% compute & top20s for each method
top20_svi = top10_df.query("mode == 'svi'")["sequence"].value_counts()[:20].to_frame()
top20_svi["mode"] = "svi"
top20_mcmc = top10_df.query("mode == 'mcmc'")["sequence"].value_counts()[:20].to_frame()
top20_mcmc["mode"] = "mcmc"
top20_df = pd.concat((top20_mcmc, top20_svi))
top20_df.reset_index(inplace=True)


# %% facet grid, each facet is countplot with different mode for estimating posterior
with sns.plotting_context('paper', font_scale = 1.3):
    g = sns.FacetGrid(top20_df, row="mode", sharex=False, height=3.5, aspect=2, gridspec_kws={"hspace":0.4})
    g.map(sns.barplot, "sequence", "count", alpha=.7)
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    [ax[0].set_yticks(range(0,4,1) )for ax in g.axes]
    g.set_titles(row_template = '{row_name}', size=16)
    g.savefig(os.path.join("output", "images", "top10_by_mode.png"))


# %% compute by-position heatmap of MCMC results
# Note: could just use MCMC here, as it's higher fidelity (see above).  
# But maybe we *want* some noise, as we're trying to balance exploration here with likely 
# payoff in value
sequences = [s.lstrip() for s in top200_df['sequence'].to_list()]
df_list = []
for posn in range(4):
    counts = Counter([s[posn] for s in sequences])
    total = sum(counts.values())
    df_list.append(pd.DataFrame({'aminos': [k for k, _ in counts.items()], 'counts': [v for _, v in counts.items()], "scaled_freqs": [v / total for _, v in counts.items()], "position": posn}))
heatcount_df = pd.concat(df_list)
model_position_count_df = heatcount_df.pivot(index="aminos", columns="position", values="counts")
model_position_freq_df = heatcount_df.pivot(index="aminos", columns="position", values="scaled_freqs")

# %% plot heatmap for model data
model_position_hm = sns.heatmap(model_position_freq_df, annot=True, cmap="crest", linewidth=0.5, fmt=".3f")
model_position_hm.get_figure().savefig(os.path.join("output", "images", "model_position_heatmap.png"))

# %% compute by-position heatmap of the data
data_seqs = pd.read_csv("data/DataSetforAssignment.xlsx-Sheet2023.csv")['Variants'].to_list()
df_list = []
for posn in range(4):
    counts = Counter([s[posn] for s in data_seqs])
    total = sum(counts.values())
    df_list.append(pd.DataFrame({'aminos': [k for k, _ in counts.items()], 'counts': [v for _, v in counts.items()], "scaled_freqs": [v / total for _, v in counts.items()], "position": posn}))
data_heatcount_df = pd.concat(df_list)
data_position_count_df = data_heatcount_df.pivot(index="aminos", columns="position", values="counts")
data_position_freq_df = data_heatcount_df.pivot(index="aminos", columns="position", values="scaled_freqs")

# %% plot heatmap for training data
data_position_hm = sns.heatmap(data_position_freq_df, annot=True, cmap="crest", linewidth=0.5, fmt=".3f")
data_position_hm.get_figure().savefig(os.path.join("output", "images", "data_position_heatmap.png"))

# %% compute log ratio of frequencies, plot as heatmap
odds_ratios = np.divide(model_position_freq_df.to_numpy(), data_position_freq_df.to_numpy())
odds_df = pd.DataFrame(odds_ratios, index=model_position_freq_df.index, columns=model_position_freq_df.columns)
odds_hm = sns.heatmap(odds_df, annot=True, cmap="crest", linewidth=0.5, fmt=".3f")
odds_hm.get_figure().savefig(os.path.join("output", "images", "odds_heatmap.png"))

# %%
