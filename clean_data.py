import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re
import time

def clean_and_geocode():
    df = pd.read_excel("exocoworkingenrichi.xlsx")
    
    def extract_cp(adresse):
        if pd.isna(adresse) or adresse == "N/A":
            return "N/A"
        match = re.search(r'(\d{5})', str(adresse))
        if match:
            return match.group(1)
        match_dep = re.search(r'\b(75|77|78|91|92|93|94|95)\d{0,3}\b', str(adresse))
        return match_dep.group(0) if match_dep else "N/A"
    
    df['Code_Postal'] = df['Adresse'].apply(extract_cp)
    df['Departement'] = df['Code_Postal'].str[:2]

    geolocator = Nominatim(user_agent="mssi_coworking_project")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    print("Géocodage en cours (cela peut prendre du temps)...")
    df['location'] = df['Adresse'].apply(lambda x: geocode(x) if x != "N/A" else None)
    
    df['latitude'] = df['location'].apply(lambda loc: loc.latitude if loc else None)
    df['longitude'] = df['location'].apply(lambda loc: loc.longitude if loc else None)
    
    df_clean = df.dropna(subset=['latitude', 'longitude'])
    
    df_clean.to_csv("coworking_ready.csv", index=False)
    print(f"Nettoyage terminé : {len(df_clean)} espaces prêts.")

if __name__ == "__main__":
    clean_and_geocode()