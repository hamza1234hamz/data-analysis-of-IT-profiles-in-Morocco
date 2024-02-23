import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
announce_details = []

for num_page in range(1, 21):
    headres = {"user-agent" : "toto"}
    result = requests.get(f'https://www.rekrute.com/offres.html?s=1&p={num_page}&o=1&positionId%5B0%5D=13',headers=headres)
    src = result.content
    soup = BeautifulSoup(src, "lxml")


    Contrat = []

    all_anounce =  soup.find_all("li",{"class":"post-id"})
    for i in range(len(all_anounce)) :
        offre = all_anounce[i].find("div",{"class":"section"})
        offre_titile_location = offre.find("h2").text.strip()
        offre_title , offre_location = offre_titile_location.split(" | ")
        
        offre_detail = offre.find_all("li")
        offre_time = offre.find("em",{"class":"date"}).find("span").text.strip()

        Domaine= offre_detail[0].find("a").text.strip()
        Fonction = offre_detail[1].find("a").text.strip()
        experience = offre_detail[2].text.strip()
        niveau_etude = offre_detail[3].find("a").text.strip()
        Contrat = offre_detail[4].find("a").text.strip()
        job_details_link = offre.find("h2").find("a").attrs['href']


        
        announce_details.append({"job Title": offre_title,
                                    "adresse company": offre_location,
                                    "time": offre_time,
                                    "Domaine": Domaine,
                                    "Fonction": Fonction,
                                    "Contrat": Contrat,
                                    "Entreprise": "N/A",
                                    "salaire": "N/A",
                                    "Niveau_etude": niveau_etude})
        
    # Write the details to a CSV file
    with open('rekrute_IT.csv', mode='w', newline='', encoding='utf-8') as file:
        keys = announce_details[0].keys()
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(announce_details)

        
        

        
        


        















