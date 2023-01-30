#%%

from os import sep
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

#%%

#primeira versao para validar o link e carregar seu conteudo.
url = 'https://portalcafebrasil.com.br/todos/podcasts/'

#%%

ret = requests.get(url)

#%%
#conteudo da pagina
ret.text

# %%

#BeautifulSoup -> biblioteca recomendada para percorrer paginas html. melhor forma de fazer essa atividade.
#Identifica o melhor parser, faz as identificações e quebra o texto de uma forma mais agradável
#nesse caso -> features=html.parser
soup = bs(ret.text)

# %%

#vai ser tratada depois como se fosse uma lista. da para usar recursos de filtro
soup
# %%

#Usando o inspect do chrome, conseguimos ver os elementos, marcações, estilos, entre outros da pagina
#Dessa forma usamos o BeautifulSoup para "encontrar" (find) o item especifico da pagina
soup.find('h5')
# %%

#Agora trazendo apenas o valor da tag
soup.find('h5').text
# %%

#apenas da tag "a" a marcação href
soup.find('h5').a['href']
# %%

#pegar todos os h5 e carregar na lista
lst_podcast = soup.find_all('h5')
# %%
for item in lst_podcast:
    print(f"EP: {item.text} - Link: {item.a['href']}")

#obs: Após essa estapa percebemos um problema. não pega todos os episódeos de fato, pois a pagina tem paginação para carregar conforme baixa a pagina.
#entregando apenas um pedaço da pagina

# %%

# usar {} para passar o parametro para o link da pagina com o numero da pagina
#usando o google inspect do chrome, vai perceber no network rolando para baixo o ?ajax=true
#
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'


# %%
#pegando o conteudo da pagina 5
url.format(5)
# %%

#cria uma função para retornar a lista de episódios (forma mais elegante)
def get_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')


# %%
#testar chamada da funçao
#retorna toda a lista da pagina 5 (exemplo apenas para validar a ideia)
get_podcast(url.format(5))

#%%

# carregar nossa log para ser usado abaixo
#validar erros 
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


# %%

#fazer um loop para carregar a lista de podcast do site
#enquanto existirem itens a serem lidos, vai varrendo.

i = 1
#lista vazia que sera preenchida
lst_podcast = []
#lista com cada pagina existente começando da 1
lst_get = get_podcast(url.format(i))
log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")

#enquanto o tamanho da minha lista for maior que zero (estiver recendo algo) vai executando a lista
while len(lst_get) > 0:
    #lista =  ela de volta + nova lista (incrementa) 
    lst_podcast = lst_podcast + lst_get
    i += 1
    #relimentando a lista a cada iteracao
    lst_get = get_podcast(url.format(i))
    log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")


# %%
#quantidade de episódios capturados após a varredura no site
len(lst_podcast)

# %%
#lista de episódios e seus links
lst_podcast

# %%
#criando um dataframe pandas para armazenar esses episódios em formato tabular. Passando nome das colunas. 
df = pd.DataFrame(columns=['nome', 'link'])

#após criado, nao temos nenhuma linha no dataframe, apenas duas colunas
df.shape

# %%
#trazendo a ultima posição do dataframe, temos 0, ou seja... nada.
df.shape[0]

# %%

for item in lst_podcast:
    #percorrer a lista localizando o ultima posição dele (localizar loc)
    # duas variaveis por linha (o nome do episódio, link)
    df.loc[df.shape[0]] = [item.text, item.a['href']]
    #na linha acima, vai inserir sempre na ultima posicao uma nova linha (nome e link) até acabar de farrer toda a lista de podcast
    
#%%
#lista depois de percorrida
#duas dimenssões do dataframe -> (linhas, colunas)
df

# %%
#aqui temos a quantidade de linhas do dataframe e a quantidade de colunas (duas dimenssões)
df.shape

# %%
#aqui temos a quantidade de linhas ou o ultima posição das linhas que é seu indice.
df.shape[0]


# %%
#separador sep -> Index como false tira o numero das linhas 
df.to_csv('banco_de_podcast.csv', sep=';', index=False)

