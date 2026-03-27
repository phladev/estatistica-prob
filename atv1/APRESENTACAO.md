# Roteiro de Apresentacao - Dashboard CSGO (5 a 7 min)

## 1) Abertura (30-45s)
"Este projeto apresenta uma analise descritiva interativa de estatisticas de CSGO, comparando jogadores e times em um dashboard web feito com Streamlit, pandas e plotly. O foco e transformar dados agregados em insights visuais com filtros dinamicos."

## 2) Problema e objetivo (30-45s)
- Problema: tabelas brutas dificultam identificar padroes de desempenho.
- Objetivo: permitir exploracao rapida com filtros e comparacoes para responder perguntas como:
  - Quem sao os melhores por rating/KD?
  - Alto desempenho vem com boa amostra (muitos mapas)?
  - Como jogadores e times se distribuem por rating?

## 3) Dados usados (30s)
- Fonte local em CSV:
  - db/player_stats.csv
  - db/team_stats.csv
- Variaveis principais:
  - country
  - total_maps
  - kd_diff
  - kd
  - rating
- Observacao importante: comparacao entre entidades diferentes (individuo x organizacao).

## 4) Demonstracao guiada do dashboard (2:30-3:00)
### 4.1 Filtros globais (40-50s)
- Pais
- Minimo de mapas
- Faixa de rating
- Top N
- Bonus: seletor de medida-resumo (Media, Mediana, Desvio padrao, Minimo, Maximo)

Frase sugerida:
"Esses filtros atualizam todos os graficos e tabelas simultaneamente, mantendo consistencia da analise."

### 4.2 KPIs e rankings (40-50s)
- Cartoes mostram medida-resumo da metrica escolhida para jogadores e times.
- Ranking dinamico Top N por metrica (rating, kd, kd_diff, total_maps).

Frase sugerida:
"Aqui eu consigo comparar rapidamente desempenho central e lideranca por metrica, sem trocar de tela."

### 4.3 Desempenho x volume (30-40s)
- Dispersao rating x total_maps.
- Tamanho da bolha = |kd_diff|.

Frase sugerida:
"Esse grafico ajuda a separar performance consistente de outliers com pouca amostra."

### 4.4 Distribuicao e comparacao por pais (30-40s)
- Boxplot e histograma de rating para jogadores x times.
- Top paises por mediana de rating.

Frase sugerida:
"A mediana por pais reduz impacto de extremos e melhora comparacao entre grupos."

### 4.5 Tabelas dinamicas (20-30s)
- Tabela de jogadores e tabela de times com ordenacao pela metrica selecionada.

Frase sugerida:
"A tabela serve como base auditavel para validar os insights dos graficos."

## 5) Pontos fortes da aplicacao (1:00)
- Interatividade real: filtros unificados em todos os componentes.
- Flexibilidade analitica: multiplas metricas e medidas-resumo.
- Leitura visual completa: ranking, dispersao, distribuicao e tabela.
- Codigo organizado: funcoes para carga, filtro e agregacao.

## 6) Pontos fracos do codigo (1:00)
- Nao ha analise temporal (sem evolucao por periodo).
- Comparacao entre niveis diferentes (jogador x time) tem limitacoes metodologicas.
- Sem pipeline de testes automatizados.
- Tratamento de outliers ainda simples.

## 7) Conclusao (20-30s)
"O dashboard entrega uma analise descritiva clara e interativa, adequada para exploracao rapida. Como proximo passo, eu incluiria dimensao temporal, metricas de confiabilidade da amostra e validacao estatistica mais robusta."

---

## Perguntas que podem aparecer (cola rapida)
1. Por que usar mediana em algumas comparacoes?
- Porque e mais robusta a outliers do que a media.

2. Por que considerar total_maps junto de rating?
- Para avaliar confiabilidade da performance: alta metrica com pouca amostra pode enganar.

3. Qual o principal limite dessa comparacao?
- Jogadores e times sao unidades de analise diferentes; comparacao e exploratoria, nao causal.

4. O que voce melhoraria se tivesse mais tempo?
- Serie temporal, normalizacao por contexto competitivo, testes automatizados e exportacao de relatorios.

## Checklist antes de apresentar
- Rodar: python3 -m streamlit run app.py
- Conferir se filtros estao atualizando todos os componentes.
- Preparar 2 cenarios de demo:
  - Cenario A: filtro amplo (visao geral)
  - Cenario B: filtro restrito (insight especifico)
- Treinar fala para caber entre 5 e 7 minutos.
