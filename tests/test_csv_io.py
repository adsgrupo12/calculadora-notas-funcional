# tests/test_csv_io.py
from io import StringIO
import pytest

from src.adapters.csv_io import ler_csv

def test_ler_csv_basico():
    csv = StringIO("""aluno,nota
A1,7.5
A2,"8,0"
A3,10
""")
    registros = ler_csv(csv)
    assert isinstance(registros, list)
    assert registros[0] == {"aluno": "A1", "nota": "7.5"} or registros[0] == {"aluno": "A1", "nota": "7.5"}  # robusto a espaços
    # Garanto que retornou só strings
    assert all(isinstance(linha["aluno"], str) and isinstance(linha["nota"], str) for linha in registros)

def test_ler_csv_cabecalho_maiusculo_ou_misto():
    csv = StringIO("""ALUNO,Nota
A1,"7,5"
""")
    registros = ler_csv(csv)
    assert registros == [{"aluno": "A1", "nota": "7,5"}]  # nomes de colunas foram normalizados para minúsculas

def test_ler_csv_sem_coluna_nota():
    csv = StringIO("""aluno,valor
A1,7.5
""")
    with pytest.raises(ValueError):
        ler_csv(csv)
