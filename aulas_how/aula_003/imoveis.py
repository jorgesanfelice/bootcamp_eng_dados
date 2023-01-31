
# %%

from os import WCONTINUED, link, sep
from typing import AsyncIterable
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import json


reqUrl = "https://glue-api.vivareal.com/v2/listings?addressCity=Curitiba&addressLocationId=BR>Parana>NULL>Curitiba&addressNeighborhood&addressState=Paraná&addressCountry=Brasil&addressStreet&addressZone&addressPointLat=-25.437238&addressPointLon=-49.269973&business=SALE&facets=amenities&unitTypes&unitSubTypes&unitTypesV3&usageTypes&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,phones),developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount))&size=300&from={}&q&developmentsSize=5&__vt&levels=CITY&ref&pointRadius&isPOIQuery"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "x-domain": "https://www.vivareal.com.br" 
}

payload = ""


def get_json(url, i,headersList, payload):
    ret = requests.request("GET", url.format(i), data=payload, headers=headersList)
    soup = bs(ret.text,'html.parser')
    return json.loads(soup.text)


# %%
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'wc',
        'vagas',
        'valor',
        'condominio',
        'wlink'
    ]
)
# %%
json_data = get_json(reqUrl,50,headersList, payload)

#carregando o json de uma forma que fique visualmente facil de entender a estrutura do arquivo.
json_formatted_str = json.dumps(json_data, indent=2)
print(json_formatted_str)

# %%
#Inicar com o zero para começar pegando o primeiro imovel
imovel_id = 0 
json_data = get_json(reqUrl,imovel_id,headersList, payload)
while len(json_data['search']['result']['listings']) > 0:
    qnt = len(json_data['search']['result']['listings'] )
    print(f'Quantidade de imóveis:{qnt} | total de imóveis: {imovel_id}')

    for i in range(0,qnt):
        try:
            descricao = json_data['search']['result']['listings'][i]['listing']['title']
        except:
            descricao = '-'
        try:
            try:
                endereco = json_data['search']['result']['listings'][i]['listing']['adress']['street']+", "+json_data['search']['result']['listings'][i]['listing']['adress']['street']['streetNumber']
            except:
                endereco = json_data['search']['result']['listings'][i]['listing']['adress']['street']
        except:
            endereco = '-'
        try:
            area = json_data['search']['result']['listings'][i]['listing']['totalAreas']
        except:
            area = '-'
        try:
            quartos = json_data['search']['result']['listings'][i]['listing']['bedrooms']
        except:
            quartos = '-'
        try:
            suites = json_data['search']['result']['listings'][i]['listing']['suites']
        except:
            suites = '-'                    
        try:
            wc = json_data['search']['result']['listings'][i]['listing']['bethrooms']
        except:
            wc = '-'        
        try:
            valor = json_data['search']['result']['listings'][i]['listing']['pricingInfos'][0]['price']
        except:
            valor = '-'  
        try:
            vagas = json_data['search']['result']['listings'][i]['listing']['parkingSpaces']
        except:
            vagas = '-'  
        try:
            condominio = json_data['search']['result']['listings'][i]['listing']['pricingInfos'][0]['monthlyCondoFee']
        except:
            condominio = '-'  
        try:
            wlink = 'https://www.vivareal.com.br' + json_data['search']['result']['listings'][i]['link']['href']
        except:
            wlink = '-'  
                                                
        if endereco != '-':        
            print(f'Descricao:{descricao}')
            print('/n')
            print(f'Endereço:{endereco}')              

        #carregar no dataframe a linha extraida
        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condominio,
            wlink
        ]
        
    imovel_id = imovel_id + qnt
    if imovel_id > 10000:
        break
    time.sleep(1) #deixar 3 min para evitar erro de muitas requisições (barrar IP erro 429)
    json_data = get_json(reqUrl,imovel_id,headersList, payload)


#%%
#while len(json_data['search']['result']['listing'] > 0):
#    i += 1
#    print(f"valor i: {i} \t\t qtd_imoveis: {df.shape[0]}")#
#    ret = requests.get(url.format(i))#
#    soup = bs(ret.text)#
#    houses = soup.find_all(#
#        'a', {'class': 'property-card__content-link js-card-title'})#
#
#    for house in houses:
#        try:
#            descricao = house.find('span', {'class': 'property-card__title'}).text.strip()
#        except:
#            descricao = None
#        try:
#            endereco = house.find('span', {'class': 'property-card__address'}).text.strip()
#        except:
#            endereco = None
#        try:
#            area = house.find('span', {'class': 'js-property-card-detail-area'}).text.strip()
#        except:
#            area = None
#        try:
#            quartos = house.find('li', {'class': 'property-card__detail-room'}).span.text.strip()
#        except:
#            quartos = None
#        try:
#            wc = house.find('li', {'class': 'property-card__detail-bathroom'}).span.text.strip()
#        except:
#            wc = None
#        try:
#            vagas = house.find('li', {'class': 'property-card__detail-garage'}).span.text.strip()
#        except:
#            vagas = None
#        try:
#            valor = house.find('div', {'class': 'property-card__price'}).p.text.strip()
#        except:
#            valor = None
#        try:
#            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()
#        except:
#            condominio = None
#        try:
#            wlink = 'https://www.vivareal.com.br' + house['href']
#        except:
#            wlink = None
#
        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condominio,
            wlink
        ]


#%%

print(descricao)
print(endereco)
print(area)
print(quartos)
print(wc)
print(vagas)
print(valor)
print(condominio)
print(wlink)

#%%
df.to_csv('banco_de_imoveis.csv', sep=';', index=False)