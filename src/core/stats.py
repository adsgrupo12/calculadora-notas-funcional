#Esse é o principal arquivo do trabalho, pois contém as funções utilizadas para fazer cálculos estatísticos
#Aqui é onde utilizamos os conceitos de programação funcional para valer!


#Ativa anotações de tipo mais modernas

from __future__ import annotations
from functools import reduce 
from typing import Callable, Dict, List



def _checar_lista_vazia(notas: List[float]) -> None:
    if not notas:
        raise ValueError("A lista de notas está vazia. Desse modo, não é possível fazer qualquer estatística.") #Se a lista de notas estiver vazia, lança uma exceçao!
    
def quantidade_notas(notas: List[float]) -> int: #RF09 -> retorna a quantidade de registros de notas -> caso não haja erro de processamento em alguma nota.
    return len(notas) 

def media(notas: List[float]) -> float: # -> RF02 -> Basicamente calcula a média
    _checar_lista_vazia(notas)
    soma = reduce(lambda acum, n: acum + n, notas, 0.0) #Vejam a função lambda, utilizada dentro do reduce aqui. Soma todas as notas
    return soma/len(notas)

def mediana(notas: List[float]) -> float: # -> RF03
    _checar_lista_vazia(notas)
    notas_ordenadas = sorted(notas)
    n = len(notas_ordenadas)
    meio = n // 2
    if n % 2 == 1:
        return notas_ordenadas[meio]
    return (notas_ordenadas[meio -1] + notas_ordenadas[meio])/2

def maior(notas: List[float]) -> float: # -> RF04
    _checar_lista_vazia(notas)
    return reduce(lambda a, b: a if a > b else b, notas)

def menor(notas: List[float]) -> float: # -> RF05
    _checar_lista_vazia(notas)
    return reduce(lambda a, b: a if a < b else b, notas)

def desvio_padrao(notas: List[float]) -> float: # -> RF06
    _checar_lista_vazia(notas)
    m = media(notas)
    variancia = reduce(lambda acc, n: acc + (n -  m)**2, notas, 0.0)/len(notas)
    return variancia ** 0.5

#moda única. Se houver mais de uma moda, retorna None.
def moda(notas: list[float]) -> float | None: # - RF07
    _checar_lista_vazia(notas)
    contagem: dict[float, int] = {}
    for n in notas:
        contagem[n] = contagem.get(n, 0) + 1

    max_freq = max(contagem.values()) 
    modas = [k for k, v in contagem.items() if v == max_freq]
    return modas[0] if len(modas) == 1 else None



def faixas_de_notas(notas: List[float]) -> Dict[str,int]: # - RF08
    faixas = {"0-4.9": 0, "5-6.9": 0, "7-8.9":0, "9-10": 0}
    for n in notas:
        if 0.0 <= n <= 4.9:
            faixas["0-4.9"] += 1
        elif 5.0 <= n <= 6.9:
            faixas["5-6.9"] += 1
        elif 7.0 <= n <= 8.9:
            faixas["7-8.9"] += 1
        elif 9.0 <= n <= 10:
            faixas["9-10"] += 1
    return faixas

def _cria_aprovador(corte: float) -> Callable[[float],bool]: # Closure 
    def aprovador(nota: float) -> bool:
        return nota >= corte
    return aprovador

def contar_aprovados(notas: list[float], corte: float = 7.0) -> int:
    if not notas:
        return 0
    aprovador = _cria_aprovador(corte)
    return reduce(lambda acc, n: acc + (1 if aprovador(n) else 0), notas, 0)





