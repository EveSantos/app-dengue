"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np

st.title('App Dengue')

@st.cache_data
def load_data():
   df = pd.read_csv('final/df_deng_norm_enriquecido.csv', low_memory=False)
   return df

dados_aux = load_data()
dados = dados_aux[dados_aux['ano_notificacao'] <= 2024].copy()
dados['ano_notificacao'] = pd.to_numeric(dados['ano_notificacao'], errors='coerce')
dados = dados.dropna(subset=['ano_notificacao'])

pop_por_ano = {
   'Ilhéus': {
       2013: 159076, 2014: 161268, 2015: 163220, 2016: 164653,
       2017: 165257, 2018: 165048, 2019: 165392, 2020: 166221,
       2021: 166149, 2022: 166187, 2023: 166500, 2024: 166800
   },
   'Itabuna': {
       2013: 208628, 2014: 210557, 2015: 212740, 2016: 214476,
       2017: 215853, 2018: 222127, 2019: 222693, 2020: 223750,
       2021: 224123, 2022: 224561, 2023: 225000, 2024: 225400
   },
}


def taxa_100k_por_ano(df, cidade, ano_col='ano_notificacao'):
   df = df.copy()
   df[ano_col] = pd.to_numeric(df[ano_col], errors='coerce')
   df = df.dropna(subset=[ano_col])

   casos_por_ano = df.groupby(ano_col).size()
   casos_por_ano.index = casos_por_ano.index.astype(int)

   pop_dict = pop_por_ano[cidade]
   taxa = casos_por_ano.index.map(
       lambda a: casos_por_ano[a] / pop_dict.get(int(a), np.nan) * 100000
   )

   return pd.DataFrame({
       'ano': casos_por_ano.index.astype(int),
       'taxa_100k': taxa,
       'casos': casos_por_ano.values,
   })


df_ilheus = dados[dados['municipio_notificacao'] == 291360]
df_itabuna = dados[dados['municipio_notificacao'] == 291480]

taxa_ilheus = taxa_100k_por_ano(df_ilheus, 'Ilhéus')
taxa_itabuna = taxa_100k_por_ano(df_itabuna, 'Itabuna')

cidades = ['Ilhéus', 'Itabuna']
cidades_selecionadas = st.multiselect(
   'Selecione as cidades',
    cidades,
    default=cidades,
    placeholder="Slecione uma ou mais cidades",
)

if cidades_selecionadas:
   datasets = {
       'Ilhéus': taxa_ilheus[['ano', 'taxa_100k']].rename(columns={'taxa_100k': 'Ilhéus'}),
       'Itabuna': taxa_itabuna[['ano', 'taxa_100k']].rename(columns={'taxa_100k': 'Itabuna'}),
   }

   dataset = datasets[cidades_selecionadas[0]]
   for cidade in cidades_selecionadas[1:]:
       dataset = dataset.merge(datasets[cidade], on='ano', how='outer')

   st.line_chart(dataset.set_index('ano'), use_container_width=True)
