#====================================================================================================
# BIBLIOTECAS
#====================================================================================================
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

#====================================================================================================
# FUNÇÕES
#====================================================================================================
def bar_graph (df, x, y, max_range, direction):   
    if direction == 'h': 
        fig = px.bar(df, x=x, y=y, template='plotly_white', text=x)
        fig.update_layout(yaxis_title=None, xaxis_title=None, xaxis_range=[0,max_range])
        fig.update_xaxes(showgrid=False)
    else:
        fig = px.bar(df, x=x, y=y, template='plotly_white', text=y)
        fig.update_layout(yaxis_title=None, xaxis_title=None, yaxis_range=[0,max_range])
        fig.update_yaxes(showgrid=False)
    fig.update_traces(textangle=0, texttemplate='%{text:.2f}%', textposition='outside', marker_color='LightSalmon')
    return fig

def go_bar_graph(x, y, nome, orientation):
    if orientation == 'h':
        fig.add_trace(go.Bar(y = y,x = x, textposition= 'outside',
                             name = nome, orientation = orientation, text =x, texttemplate='%{text:.2f}%',
                             hovertemplate ='%{y}: %{x}%'))
    else:
        fig.add_trace(go.Bar(y = y,x = x, textposition= 'inside',
                             name = nome, orientation = 'v', text =y, texttemplate='%{text:.2f}%',
                             hovertemplate ='%{x}: %{y}%'))
    return fig

def horizontal_stack_bar(x, y, name):

    fig.add_trace(go.Bar(y = y, x = x, textposition= 'inside', #texttemplate='%{text:.2f}%',
                         name = name, orientation = 'h', text = None, hovertemplate='%{y} : %{x:.2f}%'))
    
    return fig

#====================================================================================================
# CARREGANDO ARQUIVO
#====================================================================================================
data = pd.read_excel('datasets/base_eja_final.xlsx')


#====================================================================================================
# SIDEBAR
#====================================================================================================
st.set_page_config(page_title='💪 Aspectos motivacionais', layout="wide")

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("<h1 style='text-align: center; color: black;'> DOSSIÊ </h1>", unsafe_allow_html=True) 
image_path = 'images/logo_eja_(1).png'
image = Image.open(image_path)
st.sidebar.image(image)
st.sidebar.markdown("<h3 style='text-align: center; color: black;'> 2018 </h3>", unsafe_allow_html=True)
st.sidebar.markdown('''---''')


#==============================FILTROS====================================

# Gênero - Multiselect
gender_options = st.sidebar.multiselect('Selecione o gênero:',
                                        ['Masculino','Feminino'],
                                        default = ['Masculino','Feminino'])

# Idade - Slider
idade_slider = st.sidebar.slider ('Selecione o intervalo etário:',
                                  value = [int(data['IDADE'].min()), int(data['IDADE'].max())],
                                  min_value = int(data['IDADE'].min()),
                                  max_value = int(data['IDADE'].max()))

# Cor - Select box
cor_option = st.sidebar.multiselect('Escolha o grupo racial:',
                                    list(data['COR'].unique()),
                                    default= list(data['COR'].unique()))


st.sidebar.markdown('''---''')
st.sidebar.markdown ('##### Data Analyst: Geová Silvério')

#==============================HABILITAÇÃO DOS FILTROS====================================
#Filtro de gênero
linhas_selecionadas = data['GENERO'].isin(gender_options)
data = data.loc[linhas_selecionadas,:]

#Filto de idade
linhas_selecionadas = (data['IDADE'] >= idade_slider[0]) & (data['IDADE'] <= idade_slider[1])
data = data.loc[linhas_selecionadas, :]

#Filtro Racial
linhas_selecionadas = data['COR'].isin(cor_option)
data = data.loc[linhas_selecionadas, :]

#====================================================================================================
# Aspectos motivacionais
#====================================================================================================
st.title ('💪 Aspectos Motivacionais')
st.markdown('''---''')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Principal motivo de interrupção dos estudos')
        parada= pd.DataFrame(data['PARADA'].value_counts(normalize= True).mul(100).round(2)).reset_index()
        parada.columns=['Interrupção dos estudos', '%']
        parada = parada.reset_index()
        parada['index'][4] = 9
        parada['index'][5] = 10

        nr_percent = parada.iloc[5,2]
        parada = parada.sort_values('index', ascending = False).reset_index(drop = True).loc[1:9, ['Interrupção dos estudos', '%']]

        st.write(f'Percentual de não respondentes: {nr_percent}%')

        fig = bar_graph(parada, '%', 'Interrupção dos estudos', 30, 'h')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    with col2:
        st.markdown('#### Como ficou sabendo da Eja?')
        st.write('')
        conhecimento = (pd.DataFrame(data['CONHECIMENTO'].value_counts(normalize= True).mul(100).round(2)).reset_index()
                          .rename(columns={'index':'Como ficou sabendo da EJA?','CONHECIMENTO':'%'}).reset_index())
        conhecimento['index'][2] = 5
        fig = bar_graph(conhecimento.sort_values('index', ascending = True), 'Como ficou sabendo da EJA?', '%', 55, 'v')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
               
with st.container():
    col1,col2= st.columns(2)

    with col1:
        st.markdown('#### Principais motivos de retomada dos estudos')
        st.markdown('###### Resposta múltipla x3')
        
        # Separação das perguntas
        df1 = data.loc[:, 'RETOMADA _1']
        df2 = data.loc[:, 'RETOMADA _2']
        df3 = data.loc[:, 'RETOMADA _3']
        # Concatenação das respostas - Soma do número de respostas obtidas
        df_4 = pd.DataFrame(pd.concat([df1, df2, df3]).dropna().value_counts()).reset_index()
        df_4.columns=['pergunta','total']
        tot_resp = df_4['total'].sum()
        # Concatenação das respostas - Tratando e ordenando o percentual de não respondentes
        df_aux = pd.DataFrame(pd.concat([df1, df2, df3]).dropna().value_counts(normalize=True).mul(100).round(2)).reset_index()
        df_aux.columns=['Motivos de retomada', '%']
        df_aux = df_aux.reset_index()
        df_aux['index'][6] = 10
        df_aux['index'][8] = 11
        nr_percent = df_aux.iloc[8,2]
        # Dataframe final para confecção do gráfico
        st.write(f'Total de respostas obtidas: {tot_resp}   |   Percentual de não respondentes: {nr_percent}%')
        df_aux =df_aux.sort_values('index', ascending = False).reset_index(drop = True).loc[1:11, ['Motivos de retomada', '%']]
        fig = bar_graph(df_aux, '%', 'Motivos de retomada', 35, 'h')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        
    with col2:
        st.markdown('#### Principais dificuldades para estudar')
        st.markdown('###### Resposta múltipla x3')        
        # Separação das perguntas
        df1 = data.loc[:, 'DIFICULDADE_1']
        df2 = data.loc[:, 'DIFICULDADE_2']
        df3 = data.loc[:, 'DIFICULDADE_3']
        # Concatenação das respostas - Soma do número de respostas obtidas
        df_4 = pd.DataFrame(pd.concat([df1, df2, df3]).dropna().value_counts()).reset_index()
        df_4.columns=['pergunta','total']
        tot_resp = df_4['total'].sum()
        # Concatenação das respostas - Tratando e ordenando o percentual de não respondentes
        df_aux = pd.DataFrame(pd.concat([df1, df2, df3]).dropna().value_counts(normalize=True).mul(100).round(2)).reset_index()
        df_aux.columns=['Dificuldades de se permancer estudando', '%']
        df_aux = df_aux.reset_index()
        df_aux['index'][8] = 13
        df_aux['index'][3] = 14
        df_aux['index'][9] = 15
        nr_percent = df_aux.iloc[9,2]
        # Dataframe final para confecção do gráfico
        df_aux =df_aux.sort_values('index', ascending = False).reset_index(drop = True).loc[1:15, ['Dificuldades de se permancer estudando', '%']]
        # Gráfico
        st.write(f'Total de respostas obtidas: {tot_resp}  |  Percentual de não respondentes: {nr_percent}%')
        fig = bar_graph(df_aux, '%', 'Dificuldades de se permancer estudando', 25, 'h')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')

with st.container():    
    col1,col2= st.columns(2)

    with col1:
        st.markdown('##### O trabalho incentiva ou dá condições de continuar estudando?')
        trabalho = pd.DataFrame(data['TRABALHO'].value_counts(normalize= True).mul(100).round(2)).reset_index().rename(columns={'index':'O trabalho incentiva ou dá condições para continuar estudando?','TRABALHO':'%'})
        fig = bar_graph(trabalho, 'O trabalho incentiva ou dá condições para continuar estudando?', '%', 55, 'v')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    with col2:
        st.markdown('##### Frequencia de ida as aulas')
        frequencia = (pd.DataFrame(data['FREQUENCIA'].value_counts(normalize= True).mul(100).round(2)).reset_index()
                        .rename(columns={'index':'Frequencia de ida as aulas','FREQUENCIA':'%'}).sort_values('%', ascending = True))
        fig = bar_graph(frequencia, 'Frequencia de ida as aulas', '%', 100, 'v')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')