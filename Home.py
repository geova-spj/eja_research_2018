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
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#====================================================================================================
# CARREGANDO ARQUIVO
#====================================================================================================
data = pd.read_excel('datasets/base_eja_final.xlsx')

#====================================================================================================
# SIDEBAR
#====================================================================================================
st.set_page_config(page_title='Dossiê EJA 2018', layout="wide")

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
st.sidebar.markdown ('##### Data Analyst: Geová Silvério')

#====================================================================================================
# Boas Vindas
#====================================================================================================
st.title ('👋 Boas Vindas')

tab1, tab2, tab3 = st.tabs(['O Dossiê EJA', 'Contextualização da Pesquisa', 'Dados Gerais'])

with tab1:
    with st.container():
        st.markdown(
            '''
            Olá,

            Seja bem-vindo(a) a este dossiê sobre a Educação de Jovens e Adultos (EJA) na Região Metropolitana do Recife.
            Aqui você encontrará um raio X sobre essa modalidade de ensino no ano de 2018 a partir dos resultados de uma pesquisa
            conduzida junto a 514 estudantes matriculados em 25 escolas municipais e estaduais localizadas principalmente na cidade
            de Recife – PE e também nas cidades de Jaboatão dos Guararapes, Olinda, São Lourenço da Mata e Abreu e Lima.
            
            A visualização de dados aqui apresentada contempla 4 eixos analíticos:

            📊 **Perfil:** aqui se identifica os dados demográficos dos estudantes como o gênero, a idade, a cor, ocupação profissional,
            renda, estado civil além de informações mais gerais sobre a experiência de ser estudante da EJA;

            💪 **Aspectos motivacionais:** nesse eixo ilustra-se fatores os quais contribuem na motivação e desmotivação de se estudar
            na idade adulta segundo a percepção dos entrevistados bem como o que os levou de volta a sala de aula;

            📚 **Aspectos pedagógicos:** o que os estudantes acham da sala de aula? Dos seus colegas, professores, processos avaliativos?
            Quais as suas dificuldades de aprendizagem e que recursos e instrumentos estão a sua disposição na escola? As respostas a esse tipo de perguntas são tratadas nesse eixo;
            
            ⚠️ **Vulnerabilidade:** percepções sobre infraestrutura escolar e segurança, exposição a violência e drogas são temáticas
            tratadas aqui nessa sessão.
            
            De um modo geral, os dados poderão ser filtrados segundo alguns critérios (gênero, faixa etária e grupo racial) conforme a
            necessidade do usuário. Que este dossiê seja um instrumento de reflexão e fonte de inspiração para criação de outras e novas
            ferramentas diagnósticas da EJA de modo a subsidiar o planejamento de políticas públicas educacionais e auxiliar nos
            processos decisórios para melhorar esta modalidade de ensino. Caso queira trocar uma ideia sobre os dados dessa pesquisa
            e de como eles podem ser melhor utilizados sinta-se à vontade para entrar em contato comigo.
            
            Geová Silvério

            E-mail: geova.spj@gmail.com | Linked In: https://www.linkedin.com/in/geova-silverio/
            ''')

with tab2:
    with st.container():
        st.markdown(
            '''
            Durante meus anos de docência no Ensino Superior um dos desafios que tive foi ministrar a disciplina Ação Pedagógica na
            Educação de Jovens e Adultos para a licenciatura em pedagogia. A disciplina possuía horas teóricas e práticas – não sendo licenciado
            e também nunca tido trabalhado com o ensino de jovens e adultos do perfil da EJA me sentia desconfortável em sugerir trabalhos aos 
            meus estudantes que remetessem à metodologias e práticas de alfabetização e ensino com esse público.
            
            Foi desse desconforto que surgiu a ideia de ensinar a partir da ótica daquilo que sou realmente bom – pesquisa.
            Assim surgiu a pesquisa quantitativa na EJA, um projeto de ensino – aprendizagem a durar todo semestre letivo: na medida em
            que ministrava a teoria sobre a modalidade de ensino no Brasil também ensinava sobre práticas de pesquisa quanti: construção
            e aplicação de questionários, tabulação de dados e fundamentos de relatórios analíticos e construção de gráficos.

            O que apresento aqui, portanto, é o resultado de um projeto coletivo feito na parceria entre mim e meus alunos de pedagogia e destes
            com os estudantes da EJA e com os docentes e gestores das escolas participantes. É importante salientar que a pesquisa acabou por ter
            uma dimensão pedagógica na medida em que a aplicação do questionário construído por meus futuros pedagogos na época, implicava em uma
            troca, um diálogo com os estudantes da EJA, processo interativo cuja a vida e saberes prévios vinham à tona e se tornavam objetos
            pedagógicos tal como preconizaria Paulo Freire, grande nome da educação brasileira e de extrema importância na modalidade de ensino
            em questão.

            O ano de 2018 foi escolhido, pois em seu segundo semestre tive a oportunidade de lecionar a disciplina e aplicar o projeto de
            pesquisa em 5 turmas, o que permitiu a robustez de dados aqui analisados mediante a realização de 514 entrevistas.
            Dado o projeto ter finalidade pedagógica, ele não segue rigor estatístico em sua amostragem, contudo, os resultados aqui
            expostos em muito refletem as discussões tratadas pela literatura acadêmica sobre a EJA.
            '''
        )
    with st.container():
        st.markdown('#### Algumas fotos de processo de aplicação de questionário')

        image_path = 'images/fotos_eja.png'
        image = Image.open(image_path)
        st.image(image)
    
    with tab3:
        with st.container():
            st.markdown('#### A Educação de Jovens e Adultos')
            st.markdown('''
            A Educação de Jovens e Adultos é uma modalidade de ensino da Educação Básica destinada à pessoas maiores de 15 anos
            (nível fundamental) e maiores de 18 anos (nível médio) que nunca tiveram acesso à educação regular na idade apropriada ou mesmo
            tiveram seus estudos interrompidos ao longo de sua trajetória escolar. 
            ''')
                       
            st.write('Faça o download do questionário aplicado na pesquisa clicando no botão abaixo:')           
            with open('questionario.pdf', 'rb') as pdf_file:
                PDFbyte = pdf_file.read()
            quest = st.download_button(label='Questionário Aplicado',
                                       data=PDFbyte,
                                       file_name='questionario.pdf',
                                       mime='application/octet-stream')
            st.markdown('---')
        
        with st.container():
            col1,col2 = st.columns(2)
            with col1:
                estudantes = data.shape[0]
                st.metric('Estudantes entrevistados: ', estudantes)
            with col2:
                escolas = data['ESCOLA'].nunique()
                st.metric('Escolas pesquisadas: ', escolas)
        
        with st.container():
            st.markdown('#### Distribuição das redes e segmentos de ensino participantes da pesquisa')
            df1=data.loc[data['SEGMENTO'] == 'Fundamental',['REDE', 'SEGMENTO']].groupby('REDE').count().reset_index()
            df2=data.loc[data['SEGMENTO'] == 'Médio',['REDE', 'SEGMENTO']].groupby('REDE').count().reset_index()
            df3=df1.merge(df2, how='cross').drop(['REDE_y'], axis=1)
            df3.columns=['REDE','Ens. Fundamental','Ens. Médio']
            df3.iloc[1,2] = 0
            df3.iloc[2,2] = 0
            df3 = df3.sort_values('Ens. Fundamental', ascending=False)

            fig = go.Figure()
            fig.add_trace(go.Bar(y = df3['Ens. Fundamental'],x = df3['REDE'], textposition= 'inside',
                                        name = 'Ensino Fundamental', orientation = 'v', text =df3['Ens. Fundamental'],
                                        texttemplate='%{text}', hovertemplate ='Rede %{x}: %{y} estudantes'))
            fig.add_trace(go.Bar(y = df3['Ens. Médio'],x = df3['REDE'], textposition= 'inside',
                                        name = 'Ensino Médio', orientation = 'v', text =df3['Ens. Médio'],
                                        texttemplate='%{text}', hovertemplate ='Rede %{x}: %{y} estudantes'))
            fig.update_layout(template='plotly_white', barmode = 'stack', bargap = 0.2, bargroupgap = 0.2,
                            yaxis_title='Nº. de entrevistados')
            fig.data[0].marker.color = ('gold')
            fig.data[1].marker.color = ('royalblue')
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        
        with st.container():
            st.markdown('#### Escolas pesquisadas')

            # Criando dados para o mapa
            df1 = data.loc[:,['ESCOLA', 'Bairro']].groupby('ESCOLA').count().reset_index()
            df2 = data.loc[:, ['ESCOLA', 'Cidade', 'Bairro', 'REDE', 'SEGMENTO', 'lat', 'long']].drop_duplicates(subset= 'ESCOLA', keep = 'first').reset_index(drop=True)
            datamap = df2.merge(df1, on = 'ESCOLA').rename(columns={'Bairro_x': 'Bairro', 'Bairro_y': 'Qt.Entrevistas'})
            # Criando o mapa
            mapa = folium.Map(zoom_start=50)
            #Criando os clusters
            cluster = MarkerCluster().add_to(mapa)
            #Colocando os pinos
            icon = "fa-solid fa-graduation-cap"

            for index, location_info in datamap.iterrows():
                folium.Marker([location_info['lat'],       
                            location_info['long']],
                            icon = folium.Icon(color = 'orange', icon=icon, prefix='fa'),
                            popup = folium.Popup(f"""<h6> <b> {location_info['ESCOLA']} </b> </h6> <br>
                                                    <b>Cidade:</b> {location_info['Cidade']} <b>Bairro:</b> {location_info['Bairro']} <br>
                                                    <b>Rede:</b> {location_info['REDE']} <b>Segmento:</b> {location_info['SEGMENTO']} <br>
                                                    <b>Nº de Entrevistas:</b> {location_info['Qt.Entrevistas']}""",
                                                    max_width= len(f"{location_info['ESCOLA']}")*20)).add_to(cluster)
            # Exibindo o mapa
            folium_static(mapa, width = 1024, height = 600)

            df1 = datamap[['ESCOLA', 'Cidade', 'Bairro', 'REDE', 'SEGMENTO', 'Qt.Entrevistas']]
            st.dataframe(df1, use_container_width=True)