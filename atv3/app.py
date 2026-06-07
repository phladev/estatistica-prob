import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split

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

**Nesta atividade (3):** além da regressão linear múltipla já construída, o dashboard responde a
uma pergunta adicional — **como saber se um modelo de previsão é bom de verdade?** — e usa essa
resposta para comparar a regressão com modelos de *machine learning*: **Random Forest** e um
**ensemble** que combina vários modelos em um só.

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

# ── Validação de Modelos ──────────────────────────────────────────────────────
st.markdown("## O modelo de previsão é bom? Avaliação e validação")
st.markdown(
    "Um R² alto calculado **nos mesmos dados usados para treinar** o modelo não garante que ele "
    "vai prever bem o rating de um jogador que ele nunca viu — o modelo pode simplesmente ter "
    "**decorado** os dados de treino (*overfitting*). Para validar de verdade, três práticas são "
    "essenciais: **(1)** separar dados de treino e teste, **(2)** repetir essa separação várias "
    "vezes com **validação cruzada (k-fold)** para checar se o desempenho é estável, e **(3)** "
    "olhar não só para o R², mas também para o **erro de previsão** (RMSE, MAE) e para os "
    "**resíduos**, em busca de padrões que revelem onde o modelo está errando."
)

if len(df) < 80:
    st.warning("Amostra insuficiente para treino/teste e validação cruzada (mínimo 80 observações). Reduza os filtros.")
else:
    X_ml = df[PRED_FEATURES]
    y_ml = df["rating"]
    X_train, X_test, y_train, y_test = train_test_split(X_ml, y_ml, test_size=0.25, random_state=42)
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)

    def eval_model(model) -> dict[str, float]:
        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)
        return {
            "R² (treino)": r2_score(y_train, pred_train),
            "R² (teste)": r2_score(y_test, pred_test),
            "RMSE (teste)": mean_squared_error(y_test, pred_test) ** 0.5,
            "MAE (teste)": mean_absolute_error(y_test, pred_test),
        }

    lin_model = LinearRegression().fit(X_train, y_train)
    lin_scores = eval_model(lin_model)

    st.markdown("### 1. Treino vs. teste: o modelo aprendeu o padrão ou decorou os dados?")
    st.markdown(
        "Separamos **75% dos jogadores para treinar** o modelo (regressão linear, equivalente ao "
        "OLS acima) e reservamos **25% — nunca vistos durante o ajuste — para testar**. "
        "Se o R² do treino for bem maior que o do teste, é sinal de overfitting."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R² treino", f"{lin_scores['R² (treino)']:.4f}")
    c2.metric("R² teste", f"{lin_scores['R² (teste)']:.4f}")
    c3.metric("RMSE teste", f"{lin_scores['RMSE (teste)']:.4f}", help="Erro médio de previsão em unidades de rating")
    c4.metric("MAE teste", f"{lin_scores['MAE (teste)']:.4f}", help="Erro absoluto médio — mais robusto a outliers que o RMSE")

    gap = lin_scores["R² (treino)"] - lin_scores["R² (teste)"]
    st.info(
        f"**Gap treino − teste (R²):** {gap:.4f}. "
        + ("Praticamente zero — o modelo generaliza bem para jogadores que não viu, sem sinais de overfitting."
           if abs(gap) < 0.02 else
           "Gap perceptível — vale investigar se o modelo está se ajustando demais às particularidades do treino.")
    )

    st.markdown("### 2. Validação cruzada (k-fold): o resultado depende da sorte do sorteio?")
    st.markdown(
        "Um único corte treino/teste pode ser sortudo (ou azarado). A **validação cruzada k-fold** "
        "divide os dados em *k* partes (aqui, *k = 5*), treina em *k − 1* delas e testa na parte "
        "restante — repetindo o processo *k* vezes, até que cada parte tenha servido uma vez como "
        "teste. O resultado é uma **distribuição de scores**, que revela o quão estável é o "
        "desempenho do modelo em diferentes recortes dos dados."
    )
    cv_scores = cross_val_score(LinearRegression(), X_ml, y_ml, cv=kfold, scoring="r2")
    cv_df = pd.DataFrame({"Fold": [f"Fold {i + 1}" for i in range(len(cv_scores))], "R²": cv_scores})

    col_cv1, col_cv2 = st.columns([1, 1])
    with col_cv1:
        st.dataframe(cv_df.round(4), use_container_width=True, hide_index=True)
        st.metric("R² médio (5-fold)", f"{cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    with col_cv2:
        fig_cv = px.bar(
            cv_df, x="Fold", y="R²", color="R²", color_continuous_scale="Blues",
            title="R² em cada divisão da validação cruzada (5-fold)",
            range_y=[max(0, float(cv_scores.min()) - 0.01), 1.0],
        )
        fig_cv.add_hline(
            y=cv_scores.mean(), line_dash="dash", line_color="#f97316",
            annotation_text=f"Média {cv_scores.mean():.4f}", annotation_position="bottom right",
        )
        fig_cv.update_layout(height=340, coloraxis_showscale=False)
        st.plotly_chart(fig_cv, use_container_width=True)

    st.info(
        "Scores próximos entre si nas cinco divisões indicam que o desempenho do modelo **não depende "
        "de qual parte dos dados caiu no treino ou no teste** — um bom sinal de robustez. Grande "
        "variação entre folds sugeriria que o modelo é sensível à amostra usada para treiná-lo."
    )

    st.markdown("### 3. Análise de resíduos: onde o modelo erra?")
    st.markdown(
        "Resíduo = valor real − valor previsto. Um bom modelo tem resíduos **espalhados aleatoriamente "
        "em torno de zero**, sem padrão. Formato de funil, curvas ou agrupamentos nos resíduos indicam "
        "que o modelo está sistematicamente errando em certas faixas de previsão — ou seja, deixando "
        "de capturar alguma relação presente nos dados."
    )
    pred_test_lin = lin_model.predict(X_test)
    resid_df = pd.DataFrame({"Previsto": pred_test_lin, "Resíduo": y_test.to_numpy() - pred_test_lin})

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        fig_resid_scatter = px.scatter(
            resid_df, x="Previsto", y="Resíduo",
            title="Resíduos × valores previstos (conjunto de teste)",
            labels={"Previsto": "Rating previsto", "Resíduo": "Resíduo (real − previsto)"},
            opacity=0.65, color_discrete_sequence=["#3b82f6"],
        )
        fig_resid_scatter.add_hline(y=0, line_dash="dash", line_color="#f97316")
        fig_resid_scatter.update_layout(height=360)
        st.plotly_chart(fig_resid_scatter, use_container_width=True)
    with col_res2:
        fig_resid_hist = px.histogram(
            resid_df, x="Resíduo", nbins=25,
            title="Distribuição dos resíduos",
            color_discrete_sequence=["#3b82f6"],
        )
        fig_resid_hist.add_vline(x=0, line_dash="dash", line_color="#f97316")
        fig_resid_hist.update_layout(height=360)
        st.plotly_chart(fig_resid_hist, use_container_width=True)

    st.info(
        "Os resíduos se concentram perto de zero e não exibem um padrão claro em função do valor "
        "previsto — não há, por exemplo, um funil que se abre conforme o rating previsto cresce. "
        "Isso reforça que o modelo linear é uma escolha adequada para esses dados: a relação entre "
        "as métricas por round e o rating é, de fato, predominantemente linear."
    )

st.divider()

# ── Random Forest ─────────────────────────────────────────────────────────────
st.markdown("## Random Forest: previsão com machine learning")
st.markdown(
    "A regressão linear assume que cada métrica empurra o rating numa linha reta, sempre na mesma "
    "proporção. O **Random Forest** é um algoritmo de *machine learning* que constrói **centenas de "
    "árvores de decisão**, cada uma treinada com uma amostra aleatória dos jogadores e um subconjunto "
    "aleatório das métricas (técnica chamada ***bagging***), e tira a **média das previsões** de todas "
    "elas. Isso permite capturar relações não lineares e interações entre métricas que uma única reta "
    "não enxerga — ao custo de um modelo menos interpretável que a regressão."
)

if len(df) < 80:
    st.warning("Amostra insuficiente para treinar o Random Forest (mínimo 80 observações). Reduza os filtros.")
else:
    rf_model = RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_scores = eval_model(rf_model)
    rf_cv = cross_val_score(
        RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42, n_jobs=-1),
        X_ml, y_ml, cv=kfold, scoring="r2",
    )

    st.markdown("### Random Forest vs. Regressão Linear — mesmo treino e teste")
    comp_lin_rf = pd.DataFrame({"Regressão Linear": lin_scores, "Random Forest": rf_scores}).T
    comp_lin_rf["R² médio (5-fold)"] = [cv_scores.mean(), rf_cv.mean()]
    st.dataframe(comp_lin_rf.round(4), use_container_width=True)

    diff_r2 = rf_scores["R² (teste)"] - lin_scores["R² (teste)"]
    st.info(
        f"**Random Forest:** R² no teste = {rf_scores['R² (teste)']:.4f} · "
        f"R² médio em validação cruzada = {rf_cv.mean():.4f} ± {rf_cv.std():.4f}. "
        + ("Desempenho praticamente empatado com a regressão linear — o que é esperado aqui: o "
           "Rating 2.0 é calculado pelo HLTV como uma combinação essencialmente linear das métricas "
           "por round, então não há relações não lineares relevantes para o Random Forest explorar."
           if abs(diff_r2) < 0.01 else
           ("Ganho em relação à regressão linear — sinal de que existem relações não lineares ou "
            "interações entre métricas que o modelo linear não capturava."
            if diff_r2 > 0 else
            "Desempenho um pouco abaixo da regressão linear — esperado quando a relação real é "
            "praticamente linear: árvores de decisão têm mais dificuldade em aproximar uma reta "
            "do que um modelo que já assume linearidade."))
    )

    st.markdown("### Importância das métricas (*feature importance*)")
    st.markdown(
        "Para cada métrica, o Random Forest mede o quanto, em média, ela contribui para reduzir o "
        "erro de previsão ao longo de todas as árvores da floresta. Quanto maior a barra, mais o "
        "modelo depende daquela métrica para decidir suas previsões — uma forma de **explicar** um "
        "modelo que, por si só, é uma caixa relativamente opaca."
    )
    importances = pd.Series(rf_model.feature_importances_, index=PRED_FEATURES).sort_values()
    fig_imp = px.bar(
        x=importances.values,
        y=[PRED_LABELS[i] for i in importances.index],
        orientation="h",
        color=importances.values,
        color_continuous_scale="Greens",
        title="Importância de cada métrica nas previsões do Random Forest",
        labels={"x": "Importância", "y": ""},
    )
    fig_imp.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig_imp, use_container_width=True)

    top_feat, second_feat = importances.index[-1], importances.index[-2]
    st.info(
        f"**{PRED_LABELS[top_feat]}** concentra sozinha cerca de **{importances.iloc[-1]:.0%}** da "
        f"importância total — o Random Forest 'descobriu', sem qualquer pista além dos dados, que "
        "essa é a métrica mais decisiva para prever o rating, o que é coerente com sua altíssima "
        f"correlação de Pearson vista mais acima. **{PRED_LABELS[second_feat]}** vem em seguida, "
        "bem atrás. As demais métricas contribuem pouco de forma isolada — não porque sejam "
        "irrelevantes, mas porque sua relação com o rating já está em boa parte **capturada** pela "
        "métrica líder (a mesma multicolinearidade que motivou excluir KD Ratio do modelo)."
    )

st.divider()

# ── Ensemble ──────────────────────────────────────────────────────────────────
st.markdown("## Ensemble: combinando vários modelos em um só")
st.markdown(
    "Cada modelo erra de um jeito diferente: a regressão linear é estável e interpretável, mas "
    "rígida; o Random Forest captura não linearidades, mas pode reagir de forma diferente a "
    "jogadores atípicos; o **Gradient Boosting** constrói árvores em sequência, cada uma corrigindo "
    "o erro da anterior, o que o torna preciso mas mais sensível a ruído. Um **modelo ensemble** "
    "combina as previsões de vários modelos — aqui, pela **média das previsões individuais "
    "(*Voting Regressor*)** — apostando que os erros de um sejam compensados pelos acertos de "
    "outro, o que tende a **reduzir a variância** da previsão final e tornar o resultado mais robusto."
)

if len(df) < 80:
    st.warning("Amostra insuficiente para treinar o ensemble (mínimo 80 observações). Reduza os filtros.")
else:
    gb_model = GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=42)
    gb_model.fit(X_train, y_train)
    gb_scores = eval_model(gb_model)

    ensemble_model = VotingRegressor([
        ("regressao_linear", LinearRegression()),
        ("random_forest", RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42, n_jobs=-1)),
        ("gradient_boosting", GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=42)),
    ])
    ensemble_model.fit(X_train, y_train)
    ens_scores = eval_model(ensemble_model)

    st.markdown("### Comparação final — todos os modelos, mesmo treino e teste")
    final_comp = pd.DataFrame({
        "Regressão Linear": lin_scores,
        "Random Forest": rf_scores,
        "Gradient Boosting": gb_scores,
        "Ensemble (Voting)": ens_scores,
    }).T
    st.dataframe(final_comp.round(4), use_container_width=True)

    fig_final = px.bar(
        final_comp.reset_index().rename(columns={"index": "Modelo"}),
        x="Modelo", y="RMSE (teste)", color="Modelo",
        title="RMSE no conjunto de teste, por modelo — quanto menor, melhor",
        labels={"RMSE (teste)": "RMSE (teste)"},
    )
    fig_final.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig_final, use_container_width=True)

    best_model_name = final_comp["RMSE (teste)"].idxmin()
    rmse_spread = float(final_comp["RMSE (teste)"].max() - final_comp["RMSE (teste)"].min())
    st.success(
        f"**Melhor modelo no teste (menor RMSE):** {best_model_name} "
        f"(RMSE = {final_comp.loc[best_model_name, 'RMSE (teste)']:.4f}). "
        + ("Mas a diferença entre os quatro modelos é mínima — o que confirma, mais uma vez, que a "
           "relação entre as métricas por round e o rating é praticamente linear, e que modelos mais "
           "complexos não têm muito espaço para ganhar aqui."
           if rmse_spread < 0.002 else
           "A diferença entre os modelos é perceptível — vale a pena investigar quais jogadores "
           "cada modelo erra mais, para entender o que o vencedor está capturando que os demais não.")
        + " Em geral, o **ganho do ensemble é maior quando os modelos individuais cometem erros "
        "diferentes** entre si — combiná-los reduz o risco de depender de um único modelo. Quando, "
        "como aqui, os modelos já convergem para respostas parecidas, o ensemble tende a empatar "
        "com o melhor modelo individual, sem piorar o resultado."
    )

st.divider()

st.caption(
    "Nota metodológica: o dataset contém os 803 jogadores com maior número de mapas no ranking HLTV. "
    "O Rating 2.0 é um índice ofensivo/defensivo — papéis de suporte podem ser subrepresentados. "
    "Os modelos de validação, Random Forest e ensemble usam uma divisão fixa treino/teste "
    "(75/25, random_state=42) e validação cruzada de 5 folds sobre os dados filtrados. "
    "Fonte: HLTV.org."
)
