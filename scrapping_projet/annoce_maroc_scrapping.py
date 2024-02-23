import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

announce_details = []
# Scraping the annonce maroc website 
for num_page in range(1, 11) : 
    result = requests.get(f'https://www.marocannonces.com/maroc/offres-emploi-domaine-informatique-multimedia-internet-b309.html?kw=informatique&f_3=Informatique+%2F+Multim%C3%A9dia+%2F+Internet&page={num_page}')
    src = result.content
    soup = BeautifulSoup(src, "lxml")


    all_offres = soup.find("ul", {"class": "cars-list"})
    jobs_offres = all_offres.find_all("li", class_=lambda x: x != "adslistingpos")



    for i in range(1, len(jobs_offres)):    
        job = jobs_offres[i].find("div", {"class": "holder"})
        job_title = job.find("h3").text.strip()
        job_location = job.find("span", {"class": "location"}).text.strip()
        job_details_link = jobs_offres[i].find("a").attrs['href']
        
        time_announce_div = jobs_offres[i].find("div", {"class": "time"})
        
        # Check if 'time_announce_div' exists
        if time_announce_div:
            # Check if it contains a 'span' tag
            job_time_span = time_announce_div.find("span", {"class": "cnt-today"})
            if job_time_span:
                job_time = job_time_span.text.strip()
            else:
                # If 'span' tag doesn't exist, check for 'em' tag
                job_time_em = time_announce_div.find_all("em", {"class": "date"})
                if job_time_em[1]:
                    job_time = job_time_em[1].text.strip()
                else:
                    job_time = "N/A"
        else:
            job_time = "N/A"


        #acceder a chaque link tout seul 
        link = f"https://www.marocannonces.com/{job_details_link}"
        result1 = requests.get(link)
        src1 = result1.content
        soup1 = BeautifulSoup(src1, "lxml")    
        job_info = soup1.find("ul", {"class": "extraQuestionName"}, {"id": "extraQuestionName"})
        job_infos_details = job_info.find_all("li")
        
        
        Domaine = job_infos_details[0].text.strip()
        Fonction = job_infos_details[1].text.strip()
        Contrat = job_infos_details[2].text.strip()
        Entreprise = job_infos_details[3].text.strip()
        salaire = job_infos_details[4].text.strip()
        Niveau_etude = job_infos_details[5].text.strip()

        print(Domaine , Fonction , Contrat , Entreprise , salaire , Niveau_etude)

        announce_details.append({"job Title": job_title,
                                "adresse company": job_location,
                                "time": job_time,
                                "Domaine": Domaine,
                                "Fonction": Fonction,
                                "Contrat": Contrat,
                                "Entreprise": Entreprise,
                                "salaire": salaire,
                                "Niveau_etude": Niveau_etude})



    
with open('anounce_jobs_INFORMATIQUE.csv', mode='w', newline='', encoding='utf-8') as file:
    keys = announce_details[0].keys()
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    writer.writerows(announce_details)


