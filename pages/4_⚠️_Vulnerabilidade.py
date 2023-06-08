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

#====================================================================================
# CARREGANDO ARQUIVO E FAZENDO LIMPEZA
#====================================================================================================
data = pd.read_excel('datasets/base_eja_final.xlsx')

#====================================================================================================
# SIDEBAR
#====================================================================================================
st.set_page_config(page_title='⚠️ Vulnerabilidade', layout="wide")


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
st.title ('⚠️ Vulnerabilidade')
st.markdown('''---''')
              
with st.container():
    st.markdown('#### Avaliação da segurança da escola')
    seguranca = pd.DataFrame(data['SEGURANCA'].value_counts(normalize=True).mul(100).round(2).reset_index().rename(columns={'index':'Percepção de Segurança', 'SEGURANCA':'%'}))
    seguranca = seguranca.reset_index()
    seguranca.iloc[0,0] = 7
    seguranca.iloc[1,0] = 6
    seguranca.iloc[2,0] = 8
    seguranca.iloc[3,0] = 5
    seguranca.iloc[4,0] = 9
    fig = bar_graph (seguranca.sort_values('index'), 'Percepção de Segurança', '%', 40, 'v')
    st.plotly_chart(fig, use_container_width = True, theme='streamlit')
       
with st.container():
    st.markdown('#### Violência e drogas')
    aux = data[['VIOLENCIA','DROGA_CONSUMO', 'DROGA_COMPRA']]

    df1 = pd.DataFrame(aux[col].value_counts(normalize=True).mul(100).round(2) for col in aux.columns).reset_index()
    df1.iloc[0,0] = 'Foi alvo de alguma violência (furto, assalto, agressão, etc) aos arredores da escola no último ano?'
    df1.iloc[1,0] = 'Consumiu alguma droga ilícita no último ano?'
    df1.iloc[2,0] = 'No último ano, alguém lhe ofereceu ou vendeu alguma droga ilícita nos arredores ou na própria escola?'
    df1 = df1.sort_values('Sim', ascending = True)

    fig = go.Figure() # Creating instance of the figure
    # Adding NS/NR data to the figure
    fig.add_trace(go.Bar(x = df1['NS/NR'], y = df1['index'],name = 'NS/NR', orientation = 'h',
                            hovertemplate='%{y} : %{x:.2f}%'))
    # Adding Não data to the figure
    fig.add_trace(go.Bar(x = df1['Não'], y = df1['index'], textposition='inside', texttemplate='%{text:.2f}%', 
                            insidetextanchor='middle', name = 'Não', orientation = 'h', text = df1['Não'],
                            hovertemplate='%{y} : %{text:.2f}%'))
    # Adding Sim data to the figure
    fig.add_trace(go.Bar(x = df1['Sim'], y = df1['index'], textposition='inside', texttemplate='%{text:.2f}%', 
                            insidetextanchor='middle', name = 'Sim', orientation = 'h', text = df1['Sim'],
                            hovertemplate='%{y} : %{text:.2f}%'))
    fig.update_layout(template='plotly_white', barmode = 'stack', bargap = 0.2, bargroupgap = 0.0, xaxis_range=[0,100])
    fig.data[0].marker.color = ('darkviolet')
    fig.data[2].marker.color = ('royalblue')
    st.plotly_chart(fig, use_container_width = True, theme='streamlit')
with st.container(): 
    st.markdown('#### O que é mais urgente melhorar na escola?')
    df1 = pd.DataFrame(data['MELHORIA_ESC'].value_counts(normalize=True).mul(100).round(2)).reset_index()
    df1 = df1.reset_index()
    df1.iloc[5,0] = 9
    df1.iloc[2,0] = 8
    df1.iloc[4,0] = 7
    df1 = df1.sort_values('level_0', ascending=False).reset_index(drop=True)
    fig = bar_graph (df1, 'MELHORIA_ESC',  'index',  55, 'h')
    st.plotly_chart(fig, use_container_width = True, theme='streamlit')   