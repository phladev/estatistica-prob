# CSGO Web Analytics - Atividade 1

Aplicacao web interativa para analise descritiva de estatisticas de jogadores e times de CSGO.

## Stack
- Python
- Streamlit
- pandas
- plotly

## Como executar
1. Crie o ambiente virtual com python3:

```bash
python3 -m venv .venv
```

2. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

3. Atualize o pip (recomendado para evitar erro de compatibilidade):

```bash
python3 -m pip install --upgrade pip setuptools wheel
```

4. Instale dependencias:

```bash
python3 -m pip install -r requirements.txt
```

5. Execute o app:

```bash
python3 -m streamlit run app.py
```

## Solucao rapida de problemas de instalacao
- Confirme a versao do Python: `python3 --version`
- Se o pip falhar por permissao, garanta que o ambiente virtual esta ativo antes de instalar.
- Se aparecer "No module named pip", rode: `python3 -m ensurepip --upgrade`
- Se "streamlit: command not found", use: `python3 -m streamlit run app.py`

## O que o dashboard entrega
- Filtros globais (pais, minimo de mapas, faixa de rating, Top N)
- Bonus: seletor de medida-resumo (Mean, Median, Std, Min, Max)
- Ranking dinamico de jogadores e times
- Dispersao rating x total_maps
- Distribuicao de rating (boxplot e histograma)
- Comparacao por pais (mediana de rating)
- Tabelas dinamicas para jogadores e times

## Roteiro rapido (5 a 7 minutos)
1. Contexto e objetivo (30-45s)
- Dataset de jogadores e organizacoes de CSGO.
- Objetivo: analise interativa para extrair insights descritivos.

2. Pontos fortes da aplicacao (2-3min)
- Interatividade: filtros alteram graficos e tabelas em tempo real.
- Comparabilidade: visao lado a lado de jogadores e times.
- Flexibilidade: usuario escolhe metrica e medida-resumo.
- Clareza visual: ranking, dispersao, distribuicao e tabela.

3. Pontos fracos do codigo (1.5-2min)
- Sem serie temporal (nao mostra evolucao no tempo).
- Comparacao entre entidades diferentes (individuo x organizacao).
- Sem testes automatizados e sem tratamento avancado de outliers.
- Dependencia de colunas existentes no CSV (pipeline simples).

4. Fechamento com insight (30-45s)
- Exemplo: alto rating com baixo numero de mapas pode indicar baixa robustez.
- Proximo passo: incluir qualidade de amostra e serie temporal.
