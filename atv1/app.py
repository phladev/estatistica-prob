import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CSGO Dashboard", layout="wide")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    players = pd.read_csv("db/player_stats.csv")
    teams = pd.read_csv("db/team_stats.csv")

    for df in (players, teams):
        unnamed_cols = [c for c in df.columns if c.lower().startswith("unnamed")]
        if unnamed_cols:
            df.drop(columns=unnamed_cols, inplace=True)

    numeric_cols_players = ["total_maps", "total_rounds", "kd_diff", "kd", "rating"]
    numeric_cols_teams = ["total_maps", "kd_diff", "kd", "rating"]

    players[numeric_cols_players] = players[numeric_cols_players].apply(pd.to_numeric, errors="coerce")
    teams[numeric_cols_teams] = teams[numeric_cols_teams].apply(pd.to_numeric, errors="coerce")

    players["entity_type"] = "Player"
    teams["entity_type"] = "Team"

    return players, teams


def apply_filters(df: pd.DataFrame, countries: list[str], min_maps: int, rating_range: tuple[float, float]) -> pd.DataFrame:
    filtered = df.copy()
    if countries:
        filtered = filtered[filtered["country"].isin(countries)]

    filtered = filtered[filtered["total_maps"] >= min_maps]
    filtered = filtered[(filtered["rating"] >= rating_range[0]) & (filtered["rating"] <= rating_range[1])]
    return filtered


def agg_value(series: pd.Series, agg_name: str) -> float:
    if series.empty:
        return float("nan")

    if agg_name == "Mean":
        return series.mean()
    if agg_name == "Median":
        return series.median()
    if agg_name == "Std":
        return series.std()
    if agg_name == "Min":
        return series.min()
    return series.max()


players_df, teams_df = load_data()

st.title("CSGO Stats: Players x Teams")
st.caption("Analise descritiva interativa com filtros, graficos e tabelas.")

all_countries = sorted(set(players_df["country"].dropna().unique()).union(set(teams_df["country"].dropna().unique())))
min_rating = float(min(players_df["rating"].min(), teams_df["rating"].min()))
max_rating = float(max(players_df["rating"].max(), teams_df["rating"].max()))

with st.sidebar:
    st.header("Filtros")
    selected_countries = st.multiselect("Country", options=all_countries)
    min_maps = st.slider("Minimum maps", min_value=0, max_value=int(max(players_df["total_maps"].max(), teams_df["total_maps"].max())), value=100)
    rating_range = st.slider("Rating range", min_value=round(min_rating, 2), max_value=round(max_rating, 2), value=(round(min_rating, 2), round(max_rating, 2)), step=0.01)
    top_n = st.slider("Top N", min_value=5, max_value=40, value=10)

    st.markdown("---")
    st.subheader("Bonus: summary metric")
    agg_name = st.selectbox("Aggregation", ["Mean", "Median", "Std", "Min", "Max"], index=1)
    metric_name = st.selectbox("Metric", ["rating", "kd", "kd_diff", "total_maps"], index=0)

players_f = apply_filters(players_df, selected_countries, min_maps, rating_range)
teams_f = apply_filters(teams_df, selected_countries, min_maps, rating_range)

common_cols = ["name", "country", "total_maps", "kd_diff", "kd", "rating", "entity_type"]
combined = pd.concat([players_f[common_cols], teams_f[common_cols]], ignore_index=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric(f"Players {agg_name} {metric_name}", f"{agg_value(players_f[metric_name], agg_name):.3f}")
c2.metric(f"Teams {agg_name} {metric_name}", f"{agg_value(teams_f[metric_name], agg_name):.3f}")
c3.metric("Filtered players", f"{len(players_f)}")
c4.metric("Filtered teams", f"{len(teams_f)}")

st.markdown("### Dynamic ranking")
col_rank_1, col_rank_2 = st.columns(2)

with col_rank_1:
    p_rank = players_f.nlargest(top_n, metric_name)
    fig_players_rank = px.bar(
        p_rank.sort_values(metric_name),
        x=metric_name,
        y="name",
        orientation="h",
        color="country",
        title=f"Top {top_n} players by {metric_name}",
    )
    fig_players_rank.update_layout(height=440, yaxis_title="")
    st.plotly_chart(fig_players_rank, use_container_width=True)

with col_rank_2:
    t_rank = teams_f.nlargest(top_n, metric_name)
    fig_teams_rank = px.bar(
        t_rank.sort_values(metric_name),
        x=metric_name,
        y="name",
        orientation="h",
        color="country",
        title=f"Top {top_n} teams by {metric_name}",
    )
    fig_teams_rank.update_layout(height=440, yaxis_title="")
    st.plotly_chart(fig_teams_rank, use_container_width=True)

st.markdown("### Performance vs volume")
fig_scatter = px.scatter(
    combined,
    x="total_maps",
    y="rating",
    color="entity_type",
    size=combined["kd_diff"].abs().clip(lower=1),
    hover_data=["name", "country", "kd", "kd_diff"],
    title="Rating x Total maps (bubble size = |kd_diff|)",
)
fig_scatter.update_layout(height=460)
st.plotly_chart(fig_scatter, use_container_width=True)

col_dist_1, col_dist_2 = st.columns(2)
with col_dist_1:
    fig_box = px.box(
        combined,
        x="entity_type",
        y="rating",
        color="entity_type",
        points="outliers",
        title="Rating distribution by entity type",
    )
    fig_box.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

with col_dist_2:
    fig_hist = px.histogram(
        combined,
        x="rating",
        color="entity_type",
        barmode="overlay",
        nbins=30,
        opacity=0.7,
        title="Rating histogram: players vs teams",
    )
    fig_hist.update_layout(height=420)
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("### Country comparison (median rating)")
country_source = st.radio("Compare country medians for", ["Players", "Teams"], horizontal=True)
country_df = players_f if country_source == "Players" else teams_f
country_med = (
    country_df.groupby("country", as_index=False)["rating"]
    .median()
    .sort_values("rating", ascending=False)
    .head(top_n)
)
fig_country = px.bar(
    country_med,
    x="country",
    y="rating",
    color="rating",
    title=f"Top {top_n} countries by median rating ({country_source})",
)
fig_country.update_layout(height=420)
st.plotly_chart(fig_country, use_container_width=True)

st.markdown("### Dynamic tables")
tab1, tab2 = st.tabs(["Players table", "Teams table"])

with tab1:
    view_cols_players = ["name", "country", "teams", "total_maps", "total_rounds", "kd_diff", "kd", "rating"]
    st.dataframe(players_f[view_cols_players].sort_values(metric_name, ascending=False), use_container_width=True, hide_index=True)

with tab2:
    view_cols_teams = ["name", "country", "total_maps", "kd_diff", "kd", "rating"]
    st.dataframe(teams_f[view_cols_teams].sort_values(metric_name, ascending=False), use_container_width=True, hide_index=True)

st.info(
    "Nota metodologica: a comparacao entre jogadores e times e util para exploracao, "
    "mas as unidades de analise sao diferentes (individuo x organizacao)."
)
