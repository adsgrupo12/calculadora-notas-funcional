# tests/test_transform.py
#LEMBRAR DE ALTERAR ESSE MÓDULO

#===========================================


import pytest
from src.core.valida_csv import (
    remove_espacos, troca_virgula_por_ponto,
    converte_nota, validar_nota,
    extrair_nota_linha,
    to_notas, to_notas_tolerante,
    cria_aprovador,
)

# AAA = Arrange (prepara) -> Act (age) -> Assert (verifica)

def test_limpar_e_normalizar():
    # Arrange
    s = "  7,5  "
    # Act
    s1 = remove_espacos(s)
    s2 = troca_virgula_por_ponto(s1)
    # Assert
    assert s1 == "7,5"
    assert s2 == "7.5"

def test_converte_nota_valida():
    assert converte_nota(" 7,5 ") == 7.5
    assert converte_nota("10") == 10.0

def test_converte_nota_invalida():
    with pytest.raises(ValueError):
        converte_nota("abc")

def test_validar_nota_limites():
    assert validar_nota(0.0) == 0.0
    assert validar_nota(10.0) == 10.0

def test_validar_nota_fora_da_faixa():
    with pytest.raises(ValueError):
        validar_nota(-0.1)
    with pytest.raises(ValueError):
        validar_nota(10.1)

def test_extrair_nota_linha_ok():
    linha = {"aluno": "A1", "nota": " 8,0 "}
    assert extrair_nota_linha(linha) == 8.0

def test_extrair_nota_linha_sem_campo():
    linha = {"aluno": "A1"}
    with pytest.raises(ValueError):
        extrair_nota_linha(linha)

def test_to_notas_estrito_levanta_erro():
    linhas = [
        {"aluno": "A1", "nota": "7,5"},
        {"aluno": "A2", "nota": "abc"},   # inválida
        {"aluno": "A3", "nota": "10"},
    ]
    with pytest.raises(ValueError):
        to_notas(linhas)

def test_to_notas_tolerante_ignora_invalidas():
    linhas = [
        {"aluno": "A1", "nota": "7,5"},
        {"aluno": "A2", "nota": "abc"},   # inválida
        {"aluno": "A3", "nota": "10"},
    ]
    assert to_notas_tolerante(linhas) == [7.5, 10.0]

def test_make_aprovador_closure():
    aprovador7 = cria_aprovador(7.0)
    assert aprovador7(6.9) is False
    assert aprovador7(7.0) is True
    assert aprovador7(9.5) is True
