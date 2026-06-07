# CS:GO – Análise de Performance (Atividade 3)

Aplicação web interativa para análise descritiva e preditiva de estatísticas de jogadores profissionais de CS:GO. Continuação da Atividade 2 (mesmo dashboard e modelo de regressão linear), acrescentando:

- **Avaliação e validação de modelos**: divisão treino/teste, validação cruzada (k-fold), métricas de erro (RMSE, MAE) e análise de resíduos — como saber se um modelo de previsão é realmente bom.
- **Random Forest**: modelo de *machine learning* baseado em um conjunto de árvores de decisão (*bagging*), com gráfico de importância das métricas.
- **Ensemble**: combinação de regressão linear, Random Forest e Gradient Boosting em um único modelo (*Voting Regressor*), com comparação final entre todos os modelos.

**Pergunta central:** quais métricas de performance têm maior associação com o rating de um jogador, e qual abordagem de modelagem prevê esse rating com mais confiança?

## Stack
- Python 3
- Streamlit
- pandas
- plotly
- statsmodels (regressão OLS com IC/IP)
- scikit-learn (Random Forest, Gradient Boosting, Voting Regressor, validação cruzada e métricas)

## Como executar

1. Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

2. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

3. Atualize o pip (recomendado):

```bash
python3 -m pip install --upgrade pip setuptools wheel
```

4. Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

5. Execute o app:

```bash
python3 -m streamlit run app.py
```

## Solução rápida de problemas

- Confirme a versão do Python: `python3 --version` (requer 3.10+)
- Se o pip falhar por permissão, verifique se o ambiente virtual está ativo.
- Se `streamlit: command not found`, use: `python3 -m streamlit run app.py`
- Se `No module named pip`, rode: `python3 -m ensurepip --upgrade`
