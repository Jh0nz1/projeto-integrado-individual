"""
PARTE E – Jonathan Castro
Foco: horas de afazeres domésticos e cuidado de pessoas por faixa etária e sexo
(filtro "faixa etária" exigido pela persona).
Base: Tabela 9378 (IBGE/SIDRA) – média de horas por sexo e grupo de idade.
Obs.: o IBGE mede afazeres domésticos e cuidado de pessoas JUNTOS (mesmo indicador de horas).
"""

import plotly.express as px
import streamlit as st

import comum as c


def render():
    st.header("E · Afazeres e cuidado de pessoas por faixa etária")
    st.caption("Responsável: Jonathan Castro · Fonte: IBGE – PNAD Contínua, Tabela 9378")

    df = c.carregar_dados(9378, "tabela_9378_idade_tratada.csv", "up_e")
    f = c.filtros(df)
    ufs, br = c.aplicar_filtros(df, f)
    ano = f["anos"][0]
    faixas = c.FAIXAS if f["faixa"] == "Todas" else [f["faixa"]]

    ufs = ufs[ufs["sexo"].isin(["Mulheres", "Homens"])].copy()
    m = ufs.groupby(["recorte", "sexo"])["horas"].mean().unstack().reindex(faixas)
    m["Diferença"] = m["Mulheres"] - m["Homens"]

    for faixa in faixas:
        st.markdown(f"**{faixa}**")
        c.kpis([
            ("Mulheres", f"{c.fmt(m.loc[faixa, 'Mulheres'])} h"),
            ("Homens", f"{c.fmt(m.loc[faixa, 'Homens'])} h"),
            ("Diferença (M − H)", f"{c.fmt(m.loc[faixa, 'Diferença'])} h"),
        ])
    st.caption("Médias das UFs selecionadas, em horas semanais.")

    resumo = m[["Mulheres", "Homens"]].reset_index().melt(id_vars="recorte", var_name="sexo",
                                                           value_name="horas")
    fig = px.bar(resumo, x="recorte", y="horas", color="sexo", barmode="group", text_auto=".1f",
                 color_discrete_map=c.CORES_SEXO, category_orders={"recorte": faixas},
                 labels={"recorte": "Faixa etária", "horas": c.ROTULO_HORAS, "sexo": "Sexo"},
                 title=f"Horas semanais por faixa etária e sexo – {ano}")
    st.plotly_chart(fig, width="stretch")

    sexo_uf = st.radio("Comparar por estado:", ["Mulheres", "Homens"], horizontal=True, key="sexo_e")
    fig2 = px.bar(ufs[ufs["sexo"] == sexo_uf], x="sigla_uf", y="horas", color="recorte",
                  barmode="group", category_orders={"recorte": faixas},
                  labels={"sigla_uf": "Estado (UF)", "horas": c.ROTULO_HORAS, "recorte": "Faixa etária"},
                  title=f"{sexo_uf}: horas semanais por faixa etária e estado – {ano}")
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Análise estatística")
    ufs["grupo"] = ufs["sexo"] + " – " + ufs["recorte"]
    ordem = [f"{s} – {fx}" for s in ["Mulheres", "Homens"] for fx in faixas]
    dados = ufs[["sigla_uf", "grupo", "horas"]].rename(columns={"horas": "valor"})
    dados = dados.set_index("grupo").loc[ordem].reset_index()
    c.bloco_estatistico(dados[["sigla_uf", "grupo", "valor"]], "Sexo e faixa etária")

    st.subheader("Resposta para a persona")
    texto = (f"Em {ano}, nas UFs selecionadas, a diferença entre mulheres e homens aparece em "
             f"todas as faixas exibidas: de {c.fmt(m['Diferença'].min())} h a "
             f"{c.fmt(m['Diferença'].max())} h por semana. ")
    if len(faixas) == 3:
        texto += (f"Ela já existe entre os jovens de 14 a 24 anos ({c.fmt(m.loc[c.FAIXAS[0], 'Diferença'])} h) "
                  f"e é maior na faixa **{m['Diferença'].idxmax()}**. Ou seja, a desigualdade começa "
                  "cedo, na adolescência — políticas de corresponsabilidade também devem chegar "
                  "às escolas e aos jovens.")
    st.markdown(texto + " Obs.: o IBGE mede afazeres domésticos e cuidado de pessoas no mesmo indicador.")

    br_ult = br[br["sexo"].isin(["Mulheres", "Homens"])].groupby("sexo")["horas"].mean()
    if f["faixa"] != "Todas" and {"Mulheres", "Homens"} <= set(br_ult.index):
        c.infografico(br_ult["Mulheres"], br_ult["Homens"], ano, f"Brasil ({f['faixa']})")
    c.secao_noticias(["carga_mental", "economia_cuidado", "ibge"], "parte_e")
