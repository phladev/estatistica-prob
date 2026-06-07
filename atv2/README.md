# CS:GO – Análise de Performance (Atividade 2)

Aplicação web interativa para análise descritiva de estatísticas de jogadores profissionais de CS:GO, com foco em responder: **quais métricas de performance têm maior associação com o rating de um jogador?**

## Stack
- Python 3
- Streamlit
- pandas
- plotly
- statsmodels (linha de tendência OLS nos scatter plots)

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
