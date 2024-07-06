from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

class SearchRequest(BaseModel):
    name: str = None
    salary: str = None
    experience: str = None
    area: str = None

@app.post("/search")
async def search_vacancies(request: SearchRequest):
    # Реализация поиска вакансий
    title = request.name
    salary = request.salary
    experience = request.experience
    area = request.area

    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': title if title else '',
        'salary': salary if salary else '1',
        'currency': 'RUR',
        'experience': experience if experience else 'noExperience',
        'area': area if area else '1',  # Russia
        'per_page': '50',
        'only_with_salary': 'true'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies = response.json().get('items', [])
        if vacancies:
            results = []
            for vacancy in vacancies:
                results.append({
                    'title': vacancy['name'],
                    'employer': vacancy['employer']['name'],
                    'area': vacancy['area']['name'],
                    'salary': vacancy['salary']['from'],
                    'url': vacancy['alternate_url']
                })
            return results
        else:
            raise HTTPException(status_code=404, detail="No vacancies found")
    else:
        raise HTTPException(status_code=500, detail="Error fetching data from hh.ru")

@app.post("/filter")
async def filter_vacancies(request: SearchRequest):
    # Реализация фильтрации вакансий
    conditions = []
    params = []
    
    if request.name:
        conditions.append("(title ILIKE %s OR professional_roles ILIKE %s OR responsibility ILIKE %s)")
        params.extend([f"%{request.name}%", f"%{request.name}%", f"%{request.name}%"])
    
    if request.salary:
        conditions.append(
            "((salary_from IS NULL AND salary_to IS NULL) OR (salary_from IS NULL AND salary_to >= %s) OR (salary_to IS NULL AND salary_from <= %s) OR (salary_from <= %s AND salary_to >= %s))"
        )
        params.extend([request.salary, request.salary, request.salary, request.salary])
    
    if request.experience:
        conditions.append("experience = %s")
        params.append(request.experience)
    
    if request.area:
        conditions.append("area ILIKE %s")
        params.append(f"%{request.area}%")

    query = f"SELECT * FROM vacancies WHERE {' AND '.join(conditions)}"
    
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            return results
        else:
            raise HTTPException(status_code=404, detail="No vacancies found")
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
