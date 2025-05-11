import requests
from bs4 import BeautifulSoup
import csv

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    Today_Meteo = soup.find_all("section", {'class': 'item-principal cont-izq card tabla-xhoras'})
    
    def get_Date(Today_Meteo, soup):
        if not Today_Meteo:
            print("❌ Section météo non trouvée.")
            return
        Place = Today_Meteo[0].find('h2').text.strip()
        Date = Today_Meteo[0].find('span').text.strip()
        DateTime = f"{Place} {Date}"
        print(f"\n📍 {DateTime}\n")
        
        Data = []
        Rows = soup.find_all('tr')
        
        for row in Rows[1:]:
            hourElement = row.find('span', {'class': 'text-princ'})
            hour = hourElement.text.strip() if hourElement else "N/A"
            
            temperature_element = row.find('td', {'class': 'title-mod changeUnitT'})
            temperature = temperature_element.text.strip() if temperature_element else "N/A"
            
            description_all = row.find('td', {'class': 'descripcion'})
            description_type = description_all.find('strong').text.strip() if description_all and description_all.find('strong') else "N/A"
            
            row_wind = row.find('span', {'class': 'velocidad col'}) 
            if row_wind:
                wind_label = row_wind.find('strong').text.strip() if row_wind.find('strong') else "N/A"
                wind_spans = row_wind.find_all('span')
                wind_value = f"{wind_spans[0].text.strip()} : {wind_spans[1].text.strip()}" if len(wind_spans) >= 2 else "N/A"
            else:
                wind_label = "N/A"
                wind_value = "N/A"
            
            Etat_1 = row.find('span', {'class': 'col velocidad'})
            if Etat_1:
                titre_etat = Etat_1.find('strong').text.strip() if Etat_1.find('strong') else "N/A"
                fps_span = Etat_1.find("span")
                fps_text = fps_span.text.strip() if fps_span else "N/A"
                fps_value = Etat_1.find("span", {'class': 'fps-valor'})
                fps_value_text = fps_value.text.strip() if fps_value else "N/A"
                full_etat = f"{titre_etat} : {fps_text} {fps_value_text}"
            else:
                titre_etat = fps_text = fps_value_text = full_etat = "N/A"
            
            print(f"🕒 {hour} | 🌡️ {temperature} | ☁️ {description_type} | 🌬️ {wind_label}: {wind_value} | 🎯 {full_etat}")
            
            Data.append({
                'hour': hour,
                'temperature': temperature,
                'description': description_type,
                'wind_label': wind_label,
                'wind_value': wind_value,
                'etat': titre_etat,
                'fps_text': fps_text
            })
        with open('meteo_tunis.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=Data[0].keys())
            writer.writeheader()
            writer.writerows(Data)
            print("\n✅ Données sauvegardées dans 'meteo_tunis.csv'")
    
    get_Date(Today_Meteo, soup)

page = requests.get("https://www.tameteo.com/meteo_Tunis-Afrique-Tunisie-Tunis-DTTA-1-8952.html")
main(page)
