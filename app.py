import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('consulta_cand_2024_CE.csv', delimiter=';', encoding='latin1')

st.title("Eleições Municipais 2024 - Ceará")

st.sidebar.header("Filtros")

cargo_options = df['DS_CARGO'].unique()
selected_cargo = st.sidebar.selectbox('Selecionar Cargo', cargo_options)

partido_options = df['SG_PARTIDO'].unique()
selected_partido = st.sidebar.multiselect('Selecionar Partido', partido_options)

filtered_df = df[(df['DS_CARGO'] == selected_cargo)]
if selected_partido:
    filtered_df = filtered_df[filtered_df['SG_PARTIDO'].isin(selected_partido)]

st.subheader(f"Candidatos para {selected_cargo}")
st.dataframe(filtered_df[['NM_CANDIDATO', 'SG_PARTIDO', 'DS_CARGO', 'DS_SIT_TOT_TURNO']])

# 1. Distribuição por Grau de Instrução
st.subheader("Distribuição por Grau de Instrução")
instrucao_counts = filtered_df['DS_GRAU_INSTRUCAO'].value_counts().reset_index()
instrucao_counts.columns = ['Grau de Instrução', 'Número de Candidatos']
fig_instrucao = px.bar(instrucao_counts, x='Grau de Instrução', y='Número de Candidatos', title='Distribuição por Grau de Instrução')
st.plotly_chart(fig_instrucao)

# 2. Grau de Instrução por Gênero
st.subheader("Grau de Instrução por Gênero")
genero_instrucao = filtered_df.groupby(['DS_GENERO', 'DS_GRAU_INSTRUCAO']).size().reset_index(name='Número de Candidatos')
fig_genero_instrucao = px.bar(genero_instrucao, x='DS_GENERO', y='Número de Candidatos', color='DS_GRAU_INSTRUCAO', barmode='stack', title='Grau de Instrução por Gênero')
st.plotly_chart(fig_genero_instrucao)

# 3. Instrução por Cor/Raça
st.subheader("Instrução por Cor/Raça dos Candidatos")
instrucao_raca = filtered_df.groupby(['DS_COR_RACA', 'DS_GRAU_INSTRUCAO']).size().reset_index(name='Número de Candidatos')
fig_instrucao_raca = px.bar(instrucao_raca, x='DS_COR_RACA', y='Número de Candidatos', color='DS_GRAU_INSTRUCAO', barmode='stack', title='Instrução por Cor/Raça')
st.plotly_chart(fig_instrucao_raca)

# 4. Distribuição por Gênero
st.subheader("Distribuição por Gênero")
genero_counts = filtered_df['DS_GENERO'].value_counts().reset_index()
genero_counts.columns = ['Gênero', 'Número de Candidatos']
fig_genero = px.bar(genero_counts, x='Gênero', y='Número de Candidatos', title='Distribuição por Gênero')
st.plotly_chart(fig_genero)

# 5. Quantidade de Candidatas Femininas por Partido
st.subheader("Quantidade de Candidatas Femininas por Partido")
feminino_partido = filtered_df[filtered_df['DS_GENERO'] == 'FEMININO'].groupby('SG_PARTIDO').size().reset_index(name='Número de Candidatas Femininas')
fig_feminino_partido = px.bar(feminino_partido, x='SG_PARTIDO', y='Número de Candidatas Femininas', title='Candidatas Femininas por Partido')
st.plotly_chart(fig_feminino_partido)

# 6. Quantidade de Candidatos Masculinos por Partido
st.subheader("Quantidade de Candidatos Masculinos por Partido")
masculino_partido = filtered_df[filtered_df['DS_GENERO'] == 'MASCULINO'].groupby('SG_PARTIDO').size().reset_index(name='Número de Candidatos Masculinos')
fig_masculino_partido = px.bar(masculino_partido, x='SG_PARTIDO', y='Número de Candidatos Masculinos', title='Candidatos Masculinos por Partido')
st.plotly_chart(fig_masculino_partido)

# 7. Quantidade de Candidatos Masculinos e Femininos por Partido
st.subheader("Quantidade de Candidatos Masculinos e Femininos por Partido")
genero_partido = filtered_df.groupby(['SG_PARTIDO', 'DS_GENERO']).size().reset_index(name='Número de Candidatos')
fig_genero_partido = px.bar(genero_partido, x='SG_PARTIDO', y='Número de Candidatos', color='DS_GENERO', barmode='stack', title='Candidatos Masculinos e Femininos por Partido')
st.plotly_chart(fig_genero_partido)

st.download_button(
    label="Download Dados Filtrados",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='candidatos_filtrados.csv',
    mime='text/csv',
)
