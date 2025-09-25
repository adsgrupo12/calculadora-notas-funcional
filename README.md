# Calculadora de Notas — Programação Funcional com Python
Este projeto faz parte da atividade parcial da disciplina de **Programação Funcional** do curso de **Análise e Desenvolvimento de Sistemas**, da **Universidade de Fortaleza**.

Trata-se de um projeto acadêmico simples cujo objetivo é **aferir o grau de maturidade** da equipe nos **conceitos e na prática de Programação Funcional (PF)** em Python.

A descrição da atividade proposta pode ser vista em [Atividade Proposta](docs/Atividade_proposta.pdf).

## Nosso sistema

Um app simples desenvolvido em Python, no qual um professor pode fazer upload de um arquivo CSV com as notas de seus alunos e o sistema calcula média, mediana, maior, menor, moda, desvio-padrão, distribuição por faixas de notas, exibe um gráfico de histograma e oferece download de um mini-relatório, contendo as estatísticas geradas. 

## Especificação de Requisitos
O documento de especificação de requisitos pode ser encontrado na pasta [`docs\Especificacao_requisitos.md`](docs\Especificacao_requisitos.md)

---

## Estrutura do projeto
```

/
├─ src/
│  ├─ core/                # Regras de negócio (FUNÇÕES PURAS)
│  │  ├─ stats.py          # módulo contendo as funções estatísticas como média, mediana, maior, menor, etc.
│  │  └─ valida_csv.py      # contém funções de validação do arquivo csv (parse/validação - sem I/O)
│  ├─ adapters/
│  │  └─ csv\_io.py         # leitura do CSV (I/O isolado)
│  └─ app\_streamlit.py     # interface Streamlit
├─ tests/                  # testes (pytest)
│  └─ test_stats.py    #contém os testes das funções estatísticas
├─ data/
│  └─ notas.csv    # arquivo CSV de exemplo
├─ docs/
│  ├─ Especificacao\_Requisitos.md     # RF/RNF e mapeamentos, conforme solicitado na atividade proposta
├─ requirements.txt         # dependências para EXECUTAR o app
└─ README.md

````

---

## Pré-requisitos
- **Python** 3.12.2 (ou compatível).
- **pip atualizado**
- **Bibliotecas**: pandas, streamlit e matplotlib.
- **Conhecimento dos conceitos de programação funcional**, sobretudo funções puras, funções lambda, list comprehension, closure e funções de alta ordem.
---

## Como rodar o projeto

### 1) Criar e ativar um ambiente virtual
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

**macOS / Linux (bash/zsh):**
```
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Instalar as dependências
```
 pip install -r requirements.txt
```
### 3) Rodar a aplicação
```
streamlit run src/app_streamlit.py
```

### Como usar

1. Clique em “Carregar CSV” e selecione seu arquivo.

2. O CSV deve conter as colunas aluno e nota.

    - Aceita cabeçalhos alternativos: alunos → aluno, notas → nota;

    - Aceita separador vírgula (,) ou ponto-e-vírgula (;);

    - Espaços extras nas células são removidos automaticamente.
    - Incluímos um arquivo de dados de teste em `data/notas.csv`

3. Métricas exibidas: Total, Média, Mediana, Maior, Menor, Aprovados (> 7.0).
(Extras como Moda e Desvio-padrão aparecem se você habilitar a opção no app.)

### 4) Rodar os testes
```
pytest -q
```