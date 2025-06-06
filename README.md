# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>


# Projeto: fiap_gs1

## Atividade em Grupo: FIAP - 1TIAOB - 2025/1 - Fase4 GS1

## 👨‍🎓 Integrantes: 
- <a href="">Alice C. M. Assis - RM 566233</a>
- <a href="">Leonardo S. Souza - RM 563928</a>
- <a href="">Lucas B. Francelino - RM 561409</a> 
- <a href="">Pedro L. T. Silva - RM 561644</a> 
- <a href="">Vitor A. Bezerra - RM 563001</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="proflucas.moreira@fiap.com.br">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="profandre.chiovato@fiap.com.br">André Godoi Chiovato</a>


## 📜 Descrição

# Projeto: Agente de IA para Comunicação Emergencial em Desastres

## Introdução

Nos últimos anos, eventos naturais extremos — como enchentes, deslizamentos, queimadas e ondas de calor — têm ocorrido com maior frequência e intensidade. Em meio ao caos, a **comunicação emergencial** se revela um dos elementos mais frágeis e, ao mesmo tempo, mais decisivos na preservação de vidas.

Órgãos como a Defesa Civil e o Corpo de Bombeiros enfrentam limitações logísticas, escassez de recursos e falta de pessoal. Em muitas situações, **uma mensagem clara e bem distribuída pode evitar tragédias maiores**, permitindo evacuações preventivas e coordenadas antes que a situação se agrave.

Tendo em visto isto, o grupo ponderou que antes de desenvolver soluções complexas de resgate e contenção, é essencial **melhorar a comunicação** com a população em risco. A ideia é criar um agente de inteligência artificial que possa gerar automaticamente conteúdos informativos e alertas, otimizando o tempo e os recursos das equipes de emergência.

## Problema

O maior problema encontrado pelo grupo é desenvolver uma comunicação eficiente e certeira, capaz de competir com a velocidade das redes sociais e a proliferação de informações falsas. Além disso, se a informação não for entregue de maneira atrativa, muito possívelmente a população nem mesmo lerá a comunicação oficial.

Em situações de crise, a população precisa de **orientações claras e imediatas** sobre como agir, onde se abrigar e quais medidas tomar para garantir sua segurança.

Posto isso, é importante que essa comunicação seja **visualmente impactante**, utilizando imagens que transmitam a urgência da situação e as instruções necessárias de forma rápida e compreensível, uma vez que muitas pessoas podem não ter acesso a informações escritas ou podem ter dificuldades de leitura sob estresse.

## MVP da Solução Proposta

Desenvolvemos um **Agente de Inteligência Artificial** voltado à **criação automática de posts e imagens informativas** para uso imediato em canais de comunicação da Defesa Civil e Bombeiros.

Essa solução atua como um suporte operacional, gerando conteúdos em tempo real com base em dados reais sobre desastres. Seu objetivo é **aumentar a velocidade e a eficácia na divulgação de alertas e instruções** à população em risco.

O agente é capaz de:
- **Gerar posts informativos e de alertas** com base em dados coletados por sensores ambientais e previsões meteorológicas;
- **Criar imagens ilustrativas** para aumentar o impacto visual das comunicações;
- **Obter previsões meteorológicas** utilizando APIs externas;
- **Prever enchentes** com base em dados históricos, condições atuais e leituras de sensores, utilizando um modelo de IA treinado pelo grupo;

## Possíveis Upgrades para o Futuro

- **Geração de audio e video**: Expansão do agente para criar conteúdos multimídia, como vídeos curtos e mensagens de voz, que podem ser mais eficazes em alcançar públicos diversos, muito embora o grupo tenha utilizado o a IA VEO3 para fazer videos da aparesentação, devido a limitações orçamentárias, a solução inicial se concentra em posts estáticos e imagens.
- **Integração com sistemas de alerta**: Conectar o agente a plataformas de alerta em massa, como sirenes e aplicativos de mensagens, para garantir que as informações cheguem rapidamente a todos os cidadãos.
- **Análise de sentimento e feedback**: Implementar mecanismos para analisar o sentimento da população em relação às comunicações recebidas, permitindo ajustes dinâmicos nas mensagens e estratégias de engajamento.
- **Melhoria do modelo de previsão de enchentes**: Aperfeiçoar o modelo de previsão de enchentes com dados adicionais e feedback das equipes de emergência, aumentando a precisão das previsões.
- **Análise de dados históricos**: Ampliar a capacidade do agente de analisar dados históricos de desastres para prever padrões e melhorar a eficácia das comunicações futuras.
- **Expansão para outras áreas**: Adaptar o agente para atuar em outras situações de emergência, como pandemias, crises de saúde pública ou desastres tecnológicos, ampliando seu escopo de atuação.
- **Localização e personalização**: Permitir que o agente gere conteúdos personalizados com base na localização geográfica do usuário, adaptando as mensagens às especificidades de cada região afetada.

## Tecnologias Utilizadas

- **Machine Learning em Python**: Análise de dados ambientais e geração contextual de mensagens de alerta.
- **ESP32 com sensor ambiental**: Coleta de dados locais (ex.: nível de água) para criar posts com base em dados em tempo real.

ATUALIZAR AQUI
- **Base de dados reais**: Utilização de informações da plataforma [disasterscharter.org](https://disasterscharter.org), que reúne imagens de satélite e relatórios de desastres globais.
- **Banco de Dados**: Armazenamento e organização de mensagens geradas, registros de risco e históricos.
- **Streamlit**: Desenvolvimento de um dashboard interativo para visualização e gestão dos dados, permitindo que as equipes de emergência acessem rapidamente as informações geradas pelo agente.
- **API de previsão do tempo**: Integração com serviços meteorológicos para fornecer dados atualizados sobre condições climáticas, essenciais para a geração de alertas precisos.
- **Wokwi**: Simulação do ESP32 para monitoramento de condições ambientais, permitindo a criação de posts informativos baseados em dados reais.

## Resultados Esperados

- Aumento significativo da **agilidade e eficácia da comunicação** de riscos e procedimentos de segurança;
- **Evacuação mais rápida** e coordenada de comunidades ameaçadas;
- Redução da necessidade de ações logísticas de alto custo e complexas, em situações onde a demanda por recursos é alta;
- Suporte prático às operações de campo com **alertas visualmente otimizados** e fáceis de replicar;
- Ferramenta expansível para campanhas preventivas e treinamentos.

## Sobre o projeto

O projeto foi desenvolvido visando a usabilidade fácil e intuitiva, permitindo que equipes de emergência possam gerar e compartilhar informações rapidamente, mesmo sob pressão. A interface do dashboard foi projetada para ser simples e direta, com foco na visualização clara dos dados e na geração rápida de posts informativos.

### 1️⃣ Circuito de sensores
fazer readme do circuito de sensores

### 2️⃣ Armazenamento de Dados em Banco SQL com Python

O armazenamento dos dados coletados pelos sensores foi implementado em Python, utilizando um banco de dados SQL. O código é responsável por criar tabelas, inserir dados e realizar operações CRUD (Criar, Ler, Atualizar e Deletar) no banco de dados.

### MER

<p align="center">
  <img src="assets/mer.png" alt="MER" border="0" width=70% height=70%>
</p>


Tabela: TIPO_SENSOR
  - id (INTEGER NOT NULL) [PK]
  - nome (VARCHAR(255) NOT NULL)
  - tipo (VARCHAR(15) NOT NULL)

Tabela: SENSOR
  - id (INTEGER NOT NULL) [PK]
  - tipo_sensor_id (INTEGER NOT NULL) [FK -> TIPO_SENSOR]
  - nome (VARCHAR(255) NOT NULL)
  - descricao (VARCHAR(255))
  - data_instalacao (DATETIME)
  - latitude (FLOAT)
  - longitude (FLOAT)

Tabela: LEITURA_SENSOR
  - id (INTEGER NOT NULL) [PK]
  - sensor_id (INTEGER NOT NULL) [FK -> SENSOR]
  - data_leitura (DATETIME NOT NULL)
  - valor (FLOAT NOT NULL)

Tabela: ARQUIVO
  - id (INTEGER NOT NULL) [PK]
  - nome (VARCHAR(255) NOT NULL)
  - tipo (VARCHAR(15) NOT NULL)
  - ultima_atualizacao (DATETIME)
  - bytes_arquivo (BLOB NOT NULL)

Tabela: POST_REDE_SOCIAL
  - id (INTEGER NOT NULL) [PK]
  - conteudo (TEXT NOT NULL)
  - ultima_atualizacao (DATETIME)
  - anexo_id (INTEGER) [FK -> ARQUIVO]

---

### 🗃️ Justificativa da Escolha da Estrutura de Dados

A escolha de um banco de dados relacional foi motivada pelos seguintes fatores:

- **Integridade e Consistência:**  
  O modelo relacional garante que os dados estejam sempre íntegros e consistentes, especialmente importantes em cenários críticos como emergências.

- **Relacionamento entre Dados:**  
  A estrutura em tabelas com chaves primárias e estrangeiras permite mapear claramente as relações entre sensores, tipos, leituras, arquivos e posts. Isso facilita consultas complexas e cruzamento de informações.

- **Normalização e Redução de Redundância:**  
  O uso de tabelas normalizadas evita duplicidade de informações, tornando o armazenamento mais eficiente e a manutenção dos dados mais simples.

- **Consultas Eficientes e Flexíveis:**  
  O SQL possibilita consultas rápidas e personalizadas, essenciais para análises históricas, geração de relatórios e tomada de decisão em tempo real.

- **Escalabilidade e Facilidade de Manutenção:**  
  O modelo relacional é facilmente expansível, permitindo adicionar novos tipos de sensores, arquivos ou funcionalidades sem comprometer a estrutura existente.

- **Compatibilidade com o Ecossistema Python:**  
  A integração com bibliotecas Python amplamente utilizadas (como SQLAlchemy, Pandas, etc.) facilita o desenvolvimento, análise e visualização dos dados.

- **Integração com Ferramentas de Visualização:**  
  A estrutura relacional favorece a conexão com dashboards e ferramentas de BI, potencializando o uso dos dados coletados.

### 3️⃣ INSTALANDO E EXECUTANDO O PROJETO

O sistema foi desenvolvido em Python e utiliza um banco de dados Oracle para armazenar os dados. O código é modularizado, permitindo fácil manutenção e expansão.

## 📦 Requisitos
- Python 3.13.2
- Bibliotecas:
  - oracledb==3.1.0
  - pandas==2.2.3
  - matplotlib==3.10.1
  - streamlit==1.44.1
  - SQLAlchemy==2.0.40
  - google-genai==1.17.0
  - dotenv==0.9.9
  - pillow==11.2.1
  - fastapi==0.115.12
  - pydantic==2.11.5
  - uvicorn==0.34.3
  - plotly==6.1.2
  - scikit-learn==1.6.1
  - joblib==1.5.1

## 📂 Instalação

- Para instalar as dependências, utilize o seguinte comando:
    ```bash
    pip install -r requirements.txt
    ```
  
- Para executar o código, utilize o seguinte comando:
    ```bash
    streamlit run main_dash.py
    ```

## Arquivo de Configuração

O projeto utiliza um arquivo especial chamado **`.env`** para armazenar variáveis de ambiente sensíveis, como credenciais de banco de dados e chaves de APIs externas. Esse arquivo **não deve ser compartilhado publicamente** por questões de segurança.

### 📄 O que é o `.env`?

O `.env` é um arquivo-texto simples, onde cada linha define uma variável de ambiente no formato `NOME_VARIAVEL=valor`. Ele permite separar informações confidenciais do código-fonte, facilitando a configuração do sistema em diferentes ambientes (desenvolvimento, produção, etc).

### 🔑 Variáveis Utilizadas

| Variável      | Descrição                                                        | Exemplo de Valor                  |
|---------------|------------------------------------------------------------------|-----------------------------------|
| GEMINI_API    | Chave da API do Google GenAI (Gemini)                            | `AIza...`                         |
| API_MET       | Chave da API do OpenWeather                                      | `b1c2...`                         |
| SQL_LITE      | Define o banco de dados a ser usado (`true` ou `false`)          | `true` ou `false`                 |
| LOGGING_ENABLED      | Define se o logger da aplicação será ativado (`true` ou `false`) | `true` ou `false`                 |

### 🛡️ Segurança

- **Nunca compartilhe seu `.env` publicamente.**
- As chaves de API deste projeto foram enviadas apenas ao orientador via Teams.
- Caso precise rodar o projeto, obtenha suas próprias chaves conforme instruções abaixo.

### 🚀 Como obter suas chaves de API

- **GEMINI_API:**  
  Crie uma conta no [Google AI Studio](https://aistudio.google.com/app/apikey) e gere sua chave para o Google GenAI.
- **API_MET:**  
  Cadastre-se no [OpenWeather](https://openweathermap.org) e gere sua chave de API.

### ⚙️ Exemplo de arquivo `.env`

```plaintext
GEMINI_API=sua_chave_gemini_aqui
API_MET=sua_chave_openweather_aqui
SQL_LITE=true
LOGGING_ENABLED=true
```

- Se `SQL_LITE=true`, o sistema usará o banco SQLite local.
- Se `SQL_LITE=false`, será utilizado o banco Oracle da FIAP (o sistema apresentará uma tela de login para colocar o usuário e senha do banco de dados).

> 💡 **ATENÇÃO:**  
> Para o sistema funcionar corretamente é necessário criar o arquivo `.env` na raiz do projeto, e fornecer as chaves das apis supracitadas.

### 4️⃣ Visão Geral do Sistema

Ao executar o sistema, se foi setado o SQL_LITE como `false`, primeiramente você verá uma tela de login para inserir o usuário e senha do banco de dados Oracle da FIAP. Após o login, você terá acesso ao dashboard, onde poderá visualizar os dados coletados pelos sensores, gerar posts informativos e monitorar as condições ambientais em tempo real.

## Login

<p align="center">
  <img src="assets/readme/dashboard/login.JPG" alt="login" border="0" width=70% height=70%>
</p>

> Preencha o usuário e senha do banco de dados Oracle da FIAP para acessar o dashboard.
 
## Geração de posts para redes sociais

Ao entrar no sistema, o usuário será direcionado para a página de geração de posts, onde poderá criar posts informativos com base nos dados coletados pelos sensores e nas condições ambientais atuais.

<p align="center">
  <img src="assets/readme/dashboard/assistente_virtual.JPG" alt="assistente_virtual" border="0" width=70% height=70%>
</p>

O usuário poderá interagir normalmente com o assistente virtual, que irá gerar posts informativos com base no solicitado.

<p align="center">
  <img src="assets/readme/dashboard/criar_post.JPG" alt="criar_post" border="0" width=70% height=70%>
</p>

Também é possível solicitar para o agente criar e adicionar imagens aos posts, que serão utilizadas para ilustrar as informações e aumentar o impacto visual das comunicações.

<p align="center">
  <img src="assets/readme/dashboard/criar_imagem_1.JPG" alt="criar_imagem_1" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/criar_imagem_2.JPG" alt="criar_imagem_2" border="0" width=70% height=70%>
</p>

> **Nota**
> Algumas vezes o agente pode não criar a imagem diretamente, mas sim sugerir o prompt da criação de imagem. Se isso ocorrer é só falar para ele que o prompt está aprovado e que ele pode gerar a imagem, conforme supra ilustrado.

Por fim, é possível solicitar para o agente salvar o post criado, que será armazenado no banco de dados e poderá ser visualizado posteriormente.

<p align="center">
  <img src="assets/readme/dashboard/salvar_post.JPG" alt="salvar_post" border="0" width=70% height=70%>
</p>

## Previsão do tempo e de enchentes

O gente de IA também é capaz de coletar dados meteorológicos e prever condições climáticas, como enchentes, utilizando a API do OpenWeather. O usuário pode solicitar informações sobre o clima atual e previsões para os próximos dias.

<p align="center">
  <img src="assets/readme/dashboard/previsao_do_tempo.JPG" alt="previsao_do_tempo" border="0" width=70% height=70%>
</p>

> Para obter a previsão do tempo, o agente utiliza a API do OpenWeather, que fornece dados atualizados sobre as condições climáticas em tempo real.

<p align="center">
  <img src="assets/readme/dashboard/previsao_de_enchentes.JPG" alt="previsao_de_enchentes" border="0" width=70% height=70%>
</p>

> **ATENÇÃO**
> A previsão de enchentes é baseada nas leituras dos sensores e no modelo de IA treinado pelo grupo que será discutido abaixo. O Agente de IA chama uma tool que tem acesso ao modelo preditivo de enchentes, e depois passa a resposta para o usuário.

## Possíveis erros ao interagir com o agente

O projeto utiliza uma chave de API para desenvolvedores do Google, que pode ter limitações de uso. 
Caso o usuário encontre erros ao interagir com o agente, como mensagens de erro ou falhas na geração de posts, é possível que a chave tenha atingido o limite de requisições.
Para resolver esse problema, o usuário pode tentar novamente mais tarde ou utilizar uma chave de API própria, conforme explicado na seção "Arquivo de Configuração".
O limite de requisições da API é de 60 requisições por minuto e 1500 requisições por dia. No entanto, os modelos podem ficar fora do ar ao longo do dia, dependendo do fluxo de usuários que estão utilizando a API.

<p align="center">
  <img src="assets/readme/dashboard/erro_503.JPG" alt="erro_503" border="0" width=70% height=70%>
</p>

## Possíveis alucinações que o agente pode ter

O agente não é perfeito e pode apresentar alucinações, ou seja, gerar informações incorretas, irrelevantes ou até mesmo começar a responder em inglês.
Isso pode ocorrer devido a limitações no modelo de IA ou na interpretação do prompt pelo agente.
Caso isto ocorra, a melhor solução é clicar no botão "Novo Chat" e começar uma nova conversa.

## Visualizando e alterando imagens criadas

As imagens criadas pelo agente de IA podem ser visualizadas e alteradas diretamente no dashboard. O usuário pode acessar a página de Arquvios, onde poderá ver todas as imagens criadas, editar ou excluir aquelas que não forem mais necessárias.

<p align="center">
  <img src="assets/readme/dashboard/crud/arquivos.JPG" alt="arquivos" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/pagina_visualizacao_arquivos.JPG" alt="pagina_visualizacao_arquivos" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/criar_editar_arquivos.JPG" alt="criar_editar_arquivos" border="0" width=70% height=70%>
</p>

Para salvar um novo arquivo, o usuário pode clicar no botão "Novo", preencher o formulário e clicar em "Salvar". O arquivo será adicionado à lista de arquivos e poderá ser utilizado posteriormente na criação de posts.

<p align="center">
  <img src="assets/readme/dashboard/crud/criar_arquivo.JPG" alt="criar_arquivo" border="0" width=70% height=70%>
</p>

Para editar um arquivo existente, o usuário pode selecionar um arquivo da lista e clicar no botão "Editar", fazer as alterações necessárias e clicar em "Salvar". O arquivo será atualizado na lista de arquivos.

<p align="center">
  <img src="assets/readme/dashboard/crud/editar_arquivo_1.JPG" alt="editar_arquivo_1" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/editar_arquivo_2.JPG" alt="editar_arquivo_1" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/editar_arquivo_3.JPG" alt="editar_arquivo_1" border="0" width=70% height=70%>
</p>

Para excluir um arquivo, o usuário pode selecionar um arquivo da lista e clicar no botão "Editar" e posteriormente "Excluir". O arquivo será removido da lista de arquivos.

<p align="center">
  <img src="assets/readme/dashboard/crud/excluir_1.JPG" alt="excluir_1" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/excluir_2.JPG" alt="excluir_2" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/excluir_3.JPG" alt="excluir_3" border="0" width=70% height=70%>
</p>

## Visualizando e alterando posts criados

A lógica de visualização e alteração de posts criados é semelhante à de arquivos. O usuário pode acessar a página de Posts, onde poderá ver todos os posts criados, editar ou excluir aqueles que não forem mais necessários.
Posto isto, seguem abaixo algumas imagens que ilustram a página de posts, bem como a visualização e edição de posts criados.

<p align="center">
  <img src="assets/readme/dashboard/crud/posts_1.JPG" alt="posts_1" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/posts_2.JPG" alt="posts_2" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/crud/posts_3.JPG" alt="posts_3" border="0" width=70% height=70%>
</p>

## Visualizando e alterando sensores e leituras

Os sensores podem ser localizados no menu sob a sessão de sensores, nele o usuário poderá visualizar todos os sensores cadastrados, bem como as leituras realizadas por cada um deles.
O usuario também poderá realizar operações CRUD na mesma maneira do anteriormente citado.

<p align="center">
  <img src="assets/readme/dashboard/sensores/menu_sensores.JPG" alt="menu_sensores" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/sensores/menu_sensores_2.JPG" alt="menu_sensores_2" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/sensores/menu_sensores_3.JPG" alt="menu_sensores_3" border="0" width=70% height=70%>
</p>

No caso das leituras, o usuário poderá visualizar um gráfico com as leituras realizadas por cada sensor, podendo visualizar um gráfico com dados reais ou simulados.

<p align="center">
  <img src="assets/readme/dashboard/sensores/menu_sensores_4.JPG" alt="menu_sensores_4" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/sensores/menu_sensores_5.JPG" alt="menu_sensores_5" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/sensores/menu_sensores_6.JPG" alt="menu_sensores_6" border="0" width=70% height=70%>
</p>

## Importar Tabelas com os dados

As tabelas com os dados utilizados no sistema podem ser encontradas na pasta em `assets/database_export.zip`.

O arquivo zip contém os arquivos no formato CSV, que podem ser importados para o banco de dados utilizando o dashboard, conforme passos abaixo.

1. O usuário deve selecionar a opção "Importar Banco de Dados" no menu principal.
<p align="center">
  <img src="assets/readme/dashboard/importar_banco_de_dados/importar_bd_1.JPG" alt="importar_db" border="0" width=80% height=80%>
</p>

2. Selecione o arquivo ZIP localizado em `assets/database_export.zip`, espere carregar, role a página até o final e clique no botão "Salvar no Banco de Dados".
<p align="center">
  <img src="assets/readme/dashboard/importar_banco_de_dados/importar_bd_2.JPG" alt="salvar_db" border="0" width=80% height=80%>
</p>

3. Não feche a janela e espere a operação ser concluída. Após a conclusão, o sistema irá exibir uma mensagem de sucesso. Caso ocorra algum erro, tente novamente.

<p align="center">
  <img src="assets/readme/dashboard/importar_banco_de_dados/importar_bd_3.JPG" alt="salvar_db" border="0" width=80% height=80%>
</p>


## Previsão do tempo

O usuario também pode acessar a página de Previsão do Tempo, onde poderá visualizar as condições climáticas atuais e as previsões para os próximos dias.

<p align="center">
  <img src="assets/readme/dashboard/view_previsao_do_tempo.JPG" alt="view_previsao_do_tempo" border="0" width=70% height=70%>
</p>

## Modelo de IA para a previsão de enchentes

O tema escolhido pelo grupo para o modelo de IA foi a previsão de enchentes, uma vez que este é um dos desastres naturais mais frequentes no Brasil e que pode causar grandes danos à população.

O agente de IA tem acesso direto ao modelo de IA treinado pelo grupo, que foi desenvolvido utilizando a base de dados COLOCAR FONTE DA BASE DE DADOS AQUI.

Para realizar a previsão, o modelo de IA obtém a última leitura dos sensores de nível de água e condições ambientais, e utiliza essas informações para prever a probabilidade de enchentes na região.

O usuário também pode realizar a previsão de enchentes diretamente no dashboard.

Primeiramente, segue abaixo a view de exploração da base de dados utilizada para o treinamento do modelo de IA.

<p align="center">
  <img src="assets/readme/dashboard/modelo_preditivo/exploracao_dados_1.JPG" alt="exploracao_dados_1" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/modelo_preditivo/exploracao_dados_2.JPG" alt="exploracao_dados_2" border="0" width=70% height=70%>
</p>
<p align="center">
  <img src="assets/readme/dashboard/modelo_preditivo/exploracao_dados_3.JPG" alt="exploracao_dados_3" border="0" width=70% height=70%>
</p>

A seguir, a view onde o usuário pode realizar a previsão de enchentes, que utiliza o modelo de IA treinado pelo grupo.

<p align="center">
  <img src="assets/readme/dashboard/modelo_preditivo/previsao_de_enchentes_manual.JPG" alt="previsao_de_enchentes_manual" border="0" width=70% height=70%>
</p>

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.streamlit</b>: Pasta que contém arquivos de configuração do Streamlit, como o tema e a barra lateral.
- <b>assets</b>: Aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.
- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo de todas as fases.
  - <b>dashboard</b>: Código do dashboard desenvolvido em Python, utilizando a biblioteca Streamlit. ([dashboard](src/dashboard/))
  - <b>database</b>: Execução dos comandos de banco de dados, como Conectar, Cadastrar, Listar, Editar e Excluir.
  - <b>logger</b>: Código responsável por registrar as operações realizadas no banco de dados, como inserções, atualizações e exclusões.
  - <b>service</b>: Conexão com a api pública de previsão do tempo, responsável por coletar dados meteorológicos.
  - <b>wokwi</b>: Código do ESP32, responsável por monitorar a necessidade de irrigação em uma plantação, simulando sensores de nutrientes e condições ambientais.
- <b>README</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).
- <b>main_dash</b>: arquivo principal do dashboard, onde o código é executado. Ele foi colocado nesta localização para evitar problemas com imports

## 🗃 Histórico de lançamentos

* 0.3.0 - 05/06/2025  - Melhorias no readme, adição de imagens e explicações sobre os sensores e importação de banco de dados
* 0.2.0 - 04/06/2025  - Versão preliminar da nossa aplicação, com dashboard e funcionalidades básicas implementadas
* 0.1.0 - 23/05/2025  - Versão preliminar da nossa aplicação

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>