### Requirments Specification

`cat requiremets.txt`

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

1. [intro](http://localhost:8000/)  
`http://localhost:8000/`  

2. [stock list](http://localhost:8000/stock_list/)  
`http://localhost:8000/stock_list/`  

3. [stock analysis](http://localhost:8000/stock_analysis/{stock_code})  
`http://localhost:8000/stock_analysis/{stock_code}`   


---
### Crawling

```
.
├── README.md
├── deepstock
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── demo
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── practice
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views
├── manage.py
└── scrapy_app
    ├── dbs
    ├── logs
    ├── scrapy.cfg
    └── scrapy_app
```
1. run scrapy demon
`cd scrapy_app`
`scrapyd`

2. run django server
`python manage runserver`

3. post url
```
curl --data-urlencode "url=https://google.com" \
     --data-urlencode "crawlingStatus=null" \
     --data-urlencode "data=null" \
     --data-urlencode "taskID=null" \
     --data-urlencode "uniqueID=null" \
     --data-urlencode "statusInterval=1" \
     http://localhost:8000/api/crawl/

{"task_id": "165da486141611ea8f5d9cf387aa8006", "unique_id": "40ccda17-5f50-446b-926d-4227d26dd0c4", "status": "started"}
```

4. get url
> task_id : 165da486141611ea8f5d9cf387aa8006
> unique_id : 40ccda17-5f50-446b-926d-4227d26dd0c4
```
curl -o result.html -X GET http://localhost:8000/api/crawl?task_id=165da486141611ea8f5d9cf387aa8006&unique_id=40ccda17-5f50-446b-926d-4227d26dd0c4
```