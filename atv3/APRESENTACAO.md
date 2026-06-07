# Roteiro de Apresentação – Atividade 3 (7 a 10 min)

> Esta atividade parte do dashboard da Atividade 2 (mesma base de dados, mesmas seções
> descritivas e o modelo de regressão linear) e acrescenta três blocos novos, focados em
> **avaliar se um modelo de previsão é confiável** e em **comparar abordagens de modelagem**:
> validação de modelos (treino/teste, validação cruzada, resíduos), **Random Forest**
> (machine learning) e **modelos ensemble** (combinação de vários modelos). As seções 3.1 a
> 3.6 abaixo são as mesmas da Atividade 2 — voltam aqui apenas como contexto para as novas
> seções 3.7 a 3.9.

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

> **"Quais métricas de performance individual têm maior associação com o rating de um jogador profissional de CS:GO — é possível prever o rating a partir dessas métricas, e como saber se essa previsão é, de fato, confiável?"**

**Por que essa pergunta faz sentido com esses dados?**
- O rating é a variável-alvo natural: é o número que times, analistas e fãs usam para comparar jogadores.
- Com 18 métricas disponíveis, é possível medir a correlação de cada uma com o rating e construir um modelo preditivo.
- A dimensão regional adiciona contexto: estilos de jogo variam entre culturas competitivas (Europa, América, Ásia).
- **Construir um modelo é fácil; saber se ele é bom é o que separa uma análise séria de um número bonito.** Por isso esta atividade soma à Atividade 2 uma pergunta nova — *"como avaliar se um modelo de previsão é bom?"* — e usa a resposta para comparar a regressão linear com duas abordagens de *machine learning*: Random Forest e ensemble.

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

### 3.7 O modelo de previsão é bom? Avaliação e validação

**Gráficos:** Métricas treino vs. teste + Tabela e gráfico de validação cruzada (5-fold) + Scatter e histograma de resíduos.

#### O problema que esta seção resolve
O R² = 0,99 da seção anterior foi calculado **nos mesmos dados usados para ajustar o modelo**.
Isso responde "o modelo encaixa bem nos dados que ele já viu?" — mas não responde à pergunta
que realmente importa: **"o modelo vai prever bem o rating de um jogador novo, que ele nunca
viu?"**. Um modelo pode ter R² altíssimo no treino e ainda assim prever mal — isso se chama
***overfitting*** (o modelo "decorou" os dados em vez de aprender o padrão geral). Esta seção
apresenta três ferramentas para checar isso de verdade.

#### 1. Divisão treino/teste

| Conjunto | Tamanho | Papel |
|---|---|---|
| Treino | 75% dos jogadores | Usado para *ajustar* o modelo |
| Teste | 25% dos jogadores | Reservado, nunca visto durante o ajuste — usado só para *avaliar* |

| Métrica | Treino | Teste | Leitura |
|---|---|---|---|
| R² | 0,9924 | 0,9888 | Gap de apenas **0,0036** — o modelo generaliza bem |
| RMSE (teste) | — | 0,0066 | Erro médio de previsão: ~0,007 pontos de rating |
| MAE (teste) | — | 0,0054 | Erro absoluto médio — mais robusto a outliers que o RMSE |

**Como ler o "gap" treino−teste:** se o R² do treino fosse, por exemplo, 0,99 e o do teste
caísse para 0,80, seria um sinal claro de overfitting. Aqui o gap é praticamente zero — o
modelo aprendeu o **padrão geral**, não decorou os jogadores específicos do treino.

> **RMSE vs. MAE:** RMSE eleva os erros ao quadrado antes de tirar a média — por isso pune mais
> os erros grandes (é mais sensível a outliers). MAE tira a média dos erros absolutos — trata
> todo erro de forma proporcional. Quando RMSE > MAE (como aqui: 0,0066 > 0,0054), há alguns
> erros maiores puxando o RMSE para cima — mas a diferença pequena mostra que não há erros
> extremos preocupantes.

#### 2. Validação cruzada (k-fold)

Um único corte treino/teste pode ser sortudo ou azarado — por acaso, os jogadores mais difíceis
de prever podem ter caído todos no treino (ou todos no teste). A **validação cruzada k-fold**
resolve isso: divide os dados em *k* partes (aqui, *k* = 5), treina em 4 delas e testa na
restante, repetindo o processo 5 vezes — cada parte serve uma vez como teste.

| Fold | R² |
|---|---|
| 1 | 0,9901 |
| 2 | 0,9894 |
| 3 | 0,9926 |
| 4 | 0,9923 |
| 5 | 0,9914 |

**R² médio: 0,9912 ± 0,0012**

**O que dizer:** "Os cinco scores variam muito pouco entre si — de 0,989 a 0,993. Isso significa
que o desempenho do modelo **não depende de sorte na hora de separar os dados**: ele é estável,
não importa qual recorte da amostra cai no treino ou no teste."

#### 3. Análise de resíduos

Resíduo = valor real − valor previsto. Um modelo bem ajustado tem resíduos **espalhados
aleatoriamente em torno de zero**, sem formar padrões.

- **Scatter (resíduo × valor previsto):** se os pontos formassem um funil (mais dispersos à
  direita ou à esquerda) ou uma curva, seria sinal de que o modelo erra sistematicamente em
  certas faixas de rating. Aqui, a nuvem de pontos é homogênea ao longo de todo o eixo X.
- **Histograma dos resíduos:** mostra a forma aproximadamente de sino, centrada em zero —
  poucos erros grandes, muitos erros pequenos, sem viés sistemático para cima ou para baixo
  (média dos resíduos ≈ 0,00001).

**O que dizer:** "Não há padrão nos resíduos — eles formam uma nuvem homogênea em torno de
zero. Isso reforça que a regressão linear é uma escolha adequada: a relação entre as métricas
por round e o rating é, de fato, predominantemente linear, e o modelo não está deixando
sistematicamente de capturar nada relevante."

---

### 3.8 Random Forest: previsão com *machine learning*

**Gráficos:** Tabela comparativa de métricas + Gráfico de importância das métricas (*feature importance*).

#### O que é Random Forest?
A regressão linear assume que cada métrica empurra o rating sempre na mesma proporção — uma
linha reta. O **Random Forest** é um algoritmo de *machine learning* que constrói **centenas de
árvores de decisão**, cada uma treinada com uma amostra aleatória dos jogadores e um
subconjunto aleatório das métricas (técnica chamada ***bagging*** — *bootstrap aggregating*),
e tira a **média das previsões** de todas elas. Isso permite capturar relações não lineares e
interações entre métricas que uma única reta não enxerga.

#### Random Forest vs. Regressão Linear (mesmo treino e teste)

| Métrica | Regressão Linear | Random Forest |
|---|---|---|
| R² (treino) | 0,9924 | 0,9906 |
| R² (teste) | 0,9888 | 0,9703 |
| RMSE (teste) | 0,0066 | 0,0107 |
| MAE (teste) | 0,0054 | 0,0073 |
| R² médio (5-fold) | 0,9912 ± 0,0012 | 0,9714 ± 0,0057 |

**O que dizer:** "Curiosamente, o Random Forest — um modelo mais sofisticado — teve
desempenho **um pouco pior** que a regressão linear simples. Isso não é um defeito do
algoritmo: é uma confirmação de que a relação entre as métricas por round e o rating é
**praticamente linear**. Árvores de decisão são ótimas para capturar relações complexas e não
lineares — mas quando a relação real já é uma reta, elas têm mais dificuldade em aproximá-la
do que um modelo que já assume linearidade desde o início. **O modelo certo depende dos dados,
não da complexidade do algoritmo.**"

#### Importância das métricas (*feature importance*)

O Random Forest mede, para cada métrica, o quanto ela contribui, em média, para reduzir o erro
de previsão ao longo de todas as árvores da floresta — uma forma de **explicar** um modelo que,
por si só, é uma caixa relativamente opaca.

| Métrica | Importância |
|---|---|
| Kills/Round | **89,2%** |
| Deaths/Round | 8,7% |
| KAST | 1,4% |
| Impacto | 0,3% |
| Headshot% | 0,2% |
| Dano de Granada/Round | 0,1% |
| Assistências/Round | 0,1% |

**O que dizer:** "O Random Forest, sozinho, sem qualquer pista além dos números, 'descobriu'
que **kills/round concentra quase 90% da importância** — o que confirma, por outro caminho
inteiramente diferente, a altíssima correlação de Pearson (r = 0,94) vista no início da
apresentação. As demais métricas contribuem pouco de forma isolada — não porque sejam
irrelevantes, mas porque sua relação com o rating já está em boa parte capturada pela métrica
líder. É a mesma lógica de multicolinearidade que nos fez excluir KD Ratio do modelo de
regressão."

---

### 3.9 Ensemble: combinando vários modelos em um só

**Gráficos:** Tabela comparativa final + Gráfico de barras de RMSE por modelo.

#### O que é um modelo ensemble?
Cada modelo erra de um jeito diferente: a regressão linear é estável e interpretável, mas
rígida; o Random Forest captura não linearidades, mas pode reagir de forma diferente a
jogadores atípicos; o **Gradient Boosting** constrói árvores em sequência, cada uma corrigindo
o erro da anterior — é preciso, mas mais sensível a ruído. Um **modelo ensemble** combina as
previsões de vários modelos diferentes — aqui, pela **média das previsões individuais**
(técnica chamada ***Voting Regressor***) — apostando que os erros de um modelo sejam
compensados pelos acertos de outro. Isso tende a **reduzir a variância** da previsão final e
deixar o resultado mais robusto a peculiaridades de qualquer modelo isolado.

#### Comparação final entre todos os modelos (mesmo treino e teste)

| Modelo | R² (treino) | R² (teste) | RMSE (teste) | MAE (teste) |
|---|---|---|---|---|
| Regressão Linear | 0,9924 | 0,9888 | **0,0066** | 0,0054 |
| Random Forest | 0,9906 | 0,9703 | 0,0107 | 0,0073 |
| Gradient Boosting | 0,9947 | 0,9815 | 0,0085 | 0,0063 |
| **Ensemble (Voting)** | 0,9940 | 0,9837 | 0,0079 | 0,0059 |

**O que dizer:** "O ensemble combina os três modelos acima e fica **no meio do pelotão** — bem
melhor que o Random Forest sozinho, próximo do Gradient Boosting, mas ainda atrás da regressão
linear pura. Isso é didático: o **ensemble não é mágica**. Ele tende a 'puxar a média' dos
modelos que o compõem. Quando, como aqui, um dos modelos individuais (a regressão linear) já é
claramente o melhor para esses dados — porque a relação é linear — somar modelos mais fracos a
ele só dilui o resultado. **O ganho do ensemble aparece quando os modelos cometem erros
diferentes entre si**: nesse caso, a combinação reduz o risco de depender de um único modelo e
tende a superar qualquer um deles isoladamente. Aqui, os três modelos já erram de forma
parecida — porque o problema, no fundo, é quase linear — então o ensemble apenas empata
com uma combinação razoável, sem suplantar o melhor modelo individual."

> **Conclusão da comparação:** para este problema específico, **a regressão linear simples é o
> melhor modelo** — não por ser mais simples, mas porque a relação entre as métricas por round
> e o rating realmente é, na prática, linear. O valor desta seção não é "achar o modelo
> vencedor", e sim mostrar **como comparar modelos de forma justa** (mesmo treino/teste, mesmas
> métricas) e entender **por que** um modelo mais simples pode superar opções mais sofisticadas.

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

8. **R² alto no treino não é prova de um bom modelo — validação é o que prova**
   O gap treino−teste de apenas 0,0036 e os scores estáveis na validação cruzada (0,9912 ± 0,0012)
   é que mostram que o modelo generaliza bem. Sem isso, R² = 0,99 poderia ser apenas overfitting.

9. **O modelo mais sofisticado nem sempre é o melhor**
   Random Forest (R² teste = 0,970) e Gradient Boosting (0,982) ficaram **abaixo** da regressão
   linear simples (0,989). Quando a relação real entre os dados é linear, modelos lineares vencem
   modelos não lineares — complexidade extra só adiciona ruído.

10. **Random Forest confirma, por um caminho totalmente diferente, o que a correlação já apontava**
    Sem nenhuma informação sobre correlações, o algoritmo "descobriu" sozinho que kills/round
    concentra ~89% da importância na previsão — o mesmo achado central da análise de correlação.

11. **Ensemble não é mágica — ele tende à média dos modelos que o compõem**
    Combinar três modelos rendeu um resultado intermediário (R² teste = 0,984), não superior ao
    melhor modelo individual. Ensembles ajudam mais quando os modelos individuais cometem erros
    *diferentes* entre si — não quando um deles já é claramente o mais adequado ao problema.

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
> "Este trabalho usa dados do HLTV.org — a maior plataforma de estatísticas do CS:GO profissional — para entender o que diferencia um jogador de elite. A pergunta desta atividade vai um passo além da anterior: além de saber quais métricas explicam o rating e construir um modelo para prevê-lo, queremos responder **como saber se esse modelo é realmente bom** — e comparar a regressão linear com abordagens de machine learning, como Random Forest e ensembles."

### Contextualização (45s)
- O que é rating, de onde vêm os dados, 803 jogadores, estatísticas de carreira.
- Mencionar que esta atividade reaproveita o dashboard da Atividade 2 e soma três blocos novos no final: validação de modelos, Random Forest e ensemble.

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

**7. O modelo é bom? Avaliação e validação** *(70s)*
- "Até aqui medimos o R² nos mesmos dados que usamos para treinar o modelo. Mas isso não prova que ele prevê bem jogadores novos — só que ele se ajusta bem ao que já viu. Para validar de verdade, separamos 75% dos dados para treino e 25% para teste — dados que o modelo nunca viu."
- "Olhem: R² no treino = 0,99, R² no teste = 0,99. O *gap* é praticamente zero — não há overfitting, o modelo generaliza bem."
- "Para ter mais confiança ainda, rodamos validação cruzada com 5 divisões diferentes: os scores variam de 0,989 a 0,993 — bem estáveis. O resultado não depende de sorte na hora de separar os dados."
- Mostrar o gráfico de resíduos: "E aqui, os erros do modelo: estão espalhados aleatoriamente em torno de zero, sem nenhum padrão — sinal de que o modelo linear é, de fato, adequado para esses dados."

**8. Random Forest — machine learning** *(50s)*
- "Vamos comparar com um modelo de machine learning: o Random Forest, que combina centenas de árvores de decisão e tira a média das previsões delas."
- Mostrar a tabela comparativa: "Surpresa: o Random Forest teve desempenho *pior* que a regressão linear — R² no teste caiu de 0,99 para 0,97. Isso não é defeito do algoritmo: é prova de que a relação entre as métricas e o rating já é praticamente linear, então um modelo mais complexo não tem o que ganhar aqui."
- Mostrar o gráfico de importância: "E olha que interessante — sem que ninguém dissesse nada sobre correlações, o próprio algoritmo 'descobriu' que kills/round concentra quase 90% da importância na previsão. Bate exatamente com o que vimos lá na correlação de Pearson."

**9. Ensemble — combinando modelos** *(40s)*
- "Por fim, um modelo ensemble: ele combina as previsões da regressão linear, do Random Forest e de um terceiro modelo, o Gradient Boosting, tirando a média entre eles."
- Mostrar a tabela final: "O resultado fica no meio do caminho — melhor que o Random Forest sozinho, mas ainda atrás da regressão linear pura. Isso mostra que ensemble não é mágica: ele tende a 'puxar a média' dos modelos que combina. Quando um deles já é claramente o melhor para o problema — como a regressão linear aqui — somar modelos mais fracos só dilui o resultado."

### Conclusão (40s)
> "Resumindo: o rating é essencialmente uma medida ofensiva — matar mais e morrer menos explica 99% da variância — e a relação entre essas métricas e o rating é, na prática, linear. Verificamos isso de duas formas: validando o modelo de regressão com treino/teste e validação cruzada, que confirmaram que ele generaliza bem sem overfitting; e comparando com Random Forest e ensemble, que tiveram desempenho igual ou pior — não porque sejam ruins, mas porque o problema não pede complexidade extra. A lição central desta atividade não é só 'construir um modelo', e sim **saber comprovar que ele é confiável e escolher a abordagem certa para os dados que se tem**."

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

**O que é overfitting e como sabemos que não aconteceu aqui?**
Overfitting é quando o modelo "decora" os dados de treino — incluindo seu ruído e particularidades — em vez de aprender o padrão geral, e por isso prevê mal dados novos. Detectamos isso comparando o desempenho em dados que o modelo viu (treino) com dados que ele não viu (teste): se o R² do treino for muito maior que o do teste, há overfitting. Aqui o gap é de apenas 0,0036 — sinal de que o modelo generaliza bem.

**Por que usar validação cruzada se já temos divisão treino/teste?**
Uma única divisão treino/teste pode, por acaso, deixar os jogadores "mais difíceis" de prever todos do mesmo lado — o resultado dependeria de sorte. A validação cruzada repete a divisão várias vezes (5 vezes, no nosso caso) e olha para a *distribuição* dos resultados, não para um único número. Scores parecidos entre as repetições (aqui, 0,989 a 0,993) mostram que o desempenho é estável e não é fruto de uma divisão favorável.

**Por que o Random Forest teve desempenho pior que a regressão linear?**
Porque a relação entre as métricas por round e o rating já é, na prática, linear — o próprio HLTV calcula o rating como uma combinação dessas métricas. Árvores de decisão são desenhadas para capturar relações não lineares e interações complexas; quando a relação real é uma reta, elas têm mais dificuldade em aproximá-la do que um modelo que já assume linearidade. **A escolha do modelo deve seguir a natureza dos dados, não a fama do algoritmo.**

**O que é "feature importance" no Random Forest, e ele concorda com a regressão linear?**
É uma medida de quanto cada métrica contribui, em média, para reduzir o erro de previsão ao longo de todas as árvores da floresta — uma forma de explicar um modelo que, por natureza, é menos transparente que uma equação de regressão. Sim: o Random Forest concluiu, de forma independente, que kills/round concentra ~89% da importância — o mesmo achado central da análise de correlação (r = 0,94) e dos coeficientes da regressão. Três métodos diferentes chegando à mesma conclusão é um forte sinal de que o achado é real, não coincidência.

**O que é um modelo ensemble, e por que ele não venceu os demais?**
É uma técnica que combina as previsões de vários modelos — aqui, pela média simples (Voting Regressor) entre regressão linear, Random Forest e Gradient Boosting — na expectativa de que os erros de um sejam compensados pelos acertos de outro. Ensembles funcionam melhor quando os modelos que os compõem **erram de formas diferentes**: nesse caso a combinação reduz o risco de depender de um modelo só. Aqui, como o problema é praticamente linear, os três modelos tendem a errar de forma parecida — e o ensemble acaba "puxando a média" entre um modelo muito bom (regressão) e dois um pouco piores (RF e GB), terminando no meio do pelotão em vez de superar o melhor deles.

**Então, qual modelo deveríamos usar na prática?**
A regressão linear — é o que teve melhor desempenho no teste (R² = 0,989, menor RMSE) **e** é o mais simples e interpretável dos quatro: dá para olhar para os coeficientes e explicar exatamente o porquê de cada previsão, algo que Random Forest, Gradient Boosting e ensemble não oferecem com a mesma clareza. Um modelo mais simples que performa igual ou melhor é sempre preferível — é mais fácil de explicar, de manter e de confiar.

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
- [ ] **Lembrar que as seções novas (validação, Random Forest, ensemble) usam a mesma divisão treino/teste — por isso os números de "Regressão Linear" se repetem nas três tabelas comparativas (não é erro)**
- [ ] Ensaiar a transição entre "modelo preditivo" → "isso é confiável?" → "como ele se compara a machine learning?"
- [ ] Ter pronta a frase-chave da conclusão: "o modelo certo é o que combina com a natureza dos dados, não o mais complexo"
- [ ] Treinar fala para caber entre 7 e 10 minutos (atividade tem mais conteúdo que a anterior)
