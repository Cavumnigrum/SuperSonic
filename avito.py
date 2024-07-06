import requests

def fetch_vacancies_from_avito(query, loc, per_page):
    url = "https://api.avito.ru/v1/vacancies"  
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  
    }
    params = {
        'query': query,  
        'location': loc,  
        'per_page': per_page  
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        vacancies = response.json()['data']
        for vacancy in vacancies:
            print(f"Title: {vacancy['title']}\n"\
            f"Company: {vacancy['company']}\n"\
            f"Location: {vacancy['location']}\n"\
            f"Skills: {vacancy.get('skills')}\n"\
            f"Salary: {vacancy.get('salary')}\n"\
            f"Employment Type: {vacancy.get('employment_type')}\n"\
            f"Source: avito.ru\n")
    else:
        print("Failed to fetch vacancies from avito.ru")

fetch_vacancies_from_avito()
