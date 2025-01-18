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
        image = faker.image_url()
        today = datetime.now()
        days_ahead = random.choice([2, 14, 49])  # 2 jours, 2 semaines (14 jours), ou 7 semaines (49 jours)
        conference_date = today + timedelta(days=days_ahead)
        if conference_date.year < 2025:
            conference_date = datetime(2025, conference_date.month, conference_date.day)
        conference_date_str = conference_date.isoformat()
        lieu = random.choice(madagascar_faritra)
        price = generate_price()
        conferences.append({
            "title":title,
            "description": description,
            "image":image,
            "date":conference_date_str,
            "lieu":lieu,
            "price":price
        })
    return conferences
conference_data = generate_conf(30)
with open('conferences.json', 'w', encoding='utf-8') as f:
    json.dump(conference_data, f, ensure_ascii=False, indent=2)
print("Données conferences sauvegardées et générées avec succès dans conferences.json !")


