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
# CARREGANDO ARQUIVO E FAZENDO LIMPEZA
#====================================================================================================
data = pd.read_excel('datasets/base_eja_final.xlsx')

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

#====================================================================================================
# SIDEBAR
#====================================================================================================
st.set_page_config(page_title='📊 Perfil Discente', layout="wide")

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

#==============================HABILIDADE FILTROS====================================
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
# Pefil
#====================================================================================================
st.title ('📊 Perfil Discente')
st.markdown('''---''')

with st.container():
    col1,col2= st.columns(2)

    with col1:
        st.markdown('### Pirâmide Etária')
        #---------------------------------------------------AGRUPAMENTO POR FAIXA ETÁRIA----------------------------------------------
        data['faixa_etaria'] = (data.loc[:, 'IDADE'].apply(lambda x:'15 - 17 anos' if x <= 17 else
                                                                    '18 - 24 anos' if x <= 24 else 
                                                                    '25 - 31 anos' if x <= 31 else
                                                                    '32 - 40 anos' if x <= 40 else  
                                                                    '41 - 50 anos' if x <= 50 else 
                                                                    '51 - 60 anos' if x <= 60 else '60+'))
        mas = data.loc[data['GENERO'] == 'Masculino', ['faixa_etaria', 'GENERO']].groupby('faixa_etaria').count().reset_index()
        fem = data.loc[data['GENERO'] == 'Feminino', ['faixa_etaria', 'GENERO']].groupby('faixa_etaria').count().reset_index()
        df1 = pd.merge(mas, fem, how='inner', on='faixa_etaria')
        df1['mas'] = df1['GENERO_x'].apply(lambda x: round((x/258)*100,2))
        df1['fem'] = df1['GENERO_y'].apply(lambda x: round((x/256)*100,2))
        #---------------------------------------------------------------GRÁFICO-----------------------------------------------------
        men_bins = df1['mas']*-1
        women_bins = df1['fem']
        y = df1['faixa_etaria']
        # Creating instance of the figure
        fig = go.Figure()
        # Adding Male data to the figure
        fig.add_trace(go.Bar(y= y, x = men_bins, 
                                name = 'Masculino', textposition= 'outside', texttemplate='%{text:.2f}%',
                                orientation = 'h', text = men_bins*-1, hovertemplate='%{y} : %{text}%'))
        # Adding Female data to the figure
        fig.add_trace(go.Bar(y = y, x = women_bins, textposition= 'outside', texttemplate='%{text:.2f}%',
                                name = 'Feminino', orientation = 'h', text = women_bins, hovertemplate='%{y} : %{text}%'))   
        # Updating the layout for our graph
        fig.update_layout(template='plotly_white', barmode = 'relative', bargap = 0.0, bargroupgap = 0.0, xaxis_range=[-75,75],
                            xaxis= dict(tickvals = [-60, -40, -20, 0, 20, 40, 60],
                                        ticktext = ['60','40','20','0','20','40','60'],
                                        title = '% de estudantes', title_font_size = 12, showgrid=False))
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        #---------------------------------------------------------------DATAFRAME-----------------------------------------------------
        homens =  data.loc[data['GENERO'] == 'Masculino', ['GENERO']].count().astype(int)[0]
        idade_h= data.loc[data['GENERO'] == 'Masculino', ['IDADE']].mean().round(0)
        perc_h = round((homens/514)*100,2)
        mulheres = data.loc[data['GENERO'] == 'Feminino', ['GENERO']].count().astype(int)[0]
        idade_m= data.loc[data['GENERO'] == 'Feminino', ['IDADE']].mean().round(0)
        perc_m = round((mulheres/514)*100,2)    
        idade_media = data['IDADE'].mean().round(0)
        table = pd.DataFrame({'Nº abs': [homens, mulheres, homens + mulheres],
                              '%': [perc_h, perc_m, perc_h + perc_m],
                              'Idade Média': [idade_h[0],idade_m[0], idade_media]}).T.reset_index()
        table.columns=['Dados', 'Masculino', 'Feminino', 'Geral']
        st.dataframe(table, width=500)
    with col2:
        st.markdown('### Cor')
        for i in range(5):
            st.header('')
        aux = pd.DataFrame(data['COR'].value_counts(normalize=True)).mul(100).reset_index()
        aux.columns=['Cor','%']
        aux = aux.sort_values('%')
        fig = px.pie(aux, values = '%', names='Cor', hole = .5, color='Cor',
                     color_discrete_map={'Pardo (a)':'sienna',
                                         'Branco (a)':'gainsboro',
                                         'Preto (a)':'peru',
                                         'NS/NR':'thistle',
                                         'Indígena':'darkseagreen'})
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
with st.container():
#---------------------------------------------------------------DATAFRAME-----------------------------------------------------    
    aux = data[['DISCRIMINACAO', 'OPORTUNIDADE', 'CONFIANCA', 'DESISTIR', 'FAMILIA']]
    aux.columns=['Já foi ou se sentiu discriminado por ser estudante de EJA?',
                 'Já perdeu oportunidades por não ter os estudos completos?',
                 'Se sente confiante/preparado para ingressar ou permanecer no mercado?',
                 'Já pensou em desistir?',
                 'Tem apoio dos familiares para continuar estudando?']
    df1 = pd.DataFrame(aux[col].value_counts(normalize=True).mul(100) for col in aux.columns)
    df1 = df1.sort_values('Sim', ascending =  True).reset_index()
#---------------------------------------------------------------GRÁFICO-----------------------------------------------------
    # Creating instance of the figure
    fig = go.Figure()
    # Adding Não data to the figure
    fig.add_trace(go.Bar(y = df1['index'], x = df1['Não'], textposition= 'inside', insidetextanchor = 'middle', texttemplate='%{text:.2f}%',
                        name = 'Não', orientation = 'h', text = df1['Não'], hovertemplate='%{y} : %{text:.2f}%'))
    # Adding Sim data to the figure
    fig.add_trace(go.Bar(y= df1['index'], x = df1['Sim'],
                        name = 'Sim', textposition= 'inside', insidetextanchor = 'middle', texttemplate='%{text:.2f}%',
                        orientation = 'h', text = df1['Sim'], hovertemplate='%{y} : %{text:.2f}%'))
    # Updating the layout for our graph
    fig.update_layout(template='plotly_white', barmode = 'stack', bargap = 0.3, bargroupgap = 0.0)
    fig.data[0].marker.color = ('crimson')
    fig.data[1].marker.color = ('cornflowerblue')
    st.plotly_chart(fig, use_container_width = True, theme='streamlit')
with st.container():    
    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown('### Estado Civil')
        est_civil = pd.DataFrame(data['EST_CIVIL'].value_counts(normalize= True).mul(100).round(2)).reset_index()
        est_civil.columns=['Estado Civil', '%']
        fig = bar_graph (est_civil, 'Estado Civil', '%', 75, 'v')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    with col2:
        st.markdown('### Renda')
        renda = pd.DataFrame(data['RENDA'].value_counts(normalize= True).mul(100).round(2)).reset_index()
        renda.columns=['Renda', '%']
        renda = renda.reset_index()
        renda['index'][2] = 5

        nr_percent = renda.iloc[2,2]
        renda = renda.sort_values('index', ascending = False).reset_index(drop = True).loc[1:5, ['Renda', '%']]
        st.write(f'Percentual de não respondentes: {nr_percent}%')
        
        fig = px.funnel(renda, x='%', y='Renda', color='%', template='plotly_white', text='%')
        fig.update_layout(showlegend=False, yaxis_title=None)
        fig.update_traces(textangle=0, texttemplate='%{text:.2f}%', marker_color='LightSalmon')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit') 
    with col3:
        st.markdown('### Ocupação')
        ocup = pd.DataFrame(data['OCUPACAO'].value_counts(normalize= True).mul(100).round(2)).reset_index()
        ocup.columns=['Ocupação', '%']
        ocup = ocup.reset_index()
        ocup['index'][3] = 7

        nr_percent = ocup.iloc[3,2]
        ocup =ocup.sort_values('index', ascending = False).reset_index(drop = True).loc[1:7, ['Ocupação', '%']]
        st.write(f'Percentual de não respondentes: {nr_percent}%')
        
        fig = bar_graph (ocup, '%', 'Ocupação', 45, 'h')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')