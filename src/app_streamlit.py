# src/app_streamlit.py
from __future__ import annotations

# --- garantir que a raiz do projeto está no sys.path (útil quando o Streamlit muda o cwd) ---
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

# Mostre erros de import na própria página
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    from typing import Sequence, Optional, Any

    from src.adapters.csv_io import ler_csv
    from src.core.valida_csv import to_notas, to_notas_tolerante
    from src.core import stats as S
    from src.core.stats import contar_aprovados
except Exception as e:
    st.title("Erro ao iniciar o app")
    st.exception(e)
    st.stop()

st.set_page_config(page_title="Calculadora de Notas (PF)", page_icon="📊", layout="wide")
st.title("📊 Calculadora de Notas — Programação Funcional")

st.write(
    "Faça upload de um CSV com cabeçalho **`aluno,nota`**. "
    "Ex.: `A001,7.5` ou `A001,\"7,5\"` (se usar vírgula decimal, coloque entre aspas)."
)

st.sidebar.header("⚙️ Opções")
modo = st.sidebar.radio(
    "Como tratar linhas inválidas?",
    options=["Estrito (para na primeira inválida)", "Tolerante (ignora inválidas)"],
    index=0,
)
mostrar_extras = st.sidebar.checkbox("Mostrar extras (moda, desvio-padrão, faixas)", value=True)

uploaded = st.file_uploader("Selecione o arquivo CSV", type=["csv"])
if not uploaded:
    st.info("Aguardando upload do CSV…")
    st.stop()

try:
    # 1) I/O: leitura
    linhas = ler_csv(uploaded)

    # 2) Transformação para floats
    notas: Sequence[float]
    if "Estrito" in modo:
        notas = to_notas(linhas)
    else:
        notas = to_notas_tolerante(linhas)

    if not notas:
        st.warning("Nenhuma nota válida encontrada após o processamento.")
        st.stop()

    # --- MÉTRICAS ---

    aprovados = contar_aprovados(notas,corte=7.0)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total", S.quantidade_notas(notas))
    col2.metric("Média", f"{S.media(notas):.2f}")
    col3.metric("Mediana", f"{S.mediana(notas):.2f}")
    col4.metric("Maior", f"{S.maior(notas):.2f}")
    col5.metric("Menor", f"{S.menor(notas):.2f}")
    col6.metric("Aprovados (>= 7.0)", S.contar_aprovados(notas, corte=7.0))

    # --- EXTRAS ---
    moda_val: Optional[float] = None
    if mostrar_extras:
        with st.expander("🔎 Estatísticas adicionais"):
            moda_val = S.moda(notas)  # Optional[float]
            dp: float = S.desvio_padrao(notas)

            st.write(f"**Moda:** {moda_val if moda_val is not None else '— (empate ou inexistente)'}")
            st.write(f"**Desvio padrão (populacional):** {dp:.3f}")

            dist: dict[str, int] = S.faixas_de_notas(notas)
            df_dist: pd.DataFrame = pd.DataFrame(
                {"faixa": list(dist.keys()), "quantidade": list(dist.values())}
            )
            st.dataframe(df_dist, use_container_width=True)

    # --- HISTOGRAMA ---
    st.subheader("Histograma de notas")
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()
    ax.hist(notas, bins=[0, 5, 7, 9, 10], edgecolor="black")
    ax.set_xlim(0, 10)
    ax.set_xticks([0, 5, 7, 9, 10])
    ax.set_xlabel("Notas")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

    # --- MINI-RELATÓRIO PARA DOWNLOAD ---
    def _to_str(x: Any) -> str:
        return "" if x is None else str(x)

    relatorio: dict[str, Any] = {
        "total": S.quantidade_notas(notas),
        "media": round(S.media(notas), 2),
        "mediana": round(S.mediana(notas), 2),
        "maior": round(S.maior(notas), 2),
        "menor": round(S.menor(notas), 2),
        "aprovados_>7.0": S.contar_aprovados(notas, corte=7.0),
        "moda": moda_val if mostrar_extras else None,
        "desvio_padrao_pop": round(S.desvio_padrao(notas), 3) if mostrar_extras else None,
    }
    csv_out = "chave,valor\n" + "\n".join(f"{k},{_to_str(v)}" for k, v in relatorio.items())
    st.download_button(
        "⬇️ Baixar mini-relatório (CSV)",
        data=csv_out.encode("utf-8"),
        file_name="relatorio_notas.csv",
        mime="text/csv",
    )

except Exception as e:
    st.error(f"Erro ao processar o arquivo: {e}")
    st.stop()
