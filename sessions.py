import random
import json
from faker import Faker
from datetime import timedelta, datetime

faker = Faker('fr_FR')

anarana = [
    "Herizo","Soa","Finaritra","Sahaza","Linda","Sedy","Bema",
    "Sedera","John","Mika","Mickael","Narovana","Daniel",
    "Safidy","Nicole","Nomena","Toky","Toliniaina","Vatosoa","Faniry",
    "Rakoto","Naina","Niaina","Fanomezantsoa","Njara","laza","Zafy",
    "Falitiana","Ezeckel","Zo","Fitahiana","Jean","Andry","Andrianina",
    "Zandrykely","Zandrybe", "Faneva","Koto","Benja", "Naunau", "Arnel",
    "Heritiana","Mandrindra","Olivier","Santatra","Sarobidy", "Bryan",
    "Dianah", "Vannyah", "Mariah", "Maminiaina", "Sariaka", "Fitia", "Jordan", 
]

def generate_session(c, conference_date, num_conf=30):
    sessions = []    
    conference_sessions = {conf_id: [] for conf_id in range(1, num_conf + 1)}
    for _ in range(c):
        conference = random.randint(1, num_conf)
        start_time = generate_valid_start_time(conference_sessions[conference], conference_date)
        
        session =  {
            "title": faker.catch_phrase(),
            "conference": conference,
            "speaker": random.choice(anarana),
            "profession": faker.job(),
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        sessions.append(session)
        conference_sessions[conference].append(start_time)
        
    return sessions

def generate_valid_start_time(existing_times, conference_date):
    start_of_day = datetime.combine(conference_date, datetime.min.time()) + timedelta(hours=8)  # Commence à 8h
    end_of_day = start_of_day + timedelta(hours=9)  # Fin à 17h
    
    while True:
        proposed_time = faker.date_time_between(start_date=start_of_day, end_date=end_of_day)
        
        if all(abs((proposed_time - existing_time).total_seconds()) >= 5400 for existing_time in existing_times):
            return proposed_time

# Exemple d'utilisation avec la date de la conférence
# Vous devez appeler generate_conf pour obtenir la date de la conférence
from conferences import generate_conf

conference_data = generate_conf(30)
conference_date = datetime.fromisoformat(conference_data[0]['date'])  # Prendre la date de la première conférence
session_data = generate_session(60, conference_date, num_conf=30)

with open('sessions.json', 'w', encoding='utf-8') as f:
    json.dump(session_data, f, ensure_ascii=False, indent=2)

print("Données de sessions générées avec succès dans sessions.json !")


