# Roteiro de Apresentação – Atividade 2 (5 a 7 min)

---

## 1) Contextualização do problema e história dos dados

### O que é CS:GO e por que analisar?

O *Counter-Strike: Global Offensive* (CS:GO) é um dos maiores esports do mundo, com ligas profissionais em todos os continentes e premiações milionárias. O cenário competitivo exige análise constante de desempenho: scouts avaliam jogadores, analistas estudam adversários e times tomam decisões baseadas em dados.

### Fonte dos dados: HLTV.org

O HLTV.org é a principal plataforma de estatísticas do CS:GO profissional. Ela registra, desde 2012, todas as partidas oficiais e calcula métricas individuais acumuladas por jogador.

O indicador central é o **Rating 2.0** — um índice composto desenvolvido pelo HLTV que mede a contribuição ofensiva e defensiva de um jogador em cada round disputado. É a métrica que times usam para comparar e contratar jogadores.

### O dataset

| Propriedade | Valor |
|---|---|
| Jogadores | 803 (maior volume de mapas no ranking HLTV) |
| Variáveis | 20 por jogador |
| Período | Estatísticas acumuladas de carreira (sem série temporal) |
| Valores nulos | Zero — dataset limpo |

**Métricas disponíveis:** rating, KD ratio, kills/round, deaths/round, assistências/round, KAST, impacto, headshot%, dano de granada/round, mapas jogados, rounds jogados, total de kills/mortes, entre outras.

---

## 2) Pergunta central

> **"Quais métricas de performance individual têm maior associação com o rating de um jogador profissional de CS:GO — e é possível prever o rating a partir dessas métricas?"**

**Por que essa pergunta faz sentido com esses dados?**
- O rating é a variável-alvo natural: é o número que times, analistas e fãs usam para comparar jogadores.
- Com 18 métricas disponíveis, é possível medir a correlação de cada uma com o rating e construir um modelo preditivo.
- A dimensão regional adiciona contexto: estilos de jogo variam entre culturas competitivas (Europa, América, Ásia).

---

## 3) Seções do dashboard e como apresentar cada uma

---

### 3.1 Distribuição do Rating

**Gráficos:** Histograma + Boxplot lado a lado.

#### Como ler o Histograma
- Cada barra representa um intervalo de rating (ex: 0,98–0,99) e a altura é o número de jogadores naquele intervalo.
- A **linha tracejada branca** marca a **média** (1,012).
- A **linha pontilhada azul** marca a **mediana** (1,010).
- Quando média ≈ mediana, a distribuição é aproximadamente simétrica — o que se confirma aqui.
- As barras mais altas estão ao redor de 1,0 (maioria dos jogadores). As barras baixas nas extremidades direitas são os outliers (jogadores excepcionais).

#### Como ler o Boxplot
O boxplot comprime toda a distribuição em 5 números:

```
  |----[  Q1 | mediana | Q3  ]----| ← bigodes
       ↑               ↑
    25% dos           75% dos
    jogadores         jogadores
    estão abaixo      estão abaixo
```

- **Caixa:** contém os 50% centrais dos jogadores (entre Q1 e Q3).
- **Linha no meio da caixa:** mediana (1,010) — metade dos jogadores está acima, metade abaixo.
- **Bigodes:** se estendem até 1,5× o IQR além dos quartis.
- **Pontos soltos fora dos bigodes:** outliers — os 7 jogadores acima (ZywOo, s1mple, sh1ro...) e os 7 abaixo.

#### Medidas calculadas

| Medida | Valor | Interpretação |
|---|---|---|
| Média | 1,012 | Rating médio do dataset |
| Mediana | 1,010 | Ponto central (robusto a outliers) |
| Desvio padrão | 0,067 | Dispersão típica em torno da média |
| Assimetria | 0,016 | Praticamente simétrica (< 0,1 = simétrica) |
| Curtose | 0,698 | Leve excesso de casos no centro vs. normal pura |
| IQR | ~0,09 | Amplitude dos 50% centrais |
| Outliers superiores | 7 jogadores (> 1,17) |
| Outliers inferiores | 7 jogadores (< 0,85) |

**O que dizer:** "A distribuição é quase perfeitamente simétrica — a maioria dos profissionais tem rating entre 0,97 e 1,05. Os 7 outliers superiores são os jogadores verdadeiramente excepcionais: ZywOo (1,27), s1mple (1,25) e sh1ro (1,23) lideram o grupo."

---

### 3.2 Correlações com o Rating

**Gráficos:** Barra horizontal de Pearson + Matriz de calor (heatmap).

#### O que é correlação de Pearson?
- Mede o **grau e direção** da relação linear entre duas variáveis numéricas.
- Varia de **−1 a +1**:
  - **+1:** relação positiva perfeita (uma sobe, a outra sobe)
  - **0:** sem relação linear
  - **−1:** relação negativa perfeita (uma sobe, a outra desce)
- Regra prática: |r| > 0,7 = forte; 0,4–0,7 = moderada; < 0,4 = fraca.

#### Como ler o Gráfico de Barras de Correlação
- Cada barra representa uma métrica.
- **Barra verde/à direita:** correlação positiva com rating (métrica sobe → rating sobe).
- **Barra vermelha/à esquerda:** correlação negativa (métrica sobe → rating cai).
- O comprimento da barra indica a força da relação.

| Métrica | r | Interpretação |
|---|---|---|
| KD Ratio | +0,976 | Quase determina o rating sozinho |
| Kills/Round | +0,941 | Matar mais → rating maior |
| Diferença KD | +0,885 | Ter mais kills que mortes → rating maior |
| Impacto | +0,806 | Kills em momentos decisivos contam muito |
| KAST | +0,679 | Ser consistente a cada round importa |
| Mortes/Round | −0,554 | Morrer mais → rating menor |
| Assistências/Round | −0,301 | Jogadores de suporte são penalizados |
| **Headshot%** | **−0,254** | **Contraintuitivo: mais headshots → rating menor** |

#### Como ler a Matriz de Calor (Heatmap)
- Cada célula mostra a correlação entre **dois pares de métricas**.
- **Verde:** correlação positiva forte.
- **Vermelho:** correlação negativa forte.
- **Amarelo/branco:** correlação fraca ou nula.
- A diagonal principal é sempre 1,0 (cada métrica com ela mesma).
- Use para identificar quais métricas se movem juntas (possível multicolinearidade).

#### Scatter interativo
- O eixo X é a métrica selecionada, o eixo Y é sempre o rating.
- Cada ponto é um jogador, colorido por região.
- A **linha de tendência OLS** mostra a direção geral da relação.
- **Para demonstrar:** selecione "Headshot (%)" — a linha de tendência vai para baixo, confirmando a correlação negativa.

---

### 3.3 Perfil regional dos jogadores

**Gráfico:** Boxplot por Região ou por País.

#### Como ler Boxplots lado a lado
- Cada caixa representa a distribuição de rating de uma região/país.
- **Compare as medianas** (linha central de cada caixa): indica o nível médio de cada grupo.
- **Compare a largura das caixas (IQR):** indica a variabilidade interna do grupo.
- **Pontos fora dos bigodes:** outliers individuais dentro de cada grupo.

**O que dizer:** "O nível médio de rating varia pouco entre regiões (~0,01 de diferença de mediana). O que muda é o *estilo*: europa ocidental tem maior headshot%, ásia tem mais dano de granada. Não há região 'melhor' — há estilos diferentes."

---

### 3.4 Medidas-resumo completas

Tabela de estatísticas descritivas para todas as métricas:

| Coluna | O que significa |
|---|---|
| N | Número de jogadores com dados |
| Média | Soma ÷ N |
| Desvio Padrão | Dispersão típica em torno da média |
| Mínimo / Máximo | Valores extremos |
| Q1 / Q3 | Primeiro e terceiro quartis (25% e 75%) |
| Mediana | Valor central (50%) |

---

### 3.5 Ranking interativo

**Gráfico:** Barras horizontais.

- Cada barra representa um jogador. O comprimento da barra indica o valor da métrica selecionada.
- **Cor:** região do jogador.
- **Dropdown "Ordenar por":** muda a métrica de ranking.
- **Checkbox "Ordem crescente":** inverte para mostrar os jogadores com *menor* valor no topo — útil para analisar mortes/round ou assistências.
- **"Ver tabela completa":** expande para ver todos os jogadores com múltiplas métricas lado a lado.

---

### 3.6 Modelo preditivo — Regressão Linear Múltipla

**Gráficos:** Tabela de coeficientes + Barras dos coeficientes + Simulador com sliders.

#### O que é regressão linear múltipla?
- Um modelo matemático que usa **várias variáveis (preditores)** para estimar uma variável-alvo (rating).
- Fórmula geral: `rating = β₀ + β₁×kills/round + β₂×deaths/round + ... + ε`
- O modelo aprende os coeficientes (β) que minimizam o erro de previsão nos dados.

#### Preditores usados (7 métricas)
- kills/round, deaths/round, KAST, impacto, headshot%, assistências/round, dano de granada/round
- **KD Ratio e Diferença KD foram excluídos:** são calculados a partir de kills e mortes — incluí-los junto com kills/round e deaths/round seria redundância total (multicolinearidade).

#### Como ler as métricas do modelo

| Métrica | Valor | Interpretação |
|---|---|---|
| **R²** | 0,9916 | O modelo explica **99,2% da variância** do rating |
| **R² ajustado** | 0,9916 | Penaliza pelo número de preditores — continua 0,99 (modelo robusto) |
| **RMSE** | 0,006 | Erro médio de previsão: o modelo erra em média **0,006 pontos de rating** |

> **Por que R² = 0,99?** O rating HLTV é calculado internamente pelo HLTV usando essas mesmas métricas. A regressão essencialmente "descobre" a fórmula do rating. Isso não é overfitting — é evidência de que os dados são internamente consistentes.

#### Como ler a Tabela de Coeficientes

| Coluna | O que significa |
|---|---|
| Coeficiente | Quanto o rating muda para cada +1 unidade nessa métrica, com as demais fixas |
| Erro Padrão | Incerteza na estimativa do coeficiente |
| p-valor | Probabilidade de observar esse coeficiente por acaso se ele fosse zero na população |
| Sig. ✓/✗ | p < 0,05 = estatisticamente significativo |

**Coeficientes significativos:**

| Métrica | Coeficiente | Leitura |
|---|---|---|
| Kills/Round | +1,19 | +0,01 kill/round → +0,012 no rating |
| Deaths/Round | −0,77 | +0,01 morte/round → −0,008 no rating |
| Impacto | +0,04 | Kills em momentos decisivos têm impacto positivo extra |
| Assistências/Round | −0,05 | Rôle de suporte é penalizado pelo modelo |
| Headshot% | +0,0002 | **Inverteu o sinal!** (ver insight abaixo) |

**Não significativos (p > 0,05):** KAST e dano de granada — quando kills e mortes já estão no modelo, eles não acrescentam poder explicativo independente.

#### Inversão de sinal do Headshot%: correlação de Simpson
- Correlação bivariada com rating: **−0,25** (negativa)
- Coeficiente na regressão múltipla: **+0,0002** (positivo)

Isso acontece porque jogadores com alto headshot% geralmente têm *menos kills/round* (forçam a mira na cabeça e erram mais). Quando se controla por kills/round, uma headshot% maior dado o mesmo número de kills passa a ser ligeiramente positivo. A correlação negativa vista antes era um **efeito de confusão** — o headshot% estava carregando a variação de kills/round.

#### Como demonstrar o simulador

O simulador tem 7 sliders — um para cada preditor. Ao mover os sliders, o modelo recalcula em tempo real:

1. **Deixe tudo nos valores padrão (medianas)** → rating previsto ≈ 1,012 (a mediana real do dataset — consistência perfeita)
2. **Aumente kills/round de 0,69 para 0,79** → rating previsto sobe ~0,12 (coeficiente ×1,19)
3. **Reduza deaths/round de 0,67 para 0,62** → rating previsto sobe mais ~0,04
4. **Mostre o IP 95%:** mesmo prevendo 1,05, o jogador real pode estar entre 1,04 e 1,06 — o modelo é muito preciso

#### IC vs IP — diferença importante

| | O que mede | Largura | Quando usar |
|---|---|---|---|
| **IC 95% (média)** | Onde está o rating *esperado* de jogadores com esse perfil | Estreito (~0,001) | Comparar grupos de jogadores |
| **IP 95% (individual)** | Onde cai o rating de *um jogador específico* | Largo (~0,024) | Avaliar um jogador real |

> Use sempre o **IP** quando quiser dizer "esse jogador provavelmente tem rating entre X e Y".

---

## 4) Insights principais para destacar

1. **KD Ratio quase determina o rating sozinho (r = 0,976)**
   Matar mais e morrer menos é o núcleo do indicador. O rating é predominantemente ofensivo.

2. **Headshot% tem correlação negativa com rating (r = −0,25) — o dado mais contraintuitivo**
   Jogadores de elite não forçam headshots; priorizam posicionamento e ângulos vantajosos. Forçar headshots resulta em mais erros e mortes.

3. **Impacto e KAST capturam consistência além do volume**
   KAST mede a % de rounds em que o jogador fez algo útil (kill, assist, sobreviveu ou foi trocado). Elite = consistente em todos os rounds, não só nos rounds de destaque.

4. **Assistências/round tem correlação negativa (r = −0,30)**
   Papéis de suporte são subvalorizados pelo rating. Limitação conhecida do indicador.

5. **Diferenças regionais existem, mas são sutis**
   Mediana de rating varia ~0,01 entre regiões. O que muda é o *estilo*, não o nível.

6. **R² = 0,99: a regressão "descobre" a fórmula do rating**
   Kills e mortes por round explicam quase toda a variância. KAST e dano de granada perdem significância quando controlados por kills/mortes — sua correlação com rating é mediada, não direta.

7. **Inversão do sinal do Headshot% é um exemplo didático de correlação de Simpson**
   A correlação univariada e o coeficiente na regressão múltipla têm sinais opostos.

---

## 5) Recomendações da Parte 1 atendidas

| Recomendação | Como foi atendida |
|---|---|
| Formular uma pergunta respondível | Pergunta central definida + modelo preditivo como resposta quantitativa |
| Unidade de análise única | Somente jogadores individuais (sem times) |
| Análise mais profunda que ranking | Correlações, heatmap, perfil regional, regressão com simulador |
| Variáveis suficientes | 18 métricas numéricas por jogador |

---

## 6) Roteiro de fala sugerido

### Abertura (30s)
> "Este trabalho usa dados do HLTV.org — a maior plataforma de estatísticas do CS:GO profissional — para entender o que diferencia um jogador de elite. A pergunta é: quais métricas têm maior associação com o rating, e dá para prever o rating de um jogador?"

### Contextualização (45s)
- O que é rating, de onde vêm os dados, 803 jogadores, estatísticas de carreira.
- Mencionar a troca de dataset da Parte 1 e o motivo (unidade de análise inconsistente antes).

### Demonstração do dashboard (3:30–4:00)

**1. Distribuição do rating** *(30s)*
- Abrir a seção. Apontar para o histograma: "Veja que a maioria dos jogadores está em torno de 1,0. A distribuição é quase simétrica — média e mediana quase iguais."
- Apontar o boxplot: "Os 7 pontos fora do bigode superior são os outliers — ZywOo, s1mple, sh1ro."

**2. Correlações** *(45s)*
- Apontar o gráfico de barras: "KD Ratio tem correlação de 0,98 — quase determina o rating."
- Destaque: "Headshot% tem correlação *negativa* — esse é o achado mais contraintuitivo. Elite não força headshot."
- Abrir o scatter, selecionar headshot% no dropdown: "Vejam a linha de tendência indo para baixo — confirma a correlação negativa."

**3. Perfil regional** *(20s)*
- "As caixas têm tamanho similar — nível parecido entre regiões. O que muda é o estilo, não o desempenho médio."

**4. Medidas-resumo** *(10s)*
- "Aqui temos todas as estatísticas descritivas. Podemos explorar se precisar de algum número específico."

**5. Ranking** *(15s)*
- "Ranking interativo — posso mudar a métrica e ver quem lidera em cada categoria."

**6. Modelo preditivo** *(60s)*
- "Agora a parte mais importante: conseguimos *prever* o rating."
- Mostrar o R²: "O modelo explica 99% da variância do rating."
- Apontar os coeficientes: "Kills/round tem coeficiente +1,19 — o maior impacto. Deaths/round: −0,77. KAST nem aparece como significativo quando controlamos por kills e mortes."
- Abrir o simulador: "Vou simular um jogador médio." → mover o slider de kills/round para cima → "Vejam o rating previsto subir em tempo real."
- "O IP de 95% mostra onde o rating real desse jogador provavelmente cairia — aqui entre 1,00 e 1,02."

### Conclusão (30s)
> "Resumindo: o rating é essencialmente uma medida ofensiva — matar mais e morrer menos explica 99% da variância. O dado mais interessante é o headshot%: negative na correlação simples, positivo quando controlamos por kills — um exemplo clássico de correlação de Simpson. E o modelo de regressão permite que qualquer scout insira as métricas de um jogador e obtenha um rating estimado com intervalo de predição."

---

## 7) Perguntas que podem aparecer

**Por que usar correlação de Pearson e não Spearman?**
As variáveis têm distribuição próxima da normal e a relação nos scatter plots é aproximadamente linear. Pearson é adequado. Spearman seria preferível se houvesse outliers extremos distorcendo a linearidade — o que não é o caso aqui.

**O rating é uma boa variável-alvo?**
É a melhor disponível no dataset. Mas tem limitações: favorece jogadores ofensivos e não captura bem papéis de suporte, IGLs (in-game leaders) e AWPers conservadores.

**Qual a diferença entre impacto e rating?**
Impacto (calculado pelo HLTV) pesa mais kills em situações decisivas (clutches, trades em desvantagem) e penaliza mais mortes repetidas. É um refinamento do rating para qualidade do kill, não só quantidade.

**Por que o R² é tão alto (0,99)?**
O rating HLTV é calculado internamente usando as mesmas métricas por round. A regressão essencialmente "descobre" a fórmula do rating. Não é overfitting — é consistência interna dos dados. O valor pedagógico está em ver *quais* métricas são significativas e *como* os coeficientes se comparam.

**Qual a diferença entre IC e IP?**
O IC 95% da média estima onde está o rating *esperado* de jogadores com aquele perfil (estreito, ~0,001). O IP 95% individual estima onde cai o rating de *um jogador específico* — inclui tanto a incerteza do modelo quanto a variabilidade individual (largo, ~0,024). Para avaliar um jogador real, o IP é o correto.

**Por que KAST perde significância na regressão se tem r = 0,68?**
Quando kills/round e deaths/round já estão no modelo, o KAST não acrescenta poder explicativo *independente*. Sua correlação com rating é mediada por kills e mortes: jogadores consistentes (alto KAST) tendem a matar mais — mas quando isso já está controlado, KAST sozinho não move o rating.

**Por que excluíram KD Ratio e Diferença KD do modelo?**
KD Ratio = total_kills / total_deaths. Diferença KD = total_kills − total_deaths. Ambos são funções diretas de kills e mortes — incluí-los junto com kills/round e deaths/round seria multicolinearidade severa: os coeficientes ficariam instáveis e os erros padrão explodem.

**O modelo serve para prever jogadores reais fora do dataset?**
Com cautela. O modelo foi ajustado em jogadores profissionais de alto nível. Para jogadores amadores ou semi-profissionais, as relações podem ser diferentes. O IP de 95% captura a incerteza para um novo jogador *dentro do perfil profissional*.

---

## 8) Checklist antes de apresentar

- [ ] Rodar: `python3 -m streamlit run app.py`
- [ ] Confirmar que o app carrega sem erros no terminal
- [ ] Testar os filtros da sidebar (país, mínimo de mapas, Top N)
- [ ] Preparar dois cenários de demo:
  - **Cenário A:** sem filtros — visão geral dos 803 jogadores
  - **Cenário B:** filtrar Brasil — comparar perfil local com o global
- [ ] No scatter interativo, deixar pré-selecionado "Headshot (%)" para o momento do insight
- [ ] No simulador de rating, deixar os sliders nos valores padrão (medianas)
- [ ] Praticar o movimento dos sliders de kills/round e deaths/round para a demonstração ao vivo
- [ ] Treinar fala para caber entre 5 e 7 minutos
