#%%

import pandas as pd
import streamlit as st
import plotly.express as px

# Lendo com separador ; e tratando vírgula como decimal
df1 = pd.read_csv(
    r"C:\Users\Carlos\Desktop\Dashboard python\Dados\4_1_meta_2017.csv",
    sep=";",              # separador correto
    decimal=",",          # vírgula como separador decimal
    on_bad_lines="skip",  # ignora linhas quebradas
    encoding="utf-8"      # garante leitura correta
)

df2 = pd.read_csv(
    r"C:\Users\Carlos\Desktop\Dashboard python\Dados\4_1_meta_2018.csv",
    sep=";", decimal=",", on_bad_lines="skip", encoding="utf-8"
)

df3 = pd.read_csv(
    r"C:\Users\Carlos\Desktop\Dashboard python\Dados\4_1_meta_2019.csv",
    sep=";", decimal=",", on_bad_lines="skip", encoding="utf-8"
)

# Concatenando as três bases
df_final = pd.concat([df1, df2, df3], ignore_index=True)

# Substituir '##' por vazio ou por NaN
df_final = df_final.replace("##", pd.NA)   # usa NaN (melhor para cálculos)
# Se preferir string vazia, troque por: df_final = df_final.replace("##", "")

# Salvando em um novo arquivo
df_final.to_csv(
    r"C:\Users\Carlos\Desktop\Dashboard python\Dados\base_final.csv",
    sep=";", decimal=",", index=False, encoding="utf-8"
)

st.set_page_config(layout="wide")

df_final['DATA'] = pd.to_datetime(df_final['DATA'])

df_final = df_final.sort_values(by="DATA")

df_final["Month"] = df_final["DATA"].apply(lambda x: str(x.year) + "-" + str(x.month))

Month = st.sidebar.selectbox('Mês',df_final["Month"].unique())

df_filtred = df_final[df_final["Month"] == Month ]


col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtred, x="DATA", y="TOTAL_VENDA", color="CAIXA_VENDEDOR", title="FATURAMENTO POR DIA")
col1.plotly_chart(fig_date, use_container_width=True)

fig_can = px.bar(df_filtred, x="DATA", y="VALOR_CANCELADO", color="CAIXA_VENDEDOR", title="VALOR CANCELADO POR DIA")
col2.plotly_chart(fig_can, use_container_width=True)

vendedor_total = df_filtred.groupby('CAIXA_VENDEDOR')[['TOTAL_VENDA']].sum().reset_index()
fig_vendedor = px.bar(vendedor_total, x="CAIXA_VENDEDOR", y="TOTAL_VENDA", color="CAIXA_VENDEDOR", title="FATURAMENTO POR VENDEDOR")
col3.plotly_chart(fig_vendedor, use_container_width=True )


fig_pagamento = px.pie(df_filtred, values="TOTAL_VENDA", names="COD_FORMA_PGTO", title="TIPO DE PAGAMENTO")
col4.plotly_chart(fig_pagamento, use_container_width=True)

# Média de vendas por vendedor
media_vendedor = df_final.groupby('CAIXA_VENDEDOR')[['TOTAL_VENDA']].mean().reset_index()

# Ordena do maior para o menor
media_vendedor = media_vendedor.sort_values(by="TOTAL_VENDA", ascending=False)

# Cria o gráfico
fig_media_vendedor = px.bar(
    media_vendedor,
    x="CAIXA_VENDEDOR",
    y="TOTAL_VENDA",
    color="TOTAL_VENDA",  # intensidade da cor proporcional ao valor
    color_continuous_scale="Blues",
    title="MÉDIA DE VENDAS POR VENDEDOR"
)

# Adiciona rótulos nas barras
fig_media_vendedor.update_traces(texttemplate='%{y:,.0f}', textposition='outside')

# Ajusta layout
fig_media_vendedor.update_layout(
    yaxis_tickformat=",.0f",   # separador de milhar
    xaxis_title="Vendedor",
    yaxis_title="Média de Vendas (R$)",
    xaxis_tickangle=-45,       # gira rótulos do eixo X
    showlegend=False
)

# Linha de referência da média geral
fig_media_vendedor.add_hline(
    y=media_vendedor["TOTAL_VENDA"].mean(),
    line_dash="dash",
    line_color="red",
    annotation_text="Média Geral"
)

# Exibe no Streamlit
col5.plotly_chart(fig_media_vendedor, use_container_width=True)
