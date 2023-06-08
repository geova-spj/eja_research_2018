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
# CARREGANDO ARQUIVO E FAZENDO LIMPEZA
#====================================================================================================
data = pd.read_excel('datasets/base_eja_final.xlsx')

#====================================================================================================
# SIDEBAR
#====================================================================================================
st.set_page_config(page_title='📚 Aspectos Pedagógicos', layout="wide")

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
# Aspectos pedagógicos
#====================================================================================================
st.title('📚 Aspectos Pedagógicos')
st.markdown('''---''')

tab1, tab2, tab3 = st.tabs(['Percepções escolares', 'Dificuldades de aprendizagem', 'Recursos pedagógicos'])

with tab1:
    with st.container():
        col1,col2,col3 = st.columns(3)

        with col1:
            st.markdown('##### Percepção das aulas')
            aula = pd.DataFrame(data['AV_AULA'].value_counts(normalize=True).mul(100).round(2).reset_index().rename(columns={'index':'Percepção das aulas', 'AV_AULA':'%'}))
            aula.iloc[1,0] = 'Cansativas e repetitivas'
            fig = px.pie(aula, names='Percepção das aulas', values='%', color_discrete_sequence=["RoyalBlue", "red", "lavender"])
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        with col2:
            st.markdown('##### Avaliação dos professores')
            av_prof = pd.DataFrame(data['AV_PROF'].value_counts(normalize=True).mul(100).round(2).reset_index().rename(columns={'index':'Avaliação dos Professores', 'AV_PROF':'%'}))
            fig = px.pie(av_prof, names = 'Avaliação dos Professores', values='%', hole=0.5,
                         color_discrete_sequence=["RoyalBlue", "PaleTurquoise", "LightGreen", "lavender", "orange", "red"])
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        with col3:
            st.markdown('##### Percepção do processo avaliativo')
            avaliacao = pd.DataFrame(data['AV_AVALIACAO'].value_counts(normalize=True).mul(100).round(2).reset_index().rename(columns={'index': 'Percepção', 'AV_AVALIACAO':'%'}))
            fig = px.pie(avaliacao, names='Percepção', values='%', color_discrete_sequence=["RoyalBlue", "lavender", "red"])
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    with st.container():
        col1,col2 = st.columns(2)

        with col1:
            st.markdown('#### O quão útil vem sendo os aprendizados escolares?')
            utilidade = pd.DataFrame(data['UTILIDADE'].value_counts(normalize=True).mul(100).round(2).reset_index())
            utilidade = utilidade.reset_index()
            utilidade.iloc[3,0] = 5
            fig = bar_graph(utilidade.sort_values('level_0'), 'index', 'UTILIDADE', 60, 'v')
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        with col2:
            st.markdown('#### Avaliação dos colegas')
            st.write('')
            colegas = pd.DataFrame(data['AV_COLEGAS'].value_counts(normalize=True).mul(100).round(2).reset_index().rename(columns={'index':'Percepção', 'AV_COLEGAS':'%'}))
            colegas = colegas.reset_index()
            colegas.iloc[2, 0] = 5
            fig = bar_graph(colegas.sort_values('index'), 'Percepção', '%', 85, 'v')
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
with tab2:
    with st.container():
        col1,col2= st.columns(2)

        with col1:
            st.markdown('### Habilidade a qual sente maior dificuldade')
            habilidade = pd.DataFrame(data['HABILIDADES'].value_counts(normalize=True).mul(100).round(2).reset_index().rename(columns={'index':'Habilidade', 'HABILIDADES':'%'}))
            habilidade = habilidade.reset_index()
            habilidade.iloc[4,0] = 5
            habilidade.iloc[2,0] = 4
            fig = bar_graph (habilidade.sort_values('index'), 'Habilidade', '%', 35, 'v')
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        with col2:
            st.markdown('### Horas dedicadas ao estudo')
            sem_tempo = data.loc[data['HORAS_EST']==0.0,'HORAS_EST'].count()
            sem_tempo_perc = round((sem_tempo/data['HORAS_EST'].shape[0])*100,2)

            nr = data['HORAS_EST'].isnull().sum()
            nr_perc = round((nr/data['HORAS_EST'].shape[0])*100,2)
            st.write (f'Não tem tempo para estudar fora da escola: {sem_tempo} estudantes ({sem_tempo_perc}%)')
            st.write (f'Não respondentes: {nr} ({nr_perc}%)')
            
            horas = pd.DataFrame(data.loc[(data['HORAS_EST'] != 0) & (data['HORAS_EST'] != 99), 'HORAS_EST'])
            horas.columns=['Horas de Estudo']
            fig = px.histogram(horas, x='Horas de Estudo', color_discrete_sequence=['LightSalmon'])
            fig.update_layout(template='plotly_white', bargap = 0.0, bargroupgap = 0.0, xaxis_range=[0,15],
                              yaxis_title= 'Quantidade de Estudante', showlegend=False, title_text='Histograma', title_x=0.5,
                              xaxis= dict(tickvals = list (range(1,16)),
                                          ticktext = list (range(1,16)),
                                          title = 'Horas de Estudo', title_font_size = 14, showgrid=False))
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        
    with st.container():
        st.markdown('### Dificuldades em português e matemática')
        port = pd.DataFrame(data['PORTUGUES'].value_counts(normalize=True).mul(100).round(2).reset_index())
        mat = pd.DataFrame(data['MATEMATICA'].value_counts(normalize=True).mul(100).round(2).reset_index())
        df1 = port.merge(mat, how='inner')
        df1 = df1.reset_index()
        df1.iloc[2,0]=0
        df1.iloc[0,0]=1
        df1.iloc[1,0]=2
        df1 = df1.sort_values('level_0', ascending = False)
        df1.columns=['level_0','Percepção', '% Português', '% Matemática']

        x_1 = df1['% Português']
        x_2 = df1['% Matemática']
        y = df1['Percepção']
           
        fig = go.Figure() # Creating instance of the figure
        go_bar_graph(x_2, y, 'Matemática', 'h')  # Adding Mat data to the figure
        go_bar_graph(x_1, y, 'Português', 'h') # Adding Port data to the figure
        # Updating the layout for our graph
        fig.update_layout(template='plotly_white', barmode = 'group', bargap = 0.25, bargroupgap = 0.0, xaxis_range=[0,50], xaxis_title=None)
        fig.update_xaxes(showgrid=False)
        fig.data[0].marker.color = ('yellowgreen')
        fig.data[1].marker.color = ('royalblue')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    with st.container():
        st.markdown('### Dificuldades em recursos tecnológicos')
        aux=data[['CELULAR', 'COMPUTADOR', 'CAIXA ELETRONICO']]
        df1 = pd.DataFrame(aux[col].value_counts(normalize=True).mul(100) for col in aux.columns).reset_index()

        fig = go.Figure() # Creating instance of the figure
        go_bar_graph (df1['index'], df1['NS/NR'], 'NS/NR', 'v')# Adding NS/NR data to the figure
        go_bar_graph (df1['index'], df1['Nenhuma Dificuldade'], 'Nenhuma Dificuldade', 'v') # Adding Nenhuma Dificuldade data to the figure
        go_bar_graph (df1['index'], df1['Pouca Dificuldade'], 'Pouca Dificuldade', 'v') # Adding Pouca Dificuldade data to the figure
        go_bar_graph (df1['index'], df1['Dificuldade Razoável'], 'Dificuldade Razoável', 'v')# Adding Dificuldade Razoável data to the figure
        go_bar_graph (df1['index'], df1['Muita Dificuldade'],'Muita Dificuldade', 'v') # Adding Muita Dificuldade data to the figure
        # Updating the layout for our graph
        fig.update_layout(template='plotly_white', barmode = 'stack', bargap = 0.2, bargroupgap = 0.2, yaxis_range=[0,100])
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
with tab3:
    with st.container():
        st.markdown('### Recursos pedagógicos usados em sala de aula: frequência de uso')
        aux = data[['PILOTO', 'DEBATE', 'EQUIPE', 'SLIDE', 'MUSICA','VIDEO', 'LUDICO', 'LIVRO', 'JORNAL', 'BIBLIOTECA', 'LAB_INFO','EXTERNO']]

        df1 = pd.DataFrame(aux[col].value_counts(normalize=True).mul(100) for col in aux.columns).reset_index()
        df2 = pd.DataFrame((aux.isna().sum()/514)*100).reset_index()
        df2.columns=['index', 'NS/NR']
        df1 = df1.merge(df2, how='inner')

        df1.iloc[0,0] = 'Quadro e Giz/Piloto'
        df1.iloc[1,0] = 'Rodas de diálogo / Debates'
        df1.iloc[2,0] = 'Trabalhos/projetos em grupo'
        df1.iloc[3,0] = 'Data Show (Slides)'
        df1.iloc[4,0] = 'Música/Instrumentos Musicais'
        df1.iloc[5,0] = 'Audiovisual: filmes, vídeos, etc'
        df1.iloc[6,0] = 'Atividades lúdicas (jogos, encenações, etc) e esportivas'
        df1.iloc[7,0] = 'Livro didático'
        df1.iloc[8,0] = 'Revistas, Jornais, Panfletos'
        df1.iloc[9,0] = 'Visitas à biblioteca'
        df1.iloc[10,0] = 'Visitas ao laboratório de informática'
        df1.iloc[11,0] = 'Atividades externas (museus, teatro, etc)'

        df1 = df1.sort_values('Sempre', ascending = True)
        fig = go.Figure() # Creating instance of the figure
        horizontal_stack_bar(df1['NS/NR'], df1['index'], 'NS/NR') # Adding NS/NR data to the figure
        # Adding Nunca data to the figure
        fig.add_trace(go.Bar(y = df1['index'], x = df1['Nunca'], textposition= 'inside', texttemplate='%{text:.2f}%', 
                                insidetextanchor='middle', name = 'Nunca', orientation = 'h', text = df1['Nunca'],
                                hovertemplate='%{y} : %{text:.2f}%'))
        horizontal_stack_bar(df1['Raramente'], df1['index'], 'Raramente') # Adding Raramente data to the figure
        horizontal_stack_bar(df1['De vez em quando'], df1['index'], 'De vez em quando') # Adding de vez em quando data to the figure
        horizontal_stack_bar(df1['Sempre'], df1['index'], 'Sempre') # Adding sempre data to the figure
        # Updating the layout for our graph
        fig.update_layout(template='plotly_white', barmode = 'stack', bargap = 0.2, bargroupgap = 0.0, xaxis_range=[0,100])
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')