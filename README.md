# Vacancy Analyzer API

#### An asynchronous FastAPI application that collects, filters, and stores job vacancies from HeadHunter API.

The API focuses on open remote positions and allows you to:
- Fetch vacancies by keyword (Python).
- Filter and store only relevant vacancies in a PostgreSQL database.
- Database cleanup: removal of archived and closed vacancies
- Keyword search (only by `title`)
- Export vacancies to CSV

### Installation

```
git clone https://github.com/AKamysheva/Job-Vacancies-Analyzer-API.git
cd vacancy-analyzer
pip install -r requirements.txt
uvicorn app.main:app --reload
```


