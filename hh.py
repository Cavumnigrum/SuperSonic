import requests

def fetch_vacancies_from_hh(text, area, per_page):
    url = "https://api.hh.ru/vacancies"
    params = {
        'text': text,  
        'area': area,  
        'per_page': per_page  
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies = response.json()['items']
        for vacancy in vacancies:
            print(f"Title: {vacancy['name']}\n"\
            f"Company: {vacancy['employer']['name']}\n"\
            f"Location: {vacancy['area']['name']}\n"\
            f"Skills: {', '.join(skill['name'] for skill in vacancy.get('key_skills', []))}\n"\
            f"Salary: {vacancy.get('salary')}\n"\
            f"Employment Type: {vacancy.get('employment')}\n"\
            f"Source: hh.ru\n")
    else:
        print("Failed to fetch vacancies from hh.ru")

fetch_vacancies_from_hh("Python developer",1,10)
