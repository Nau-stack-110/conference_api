from faker  import Faker
import random
import json
from datetime import datetime, timedelta
faker = Faker('fr_FR')
madagascar_faritra =  [
    'Antananarivo', 'Antsirabe', 'Fianarantsoa', 'Mahajanga', 'Toliara', 'Fianarantsoa',
    'Antsiranana', 'Nosy Be', 'Morondava', 'Toamasina', 'Mandoto', 'Ambositra', 'Ambatolampy',
]
def generate_price():
    return "Gratuit" if random.random() < 0.3 else f"{random.randint(10000, 60000)} Ar"
def generate_conf(c):
    conferences = []
    for _ in range(c):
        title = faker.catch_phrase()
        description = faker.text(max_nb_chars=200)
        # image = faker.image_url()
        today = datetime.now()
        days_ahead = random.choice([2, 3, 4, 5, 14, 49])  
        conference_date = today + timedelta(days=days_ahead)
        if conference_date.year < 2025:
            conference_date = datetime(2025, conference_date.month, conference_date.day)
        conference_date_str = conference_date.date().isoformat()
        lieu = random.choice(madagascar_faritra)
        price = generate_price()
        conferences.append({
            "title":title,
            "description": description,
            "date":conference_date_str,
            "lieu":lieu,
            "price":price
        })
    return conferences

def generate_sessions(conferences):
    sessions = []
    for conference_id, conference in enumerate(conferences, start=1):
        start_time = datetime.strptime(conference['date'], "%Y-%m-%d")
        for i in range(random.randint(1, 5)):  # Générer entre 1 et 5 sessions par conférence
            # Générer une heure de début aléatoire entre 8h et 19h
            hour = random.randint(8, 19)  # 19 pour inclure 19h, car on ajoute 2h pour la prochaine session
            session_start_time = start_time.replace(hour=hour, minute=0)  # Assurez-vous que la date de la session est la même que celle de la conférence
            session = {
                "conference": conference_id,
                "title": faker.catch_phrase(),
                "speaker": faker.name(),
                "profession": faker.job(),
                "start_time": session_start_time.isoformat()  # Format datetime
            }
            sessions.append(session)
    return sessions

# Générer les conférences
conference_data = generate_conf(30)

# Générer les sessions basées sur les conférences
session_data = generate_sessions(conference_data)

# Sauvegarder les données dans un fichier JSON
with open('sessions.json', 'w', encoding='utf-8') as f:
    json.dump(session_data, f, ensure_ascii=False, indent=2)

print("Données des sessions sauvegardées et générées avec succès dans sessions.json !")


