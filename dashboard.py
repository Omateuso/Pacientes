import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    file_path = "dataset/pacientes.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

st.title("Análise de Pacientes")

st.subheader("Visão Geral dos Pacientes")
st.metric("Total de Pacientes", len(df))
st.metric("Taxa de Diabetes (%)", round(df['Outcome'].mean()*100, 2))

st.subheader("Distribuição dos Perfis Nutricionais")
fig_perfil = px.histogram(df, x='Perfil', title='Distribuição dos Perfis Nutricionais', color='Perfil')
st.plotly_chart(fig_perfil)

st.subheader("Distribuição de Atributos Médicos")
option = st.selectbox("Escolha um atributo", ['Glucose', 'BloodPressure', 'BMI', 'Age'])
fig_hist = px.histogram(df, x=option, title=f'Distribuição de {option}', color='Outcome', barmode='overlay')
st.plotly_chart(fig_hist)

st.subheader("Correlação entre Fatores")
fig_scatter = px.scatter(df, x='Glucose', y='BMI', color='Outcome', title='Glicose vs. BMI')
st.plotly_chart(fig_scatter)

st.subheader("Diabetes por Faixa Etária")
df['Faixa Etária'] = pd.cut(df['Age'], bins=[0, 20, 40, 60, 80, 100], labels=['0-20', '21-40', '41-60', '61-80', '80+'])
fig_faixa = px.bar(df.groupby('Faixa Etária')['Outcome'].mean().reset_index(), x='Faixa Etária', y='Outcome', title='Taxa de Diabetes por Faixa Etária')
st.plotly_chart(fig_faixa)

st.subheader("Comparação de Perfis Nutricionais")
fig_box = px.box(df, x='Perfil', y='Glucose', color='Outcome', title='Distribuição de Glicose por Perfil')
st.plotly_chart(fig_box)

st.sidebar.title("🔍 Filtros Interativos")
idade = st.sidebar.slider("Idade", int(df['Age'].min()), int(df['Age'].max()), (20, 60))
glicose = st.sidebar.slider("Glicose", int(df['Glucose'].min()), int(df['Glucose'].max()), (70, 150))

df_filtrado = df[(df['Age'].between(*idade)) & (df['Glucose'].between(*glicose))]
st.subheader("Pacientes Filtrados")
st.dataframe(df_filtrado)
