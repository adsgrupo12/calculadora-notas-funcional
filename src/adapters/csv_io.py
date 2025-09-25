# src/adapters/csv_io.py
from __future__ import annotations 
from os import PathLike
from typing import IO, Any, cast
import pandas as pd

COLUNAS = {"aluno", "nota"}
ALIASES: dict[str, str] = { 
}

# Para tipos
Pathish = str | PathLike[str]
FileLike = IO[str] | IO[bytes]


def _rewind(obj: object) -> None:
    """Rebobina um file-like se ele tiver seek()."""
    seek = getattr(obj, "seek", None)
    if callable(seek):
        try:
            seek(0)
        except Exception:
            # não queremos quebrar só porque não deu para rebobinar
            pass


def _read_df(arquivo: Pathish | FileLike, sep: str) -> pd.DataFrame:
    """Wrapper tipado para read_csv, com dtype=str e tolerância a espaços."""
    df_any = pd.read_csv(arquivo, dtype=str, sep=sep, skipinitialspace=True)  # type: ignore[call-overload]
    return cast(pd.DataFrame, df_any)


def ler_csv(arquivo: Pathish | FileLike) -> list[dict[str, str]]:
    """
    Lê CSV (caminho, StringIO, UploadedFile do Streamlit, etc.)
    - Tenta vírgula e, se falhar, ponto e vírgula como separador.
    - Normaliza nomes de colunas (minúsculas, trim) e aplica ALIASES (ex.: 'notas' -> 'nota').
    - Remove espaços nas células e retorna SOMENTE 'aluno' e 'nota' como strings.
    """
    last_err: Exception | None = None
    found_cols: list[str] | None = None

    for sep in (",", ";"):
        try:
            _rewind(arquivo)
            df: pd.DataFrame = _read_df(arquivo, sep)
        except Exception as e:
            last_err = e
            continue

        # Normaliza cabeçalhos (como strings) e aplica apelidos
        colnames = [str(c).strip().lower() for c in df.columns.to_list()]
        df.columns = colnames  # type: ignore[assignment]
        df.rename(columns=ALIASES, inplace=True)

        found_cols = list(df.columns)  # type: ignore[misc]
        cols = set(found_cols)

        if not COLUNAS.issubset(cols):
            # tenta outro separador
            continue

        # Strip em colunas de texto (object)
        for col in list(df.columns):  # type: ignore[misc]
            serie = df[col]
            # .map com lambda mantém tipo object e evita barulho no strict
            df[col] = serie.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Mantém somente as colunas que interessam
        df = df[["aluno", "nota"]]

        # to_dict com orient="records" -> list[dict[str, str]]
        records_any: Any = df.to_dict(orient="records")
        records = cast(list[dict[str, str]], records_any)
        return records

    if found_cols is not None:
        raise ValueError(f"CSV deve conter as colunas {COLUNAS}. Encontrado: {found_cols}")

    if last_err is not None:
        raise last_err

    raise ValueError("Não foi possível ler o CSV.")

