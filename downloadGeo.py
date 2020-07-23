import os
import requests
from bs4 import BeautifulSoup
import lxml
from requests import Request, Session
import easygui

# url do site geosampa
url = "http://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx"

# url para acesso a api que devolve os arquivos presentes na região selecionada
url_request = "http://geosampa.prefeitura.sp.gov.br/PaginasPublicas/map.geo/get"

# valores limites da área selecionada
bbox = easygui.enterbox("Cole o conteúdo do bbox aqui", "Entre com os valores limites da área selecionada")

# inicia uma sessão e já salva o cookie
session = requests.Session();

# cabeçalho de request para a api
userAgent = {'User-Agent': 'python-requests/2.4.3 CPython/3.4.0'}
headers = {'Host' : 'geosampa.prefeitura.sp.gov.br', 'Referer' : 'http://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx', 'X-Requested-With' : 'XMLHttpRequest', 'Upgrade-Insecure-Requests' : '1' }
headers.update(userAgent)
r = session.get(url, headers=headers, stream=True);
s = BeautifulSoup(r.text, "lxml");

# monta os parâmetros e passa para a api
s.find(id='hc').get('value')
data = {"hc": s.find(id='hc').get('value'),"tipoServico": "DWFS1","request": "GetFeature","service": "wfs","version": "1.0.0","typeName": {"geoportal:quadricula_folha_mds"},"featureType": {"geoportal:quadricula_folha_mds"},"bbox": bbox}
response = session.get(url_request, headers=headers, params=data)

# pega a resposta da api e lê como xml
soup = BeautifulSoup(response.text, "xml")
listForDownload = [];

# Acha todas as tags <geoportal:cd_quadricula> que contém o nome do arquivo
for quadricula in soup.findAll("geoportal:cd_quadricula"):
    t = str(quadricula);
    t = t[t.find('>')+1:t.rfind('<')]
    listForDownload.append(t)

#If there is no such folder, the script will create one automatically
folder_location = r'C:\webscraping'
if not os.path.exists(folder_location):os.mkdir(folder_location)

# Link para download
url_ = "https://laz-m3dc-pmsp.s3-sa-east-1.amazonaws.com/MDS_color_"

# Acrescenta o nome do arquivo no link para download e faz o download na pasta webscrapping
for num in listForDownload:
    filename = num+'.laz'
    f = open(folder_location+'\\'+filename, 'wb')
    f.write(requests.get(url_+ filename).content)
    f.close();
