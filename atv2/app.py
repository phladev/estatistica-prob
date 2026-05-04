import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import streamlit as st

st.set_page_config(page_title="CS:GO – Análise de Performance", layout="wide")

REGIOES: dict[str, list[str]] = {
    "Americas": [
        "United States", "Brazil", "Canada", "Argentina", "Uruguay",
        "Chile", "Peru", "Mexico", "Colombia", "Venezuela",
    ],
    "Europa Ocidental": [
        "Denmark", "Sweden", "France", "Finland", "Germany", "Norway",
        "Spain", "Netherlands", "Belgium", "United Kingdom",
    ],
    "Europa Oriental": [
        "Russia", "Ukraine", "Poland", "Bulgaria", "Kazakhstan", "Belarus",
        "Serbia", "Croatia", "Latvia", "Lithuania", "Estonia",
        "Czech Republic", "Slovakia", "Hungary", "Romania", "Moldova",
    ],
    "Oceania": ["Australia", "New Zealand"],
    "Ásia": ["China", "Thailand", "Mongolia", "South Korea", "Japan", "India", "Singapore"],
}

METRICAS: dict[str, str] = {
    "rating": "Rating",
    "kd_ratio": "KD Ratio",
    "kills_per_round": "Kills por Round",
    "kd_difference": "Diferença KD",
    "impact": "Impacto",
    "kast": "KAST (%)",
    "headshot_percentage": "Headshot (%)",
    "deaths_per_round": "Mortes por Round",
    "grenade_damage_per_round": "Dano de Granada/Round",
    "assists_per_round": "Assistências por Round",
}

NUMERIC_COLS = [
    "rating", "kd_ratio", "kills_per_round", "kd_difference", "impact", "kast",
    "headshot_percentage", "deaths_per_round", "grenade_damage_per_round",
    "assists_per_round", "teammate_saved_per_round", "saved_by_teammate_per_round",
]

CORR_LABELS = {
    "kd_ratio": "KD Ratio",
    "kills_per_round": "Kills/Round",
    "kd_difference": "Diferença KD",
    "impact": "Impacto",
    "kast": "KAST (%)",
    "saved_by_teammate_per_round": "Salvo por col./Round",
    "total_kills": "Total de Kills",
    "maps_played": "Mapas jogados",
    "rounds_played": "Rounds jogados",
    "total_deaths": "Total de mortes",
    "grenade_damage_per_round": "Dano de Granada/Round",
    "headshot_percentage": "Headshot (%)",
    "assists_per_round": "Assistências/Round",
    "teammate_saved_per_round": "Colegas salvos/Round",
    "deaths_per_round": "Mortes/Round",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("db/hltv_playerStats-complete.csv")

    regiao_map: dict[str, str] = {}
    for regiao, paises in REGIOES.items():
        for pais in paises:
            regiao_map[pais] = regiao
    df["regiao"] = df["country"].map(regiao_map).fillna("Outros")

    return df


df_raw = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filtros")
    all_countries = sorted(df_raw["country"].unique())
    selected_countries = st.multiselect("País", options=all_countries)

    min_maps = st.slider(
        "Mínimo de mapas jogados",
        min_value=int(df_raw["maps_played"].min()),
        max_value=int(df_raw["maps_played"].max()),
        value=int(df_raw["maps_played"].min()),
    )

    top_n = st.slider("Top N (rankings e gráficos)", min_value=5, max_value=20, value=10)

    st.markdown("---")
    st.subheader("Medida-resumo personalizada")
    agg_opcoes = {"Média": "mean", "Mediana": "median", "Desvio Padrão": "std", "Mínimo": "min", "Máximo": "max"}
    agg_label = st.selectbox("Agregação", list(agg_opcoes.keys()), index=1)
    metrica_kpi = st.selectbox("Métrica", list(METRICAS.keys()), format_func=lambda k: METRICAS[k])

# Aplicar filtros
df = df_raw.copy()
if selected_countries:
    df = df[df["country"].isin(selected_countries)]
df = df[df["maps_played"] >= min_maps]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("O que define um jogador de elite no CS:GO?")
st.markdown(
    """
**Contextualização:** O CS:GO (*Counter-Strike: Global Offensive*) é um dos maiores esports
do mundo, com competições profissionais em todos os continentes. O **HLTV.org** é a principal
plataforma de estatísticas do cenário e desenvolveu um sistema de **Rating 2.0** — um índice
composto que resume a contribuição de um jogador em kills, mortes, rounds sobrevividos e
impacto coletivo. Compreender o que move esse indicador é fundamental para scouts, analistas e
fãs que querem entender o desempenho além do simples placar.

**Pergunta central:** *Quais métricas de performance individual têm maior associação com o
rating de um jogador profissional de CS:GO, e existem diferenças no perfil de jogo entre regiões?*

> **Dataset:** 803 jogadores do ranking HLTV · **Fonte:** HLTV.org · **Período:** estatísticas acumuladas de carreira
"""
)

st.divider()

# ── KPIs ─────────────────────────────────────────────────────────────────────
agg_fn = agg_opcoes[agg_label]
agg_val = getattr(df[metrica_kpi], agg_fn)()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Jogadores", f"{len(df)}")
k2.metric("Países representados", f"{df['country'].nunique()}")
k3.metric("Média de Rating", f"{df['rating'].mean():.3f}")
k4.metric("Mediana de Rating", f"{df['rating'].median():.3f}")
k5.metric(f"{agg_label} de {METRICAS[metrica_kpi]}", f"{agg_val:.3f}")

st.divider()

# ── Distribuição do Rating ────────────────────────────────────────────────────
st.markdown("## Distribuição do Rating")
st.markdown(
    "O rating varia de **0,77 a 1,27** entre os jogadores da amostra. "
    "A distribuição é aproximadamente simétrica em torno de **1,01**, com leve assimetria positiva — "
    "os jogadores de elite se destacam como outliers superiores."
)

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(
        df,
        x="rating",
        nbins=35,
        color_discrete_sequence=["#f97316"],
        title="Histograma do Rating",
        labels={"rating": "Rating", "count": "Frequência"},
    )
    fig_hist.add_vline(
        x=df["rating"].mean(),
        line_dash="dash",
        line_color="white",
        annotation_text=f"Média {df['rating'].mean():.3f}",
        annotation_position="top right",
    )
    fig_hist.add_vline(
        x=df["rating"].median(),
        line_dash="dot",
        line_color="lightblue",
        annotation_text=f"Mediana {df['rating'].median():.3f}",
        annotation_position="top left",
    )
    fig_hist.update_layout(height=380, bargap=0.05)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(
        df,
        y="rating",
        points="outliers",
        color_discrete_sequence=["#f97316"],
        title="Boxplot do Rating",
        labels={"rating": "Rating"},
    )
    fig_box.update_layout(height=380)
    st.plotly_chart(fig_box, use_container_width=True)

q1 = df["rating"].quantile(0.25)
q3 = df["rating"].quantile(0.75)
iqr = q3 - q1
fence_up = q3 + 1.5 * iqr
fence_low = q1 - 1.5 * iqr
outliers_up = df[df["rating"] > fence_up]
outliers_low = df[df["rating"] < fence_low]

skew_val = df["rating"].skew()
skew_label = "aproximadamente simétrica" if abs(skew_val) < 0.1 else ("assimetria positiva" if skew_val > 0 else "assimetria negativa")

st.info(
    f"**Assimetria:** {skew_val:.3f} ({skew_label}) · "
    f"**Curtose:** {df['rating'].kurt():.3f} · "
    f"**IQR:** {iqr:.3f} · "
    f"**Outliers superiores (> {fence_up:.3f}):** {len(outliers_up)} jogadores"
    + (f" — {', '.join(outliers_up.nlargest(5, 'rating')['nick'].tolist())} entre os destaques" if len(outliers_up) else "")
    + f" · **Outliers inferiores (< {fence_low:.3f}):** {len(outliers_low)} jogadores"
    + (f" — {', '.join(outliers_low.nsmallest(5, 'rating')['nick'].tolist())} entre os mais baixos" if len(outliers_low) else "")
    + "."
)

st.divider()

# ── Correlações ───────────────────────────────────────────────────────────────
st.markdown("## Quais métricas explicam o Rating?")

all_numeric = df.select_dtypes(include="number").columns.tolist()
corr_full = df[all_numeric].corr().round(3)
corr_rating = corr_full["rating"].drop("rating").sort_values()
corr_rating.index = [CORR_LABELS.get(i, i) for i in corr_rating.index]

col_c1, col_c2 = st.columns([1, 2])

with col_c1:
    fig_corr_bar = px.bar(
        x=corr_rating.values,
        y=corr_rating.index,
        orientation="h",
        color=corr_rating.values,
        color_continuous_scale="RdYlGn",
        range_color=[-1, 1],
        title="Correlação de cada métrica com o Rating",
        labels={"x": "Correlação de Pearson", "y": ""},
    )
    fig_corr_bar.update_layout(height=440, coloraxis_showscale=False)
    st.plotly_chart(fig_corr_bar, use_container_width=True)

with col_c2:
    heat_cols = [
        "rating", "kd_ratio", "kills_per_round", "impact", "kast",
        "headshot_percentage", "deaths_per_round", "assists_per_round",
        "grenade_damage_per_round",
    ]
    heat_labels = [METRICAS.get(c, CORR_LABELS.get(c, c)) for c in heat_cols]
    corr_heat = df[heat_cols].corr().round(2)
    corr_heat.columns = heat_labels
    corr_heat.index = heat_labels

    fig_heat = px.imshow(
        corr_heat,
        text_auto=True,
        color_continuous_scale="RdYlGn",
        zmin=-1,
        zmax=1,
        title="Matriz de correlação entre métricas selecionadas",
    )
    fig_heat.update_layout(height=440)
    st.plotly_chart(fig_heat, use_container_width=True)

_cr = corr_full["rating"]
st.info(
    f"**KD Ratio** (r = {_cr['kd_ratio']:.2f}) e **Kills por Round** (r = {_cr['kills_per_round']:.2f}) dominam a relação com o rating — "
    "matar mais e morrer menos é o núcleo da métrica. "
    f"**Impacto** (r = {_cr['impact']:.2f}) e **KAST** (r = {_cr['kast']:.2f}) revelam que *consistência* também pesa. "
    f"Surpreendentemente, **Headshot%** tem correlação *negativa* (r = {_cr['headshot_percentage']:.2f}): jogadores de elite "
    "priorizam posicionamento e tomada de decisão, não apenas precisão de mira. "
    f"**Assistências/round** (r = {_cr['assists_per_round']:.2f}) evidencia que papéis de suporte são subvalorizados pelo Rating."
)

st.markdown("### Explorar: métrica vs. Rating")
metric_x = st.selectbox(
    "Eixo X — comparar com Rating",
    [k for k in METRICAS if k != "rating"],
    format_func=lambda k: METRICAS[k],
)
fig_scatter = px.scatter(
    df,
    x=metric_x,
    y="rating",
    color="regiao",
    hover_data=["nick", "country", "maps_played"],
    trendline="ols",
    title=f"{METRICAS[metric_x]} × Rating",
    labels={metric_x: METRICAS[metric_x], "rating": "Rating", "regiao": "Região"},
    opacity=0.65,
)
fig_scatter.update_layout(height=460)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ── Perfil regional ───────────────────────────────────────────────────────────
st.markdown("## Perfil regional dos jogadores")

view_mode = st.radio("Agrupar por", ["Região", f"País (Top {top_n} em número de jogadores)"], horizontal=True)

if view_mode == "Região":
    fig_regional = px.box(
        df,
        x="regiao",
        y="rating",
        color="regiao",
        points="outliers",
        title="Distribuição de Rating por Região",
        labels={"regiao": "Região", "rating": "Rating"},
    )
    fig_regional.update_layout(height=430, showlegend=False)
    st.plotly_chart(fig_regional, use_container_width=True)

    region_summary = (
        df.groupby("regiao")["rating"]
        .agg(["median", "mean", "std", "count"])
        .rename(columns={"median": "Mediana", "mean": "Média", "std": "Desvio Padrão", "count": "N"})
        .sort_values("Mediana", ascending=False)
        .round(3)
    )
    st.dataframe(region_summary, use_container_width=True)
else:
    top_countries = df["country"].value_counts().head(top_n).index
    df_top_c = df[df["country"].isin(top_countries)]
    country_order = (
        df_top_c.groupby("country")["rating"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )
    fig_country = px.box(
        df_top_c,
        x="country",
        y="rating",
        color="country",
        points="outliers",
        category_orders={"country": country_order},
        title=f"Rating — Top {top_n} países com mais jogadores (ordenado por mediana)",
        labels={"country": "País", "rating": "Rating"},
    )
    fig_country.update_layout(height=430, showlegend=False)
    st.plotly_chart(fig_country, use_container_width=True)

st.divider()

# ── Medidas-resumo ────────────────────────────────────────────────────────────
st.markdown("## Medidas-resumo completas")

summary_cols = list(METRICAS.keys())
summary = df[summary_cols].describe().T.rename(
    columns={
        "count": "N",
        "mean": "Média",
        "std": "Desvio Padrão",
        "min": "Mínimo",
        "25%": "Q1",
        "50%": "Mediana",
        "75%": "Q3",
        "max": "Máximo",
    }
)
summary.index = [METRICAS[c] for c in summary_cols]
st.dataframe(summary.round(3), use_container_width=True)

st.divider()

# ── Ranking ───────────────────────────────────────────────────────────────────
st.markdown("## Ranking de jogadores")

col_r1, col_r2 = st.columns([2, 1])
with col_r1:
    rank_metric = st.selectbox(
        "Ordenar por",
        list(METRICAS.keys()),
        format_func=lambda k: METRICAS[k],
        key="rank_metric",
    )
with col_r2:
    ascending = st.checkbox("Ordem crescente", value=False)

top_players = df.nlargest(top_n, rank_metric)
sorted_players = top_players.sort_values(rank_metric, ascending=ascending)

fig_rank = px.bar(
    sorted_players,
    x=rank_metric,
    y="nick",
    orientation="h",
    color="regiao",
    category_orders={"nick": sorted_players["nick"].tolist()},
    hover_data=["country", "maps_played", "rating", "kast", "impact"],
    title=f"Top {top_n} jogadores por {METRICAS[rank_metric]}",
    labels={rank_metric: METRICAS[rank_metric], "nick": "Jogador", "regiao": "Região"},
)
fig_rank.update_layout(height=420, yaxis_title="")
st.plotly_chart(fig_rank, use_container_width=True)

with st.expander("Ver tabela completa"):
    view_cols = ["nick", "country", "regiao", "maps_played", "rating", "kd_ratio", "kills_per_round", "kast", "impact", "headshot_percentage"]
    st.dataframe(
        df[view_cols].sort_values(rank_metric, ascending=ascending).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# ── Modelo Preditivo ──────────────────────────────────────────────────────────
st.markdown("## Previsão de Rating")
st.markdown(
    "Com as correlações mapeadas, o próximo passo é construir um **modelo de regressão linear múltipla** "
    "para prever o rating a partir das métricas de performance. Os preditores usados são métricas *por round* — "
    "KD Ratio e Diferença KD foram excluídos por serem derivados das demais, o que introduziria multicolinearidade severa."
)

PRED_FEATURES = [
    "kills_per_round", "deaths_per_round", "kast", "impact",
    "headshot_percentage", "assists_per_round", "grenade_damage_per_round",
]
PRED_LABELS = {k: METRICAS[k] for k in PRED_FEATURES}

if len(df) < 30:
    st.warning("Amostra insuficiente para ajustar o modelo (mínimo 30 observações). Reduza os filtros.")
else:
    X = sm.add_constant(df[PRED_FEATURES])
    ols = sm.OLS(df["rating"], X).fit()

    rmse = float((ols.resid ** 2).mean() ** 0.5)

    m1, m2, m3 = st.columns(3)
    m1.metric("R²", f"{ols.rsquared:.4f}", help="Proporção da variância do rating explicada pelo modelo")
    m2.metric("R² ajustado", f"{ols.rsquared_adj:.4f}")
    m3.metric("RMSE", f"{rmse:.4f}", help="Erro médio de previsão em unidades de rating")

    coef_df = pd.DataFrame({
        "Coeficiente": ols.params.drop("const"),
        "Erro Padrão": ols.bse.drop("const"),
        "p-valor": ols.pvalues.drop("const"),
    })
    coef_df.index = [PRED_LABELS[i] for i in coef_df.index]
    coef_df["Sig."] = coef_df["p-valor"].apply(lambda p: "✓" if p < 0.05 else "✗")

    col_coef, col_chart = st.columns([1, 1])

    with col_coef:
        st.markdown("**Coeficientes do modelo OLS**")
        st.dataframe(coef_df.round(4), use_container_width=True)

    with col_chart:
        coef_sorted = (
            coef_df.reset_index()
            .rename(columns={"index": "Métrica"})
            .sort_values("Coeficiente", ascending=False)
        )
        abs_max = float(coef_sorted["Coeficiente"].abs().max())
        fig_coef = px.bar(
            coef_sorted,
            x="Coeficiente",
            y="Métrica",
            orientation="h",
            color="Coeficiente",
            color_continuous_scale="RdYlGn",
            range_color=[-abs_max, abs_max],
            category_orders={"Métrica": coef_sorted["Métrica"].tolist()},
            title="Coeficientes da Regressão OLS",
        )
        fig_coef.update_layout(height=320, coloraxis_showscale=False)
        st.plotly_chart(fig_coef, use_container_width=True)

    st.markdown("### Simular o rating de um jogador")
    st.markdown("Ajuste as métricas abaixo para estimar o rating com intervalo de predição de 95%.")

    row1 = st.columns(4)
    row2 = st.columns(3)
    user_vals = {}
    for col, feat in [*zip(row1, PRED_FEATURES[:4]), *zip(row2, PRED_FEATURES[4:])]:
        lo = float(df[feat].quantile(0.01))
        hi = float(df[feat].quantile(0.99))
        med = float(df[feat].median())
        step = max(round((hi - lo) / 100, 4), 0.001)
        user_vals[feat] = col.slider(
            PRED_LABELS[feat],
            min_value=round(lo, 3),
            max_value=round(hi, 3),
            value=round(med, 3),
            step=step,
        )

    new_obs = sm.add_constant(pd.DataFrame([user_vals]), has_constant="add")
    pred = ols.get_prediction(new_obs).summary_frame(alpha=0.05)

    p1, p2, p3 = st.columns(3)
    p1.metric("Rating previsto", f"{pred['mean'].iloc[0]:.3f}")
    p2.metric(
        "IC 95% (média)",
        f"[{pred['mean_ci_lower'].iloc[0]:.3f}, {pred['mean_ci_upper'].iloc[0]:.3f}]",
    )
    p3.metric(
        "IP 95% (jogador individual)",
        f"[{pred['obs_ci_lower'].iloc[0]:.3f}, {pred['obs_ci_upper'].iloc[0]:.3f}]",
    )

    st.info(
        "**IC 95% da média:** intervalo para o rating esperado de um jogador *com esse perfil médio* na população. "
        "**IP 95% individual:** intervalo mais largo — captura a variação de um jogador específico "
        "além da incerteza paramétrica do modelo. Use o IP para avaliar um jogador real."
    )

st.divider()

st.caption(
    "Nota metodológica: o dataset contém os 803 jogadores com maior número de mapas no ranking HLTV. "
    "O Rating 2.0 é um índice ofensivo/defensivo — papéis de suporte podem ser subrepresentados. "
    "Fonte: HLTV.org."
)
