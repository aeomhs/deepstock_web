### Requirments Specification

`cat requiremets.txt`

---
## Migration

### secret.json  
- 프로젝트 루트와 동일한 경로

### DB migrate  
```
python manage.py migrate
```

### collect static  
```
python manage.py collectstatic
```

### Run server  
```
python manage.py runserver
```

---
### Valid URL

#### [intro](http://localhost:8000/)  
```
http://localhost:8000/
```  

#### [stock list](http://localhost:8000/stock_list/)  
```
http://localhost:8000/stock_list/
```  

#### [stock analysis](http://localhost:8000/stock_analysis/{stock_code})  
```
http://localhost:8000/stock_analysis/{stock_code}
```   


---
### Crawling Implements 

```
.
├── deepstock
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── demo
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                /* Data Model ; ORM */
│   ├── templates
│   ├── tests.py
│   ├── urls.py                  /* request forwarding */
│   └── views
│        ├── scrapy_views.py     /* 크롤링 요청 */
│        └── views.py          
├── manage.py
├── requirements.txt
└── scrapy_app
    ├── logs                     /* 로그 */
    ├── scrapy.cfg
    └── scrapy_app
         ├── pipelines.py        /* 크롤링 데이터 Django DB 저장 */
         ├── settings.py
         └── spiders
              ├── newsbot.py      /* 주식 종목 관련 뉴스 크롤링 */
              └── stockbot.py     /* 주식 데이터 가져오기 */

```


## Test Crawling
#### open terminal, Run scrapy demon  
```
cd scrapy_app
scrapyd
...
2019-12-12T13:59:31+0900 [Launcher] Scrapyd 1.2.1 started: max_proc=16, runner='scrapyd.runner'
```
#### open new terminal , Run django server  
```
python manage runserver
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
---
## News Crawling
#### POST Request, Start news crawling  
```
/* 종목 관련 뉴스 크롤링 */
curl --data-urlencode "stock_code=005930" http://localhost:8000/api/crawl/

{"task_id": "61b6b1c81c9c11ea99039cf387aa8006", "unique_id": "ab1a0337-8838-4eb8-b4dd-0f4464d97d79", "status": "started"}

/* 모든 종목 관련 뉴스 크롤링 */
curl --data-urlencode "stock_code=all" http://localhost:8000/api/crawl/
```

#### GET Request, Return news crawling data  
> task_id : 61b6b1c81c9c11ea99039cf387aa8006  
> unique_id : ab1a0337-8838-4eb8-b4dd-0f4464d97d79  

```
curl -o result.html -X GET http://localhost:8000/api/crawl?task_id=61b6b1c81c9c11ea99039cf387aa8006&unique_id=ab1a0337-8838-4eb8-b4dd-0f4464d97d79
```

---
## Stock Data Crawling
#### POST Request, Start Stock List crawling
```
curl --data-urlencode "secure=DEEPSTOCK_SECURE" http://localhost:8000/api/stock_init/

{"task_id": "67e615fe1c9f11eabe129cf387aa8006", "unique_id": "929c5938-dd91-4bcd-b625-22d07f8d8180", "status": "started"}
```