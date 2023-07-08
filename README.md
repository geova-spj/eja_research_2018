<p align="center">
  <img src= images/logo_eja_(2).png alt="Sublime's custom image" width=300)/>
</p>

# Contextualização
A Educação de Jovens e Adultos (EJA) é uma modalidade de ensino da Educação Básica destinada à pessoas maiores de 15 anos (nível fundamental) e maiores de 18 anos (nível médio) que nunca tiveram acesso à educação regular na idade apropriada ou mesmo tiveram seus estudos interrompidos ao longo de sua trajetória escolar.

O presente projeto demonstra por meio de um conjunto de dashboards os resultados de uma pesquisa realizada com 514 estudantes dessa modalidade de ensino no ano de 2018. O universo da pesquisa contempla 25 escolas da Região Metropolitana do Recife das redes municipal, estadual e privada e os estudantes entrevistados estavam tanto na EJA nível fundamental quanto na EJA nível médio.

**O objetivo maior da pesquisa era responder a seguinte pergunta: qual o perfil discente da Educação de Jovens e adultos?** O acesso aos resultados da pesquisa, ao questionário aplicado e a maiores detalhamentos do contexto em que ela se deu podem ser acompanhados pelo link: https://geova-spj-eja-research-2018.streamlit.app/

# Eixos Analíticos

Os resultados da pesquisa apresentadas foram analiticamente dividido em 4 categorias:

📊 **Perfil:** dados demográficos dos estudantes como o gênero, a idade, a cor, ocupação profissional, renda, estado civil além de informações mais gerais sobre a experiência de ser estudante da EJA.

💪 **Aspectos motivacionais:** dados os quais identifiquem os fatores a contribuir na motivação e desmotivação de se estar na sala de aula na idade adulta bem como o que levou a desistência da mesma no passado.

📚 **Aspectos pedagógicos:** dados que ilustram as percepções dos estudantes sobre a sala de aula - colegas, professores, processos avaliativos, dificuldades de aprendizagem, etc. Também investiga-se os recursos pedagógicos a disposição na escola e sua frequência de uso.

⚠️ **Vulnerabilidade:** temas como qualidade da infraestrutura escolar, segurança, exposição a violência e drogas são abarcados nos dados dessa categoria.

# Ferramentas e processos

1. Os questionários de pesquisas foram aplicados tradicionalmente em versão impressa, posteriormente eles foram tabulados, os dados tratados e processados em uma planilha de **excel**.
2. A planilha de excel passou por novos tratamentos e processamento de dados por meio da **linguagem de programação Python**. Usou-se o **Jupyter Notebook** para testes, análises e visualizações, auxiliaram nesse processo as bibliotecas **Pandas, Numpy, Matplotib, Plotly e Folium**.
3. Definidas as análises e visualizações a comporem o produto final: dashboard analítico com os resultados de pesquisa - usou-se o **VS Code** para criação dos scripts Python e o framework **Streamlit** para produção do dash e publicação em sua cloud.

**Obs:** o painel analítico apresenta a possibilidade de realização de filtros nos eixos citados acima. Assim, pode-se obter recortes etários, de gênero e raciais nos dados da pesquisa.

# Top 3 Insights de dados

1. O perfil discente da EJA é em sua grande maioria de jovens entre 15 a 24 anos oriundos das classes mais baixas, pretos e pardos, desempregados ou na informalidade com renda familiar de até 1 salário mínimo que já perderam oportunidades pela falta de estudos e com considerável risco de novamente abandonar a escola (42.6% já pensou em desistir).

<p align="center">
  <img src= images/general_eja.png alt="Sublime's custom image"/>
</p>

2. O trabalho é um elemento significativo na trajetória dos estudantes pesquisados: figura em primeiro lugar como o principal motivo de abandono dos estudos (para 23% dos jovens) e também como uma das principais dificuldades para se permanecer na sala de aula . Ao mesmo tempo também é um grande elemento motivador na retoma dos estudos.

<p align="center">
  <img src= images/motivacional_eja.png alt="Sublime's custom image"/>
</p>

3. A cultura escolar de um modo geral é bem avaliada pelos estudantes - aulas, professores, processos avaliativos, etc, mesmo que ainda limitada ao uso de recursos pedagógicos tradicionais (quadro e giz/piloto, livro didático, trabalhos em grupo e rodas de diálogos). O que pesa na qualidade de ensino é carência de infraestrutura escolar sendo esta o mais urgente a se melhorar na escola para 46,5% dos estudantes.

<p align="center">
  <img src= images/melhora_eja.png alt="Sublime's custom image"/>
</p>

# Conclusão

O objetivo do projeto foi a criação de um painel analítico o qual resumisse os resultados de uma pesquisa a qual buscava compreender o perfil dos estudantes da modalidade de ensino Educação de Jovens e Adultos na Região Metropolitana do Recife. Os dados são de 2018, agregam em 4 eixos analíticos - perfil, aspectos motivacionais, aspectos pedagógicos e vulnerabilidade - a percepção de 514 estudantes da EJA fundamental e médio de 25 escolas pertencentes as redes municipal, estadual e privada. 

A partir desses dados é possível ter mais linhas investigativas das necessidades educacionais dos estudantes e das carências pedagógicas da modalidade de ensino de modo a orientar estratégias mais assertivas em pró do melhor desenvolvimento da EJA como política pública e direito à educação de todos e todas.

# Próximos passos

1. Adotar práticas/técnicas de *encoding* no dataset de trabalho de modo a melhorar o processo de tratamento e análise de dados;
2. Explorar ferramentas de visualização de dados mais adequadas para produção do painel de modo também a lhe conferir uma identidade estética mais uniforme;
3. Aplicar testes estatísticos em algumas variáveis, a exemplo de correlação, de modo a aprofundar as possibilidades de análise.

