# Calculadora de Notas — Programação Funcional com Python
Este projeto faz parte da atividade parcial da disciplina de **Programação Funcional** do curso de **Análise e Desenvolvimento de Sistemas**, da **Universidade de Fortaleza**.

Trata-se de um projeto acadêmico simples cujo objetivo é **aferir o grau de maturidade** da equipe nos **conceitos e na prática de Programação Funcional (PF)** em Python.

A descrição da atividade proposta pode ser vista em [Atividade Proposta](docs/Atividade_proposta.pdf).

## Nosso sistema

Um app simples desenvolvido em Python, no qual um professor faz upload de um CSV com as notas de seus alunos e o sistema calcula média, mediana, maior, menor, exibe um gráfico de histograma e oferece download de um mini-relatório. 

## Requisitos Funcionais (RF)
- RF01: Fazer upload de um arquivo CSV, contendo as notas dos alunos (colunas: aluno, nota).
- RF02: A partir das notas lidas no arquivo csv, calcular média de notas. 
- RF03: A partir das notas lidas no arquivo csv, calcular mediana das notas.
- RF04: A partir das notas lidas no arquivo csv, calcular a maior nota.
- RF05: A partir das notas lidas no arquivo csv, calcular a menor nota.
- RF06: A partir das notas lidas no arquivo csv, calcular o desvio-padrão das notas.
- RF07: A partir das notas lidas no arquivo csv, calcular a moda.
- RF08: Exibir a quantidade de notas por faixas de valor. Por exemplo, [0-4.9; 5-6.9; 7-8.9;9-10]
- RF09: Exibir a quantidade total de notas processadas. 
- RF10: Exibir o número de alunos aprovados, conforme nota de corte.
- RF11: Exibir gráfico (histograma) das notas.

  
## Requisitos Não Funcionais (RNF)
- RNF01: Interface simples, utilizando a biblioteca Streamlit do Python.
- RNF02: Execução local via streamlit run.
- RNF03: Códifo testável (pytest) e organizado.

##Regras de negócios
- RN01: As notas estão no intervalo de 0 a 10.
- RN02: O sistema deve verificar se o arquivo de notas não está vazio antes de fazer todos os cálculos.
- RN03: Antes de fazer qualquer processamento do arquivo de notas, deve-se verificar se os dados dentro do arquivo csv estão consistentes, se os cabeçalhos está corretos, etc.
- RN04: A nota de corte para aprovação será 7.0.

## Restrições
Utilizar, obrigatoriamente, conceitos de Programação Funcional no código-fonte, compreendendo:
- **Função Lambda** (ver funções `media(lista_de_notas)`, `maior(lista_de_notas)`, `menor(lista_de_notas)` em `core/stats.py`);
- **List Comprehension** (ver função `moda(lista_de_notas)` em `core/stats.py`);
- **Clousure** (ver funções `_cria_aprovador` e `contar_aprovados(lista_de_notas, corte)`);
- **Função de alta ordem** (ver funções `media(lista_de_notas)`, `maior(lista_de_notas)`, `menor(lista_de_notas)` em `core/stats.py`);

## Mapeamento de requisitos -> Funções do código

| Requisito | Onde está no código?                                                                  | Observações      |
| --------- | -------------------------------------------------------------------------------- | ---------------- |
| RF01      | `adapters/csv_io.py`: `ler_csv()`; `app_streamlit.py` (uploader); `valida_csv.py`  | Contém as funções que validam cabeçalho e arquivo csv e fazem a leitura do arquivo|
| RF02      | `core/stats.py`: `media(lista_de_notas)`                           | função pura para calcular a média das notas. Utiliza a função `reduce` (função de alta ordem) para somar as notas contidas na lista de notas passada como parâmetro.      |
| RF03      | `core/stats.py`: `mediana(lista_de_notas)`                                        |função pura para calcular a mediana de notas.   |
| RF04      | `core/stats.py`: `maior(lista_de_notas)`                                    | Função pura que retorna a maior nota da lista de notas passadas como parâmetro. Utiliza `reduce()` para retornar o maior valor da lista de notas.               |
| RF05      | `core/stats.py`: `menor(lista_de_notas)`                                                        | Função pura que retorna a menor nota da lista de notas passadas como parâmetro. Utiliza `reduce()` para retornar o menor valor da lista de notas.         |
| RF06      | `core/stats.py`: `desvio_padrao(lista_de_notas)`                                               | Função pura que retorna o desvio padrão das notas passadas como parâmetro. Utiliza a função `reduce()` para calcular a variância.       |
| RF07      | `core/stats.py`: `moda(lista_de_notas)`                                                      | Função pura utilizada para calcular a moda única. Se houver mais de uma moda, retorna None.  Utiliza list comprehension para verificar a moda.      |
| RF08     | `core/stats.py`: `faixa_de_notas(lista_de_notas)`                                                            | Retorna um dicionário contendo a quantidade de notas em cada faixa de valor. |
| RF09     | `core/stats.py`: `quantidade_notas(lista_de_notas)`           | retorna a quantidade de notas processadas. |
| RF10     | `_cria_aprovador` e `contar_aprovados(lista_de_notas, corte)` em `core/stats.py                            | A função cria_aprovador é uma closure, ou seja, uma fábrica de verificador. Dizemos o corte(ex.: 7.0) e a função devolve uma outra função que responde "aprovador ou reprovado" para qualquer nota. Já a função contar_aprovados: usa a função _cria_aprovador para criar o verficador (com a nota de corte escolhida) e conta quantas notas passam no teste.
| RF11     | `src/app_streamlit.py`                                        | Exibe o gráfico de histograma utilizando a biblioteca matplotlib. |
| RNF01    | `src/app_streamlit.py`                                                           | Interface simples, utilizando a biblioteca Streamlit do Python.|
| RNF02    |`src/app_streamlit.py`                                                                            | Execução local via streamlit run.|
| RNF03    | `tests/test_stats.py`                                                                         | arquivo contendo as funções de teste |

## Papéis dos membros da equipe
- **PO/Documentação (Francisco Riomar Barros Filho)**: manter requisitos, mapear RF/RNF → funções, preparar README/relatório, coletar uso do chatbot.

- **Lógica funcional (Cezarnildo Moreira da Silva e Francisco Augusto de Oliveira Filho)**
  : implementação das funções puras e lógica de negócio - core/stats.py e tests/test_stats.py.

- **Entrada e validação (José Claudecir Silva de Lima e Lucas Pires Albuquerque)**: core/transform.py, adapters/csv_io.py, tests/test_transform.py.

- **(UI e integração) Francisco Rodrigues de Oliveira Lima e Francisco Riomar Barros Filho**: app_streamlit.py, gráficos, tratamento de erros, empacota tudo.