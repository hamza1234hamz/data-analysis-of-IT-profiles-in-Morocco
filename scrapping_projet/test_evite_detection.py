import requests 
from bs4 import BeautifulSoup
import pandas as pd
"""
   user-agent :  Il fournit des informations sur le logiciel utilisateur, 
    tel que le nom du navigateur, sa version, le système 
    d'exploitation et parfois d'autres détails sur le client. 
 """
# les methode d'eviter le bloquage de web scrapping
# 1 er methode : changer le user-agent :
    # recuperer le user-agent de votre navigateur :
response = requests.get('https://httpbin.org/user-agent')
response.json()
    # cela va retuner : {'user-agent': 'python-requests/2.31.0'} 
    # alors vortre user-agent commecnce par python-requetes ce qui facile de le bloquer par les sites 
    # car le serveur va identifier que vous etes entraine d'utiliser le model requests pour acceder au contenu de page 


    # le user-agent exist dans les headers de notre requete http 
    # alores on peut le echanger : 
headres = {"user-agent" : "toto"}
response1 = requests.get('https://www.rekrute.com/offres-emploi-informatique-electronique-fonction-13.html',headers=headres)
src = response1.content
soup = BeautifulSoup(src, "lxml")
# normalement dans les cas normal  rekrute.com bloque les request provient de model request mais quand on change le user-agent il accepte les request



# 2 eme methode  : est de chnager les headres : 
    # on peut aussi configuer autre headers qui peut etr utile pour l'envoie des requetes
    # recuperer les hesdres : 
response = requests.get('https://httpbin.org/headers')
response.json()
 

# 3 eme methode : utilisation des proxie 
"""
Un proxy est un serveur intermédiaire qui agit comme un intermédiaire entre l'utilisateur et Internet.
Lorsqu'un utilisateur envoie une requête vers Internet, 
celle-ci est d'abord envoyée au serveur proxy. 
Le proxy traite ensuite cette requête et l'envoie au
serveur web de destination. De la même manière, lorsque le serveur web
répond, la réponse est d'abord envoyée au proxy, qui la transmet ensuite à l'utilisateur. 
Ainsi, toutes les communications entre l'utilisateur et Internet passent par le proxy.

ce qui permet de changer l'adresse ip dont provient la requete.
pour eviter le bloquge de notre requetes grace aux nomber enorme des requetes .
"""

    # ON peut avoir une list des proxcy que on tourner pour acceder a chaque fois au site depuis une proxy diffeerent 
    # pour avoir une list gratuit des proxy : https://free-proxy-list.net/
response2 = requests.get('https://free-proxy-list.net/')
    # scraping la table des proxy :
proxy_list = pd.read_html(response2.text)[0]
    # ajouter une colone de  url 
proxy_list["url"] = "http://" + proxy_list['IP Address'] + ":" +proxy_list["Port"].astype(str)
#print(proxy_list)
    # pour savoir les liste de proxy qui support les Https et les http
        # https 
https_proxies = proxy_list[proxy_list["Https"]=="yes"]
#print(https_proxies.shape[0])
        #http 
http_proxies = proxy_list[proxy_list["Https"]=="no"]
#print(http_proxies.shape[0])

    #selection les proxies valide  on testant les proxiez valide et les non valide

url = "https://httpbin.org/ip"
good_proxies = set()
for proxy_url in https_proxies['url']:
    proxies ={
        "http":proxy_url,
        "https":proxy_url,
    }
    try: 
        response = requests.get(url,proxies=proxies,timeout=2) 
        good_proxies.add(proxy_url)
        print(f"proxy {proxy_url} ok , added to good proxy list")
        
    except Exception:
        pass
    
    if len(good_proxies) >=3:
        break
