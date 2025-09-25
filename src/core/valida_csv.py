from __future__ import annotations
from typing import Callable, Dict, Iterable, List

# Função para remover espaços extras no começo e no fim de um texto
def remove_espacos(s:str) -> str:
    return s.strip()

def troca_virgula_por_ponto(s: str) -> str:
    return s.replace(",",".")

def converte_nota(nota:str) -> float:
    n = troca_virgula_por_ponto(remove_espacos(nota))

    try:
        return float(n)
    except ValueError:
        raise ValueError(f"Nota inválida: {nota!r}")
    
def validar_nota(nota: float) -> float:
    if 0.0 <= nota <= 10.0:
        return nota
    raise ValueError(f'Nota fora da faixa 0-10: {nota}')

def extrair_nota_linha(linha: Dict[str,str]) -> float:
    if "nota" not in linha:
        raise ValueError("Coluna 'nota' ausente.")
    return validar_nota(converte_nota(linha["nota"]))

'''
def to_notas(linhas):
    resultado = []
    for l in linhas:
        resultado.append(extrair_nota_linha(l))
    return resultado
'''
#utilizando list comprehension...
def to_notas(linhas: Iterable[Dict[str,str]]) -> List[float]:
    return [extrair_nota_linha(l) for l in linhas]

def to_notas_tolerante(linhas: Iterable[Dict[str,str]]) -> List[float]:
    notas: List[float] = []
    for l in linhas:
        try:
            notas.append(extrair_nota_linha(l))
        except ValueError:
            pass
    return notas
    
def cria_aprovador(corte: float) -> Callable[[float], bool]: # Closure -> 
    def aprovador(nota: float) -> bool:
        return nota >=corte
    return aprovador

            