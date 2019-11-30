### Requirments Specification

```
Python Version : 3.6.8
Django Version : 2.2.7
```

---
### Running
1. secret.json
- 프로젝트 루트와 동일한 경로

2. DB migrate
`python manage.py migrate`

3. collect static
`python manage.py collectstatic`

4. Run server
`python manage.py runserver`

---
### Valid URL
`localhost:8000/`
`localhost:8000/stock_list/`
`localhost:8000/stock_analysis/{stock_code}`
