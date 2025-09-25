import math
import pytest

from src.core.stats import (
    quantidade_notas, media, mediana, maior, menor, moda, desvio_padrao, faixas_de_notas
)

def test_total():
    notas = [5.5,6.7,4.3,8.0]
    resultado = quantidade_notas(notas)
    assert resultado == 4

def test_media():
    notas = [4.0, 6.0,8.0,10.0]
    resultado = media(notas)
    assert resultado == 7

def test_mediana_impar():
    assert mediana([10.0,1.0,5.0]) == 5.0 

def test_mediana_par():
    assert mediana([6.0, 8.0, 4.0, 7.0]) == 6.5  #(6.0 + 7.0)/2 

def test_maior_menor():
    notas = [7.5,9.0,3.0,10.0,5.0]
    assert maior(notas) == 10.0
    assert menor(notas) == 3.0

def test_moda_unica():
    assert moda([7.0, 8.0,8.0,9.0]) == 8.0

def test_moda_empate():
    assert moda([7.0,7.0,8.0,8.0,9.0]) is None

def test_desvio_padrao_pop():
    notas = [2.0,4.0,4.0,4.0,5.0,5.0,7.0,9.0]
    assert math.isclose(desvio_padrao(notas),2.0,rel_tol=1e-12,abs_tol=0.0)

def test_erros_lista_vazia():
    with pytest.raises(ValueError):
        media([])
    with pytest.raises(ValueError):
        mediana([])
    with pytest.raises(ValueError):
        maior([])
    with pytest.raises(ValueError):
        menor([])
    with pytest.raises(ValueError):
        desvio_padrao([])
    with pytest.raises(ValueError):
        moda([])

def test_faixas_de_notas():
    notas = [0.0, 4.9, 5.0, 6.9, 7.0, 8.9, 9.0, 10.0]
    assert faixas_de_notas(notas) == {"0-4.9": 2, "5-6.9": 2, "7-8.9": 2, "9-10": 2}
