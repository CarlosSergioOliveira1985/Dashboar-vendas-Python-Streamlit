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

df_final

st.set_page_config(layout="wide")

df_final['DATA']

df_final['DATA'] = pd.to_datetime(df_final['DATA'])

df_final["DATA"]

df_final = df_final.sort_values(by="DATA")

df_final["Month"] = df_final["DATA"].apply(lambda x: str(x.year) + "-" + str(x.month))

df_final

Month = st.sidebar._selectbox('Mês',df_final["Month"].unique())