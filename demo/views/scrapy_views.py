from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from ..models import ScrapyItem, Company

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        # check if url format is valid
        validate(url)
    except ValidationError:
        return False

    return True


def is_valid_stock_code(code):
    if code == 'all':
        return True
    try:
        Company.objects.get(code=code)
        return True
    except Company.DoesNotExist:
        return False


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        stock_code = request.POST.get('stock_code', None)

        if not stock_code:
            return JsonResponse({'error': '입력이 부족합니다.'})

        if not is_valid_stock_code(stock_code):
            return JsonResponse({'error': '정보가 없는 주식 종목이거나, 옮바르지 않은 입력입니다.'})

        unique_id = str(uuid4()) # create a unique ID.

        # This is the custom settings for scrapy spider.
        # We can send anything we want to use it inside spiders and pipelines.
        # I mean, anything
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.

        task = scrapyd.schedule('default', 'newsbot',
                settings=settings, stock_code=stock_code)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': '입력이 부족합니다.'})

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                items = ScrapyItem.objects.filter(unique_id=unique_id)

                return JsonResponse({
                    'data': list(items.values())
                })
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})


def is_valid_secure(secure):
    if secure == 'DEEPSTOCK_SECURE':
        return True
    return False


@csrf_exempt
@require_http_methods(['POST'])
def stock_init(request):
    if request.method == 'POST':
        # Secure Check
        secure = request.POST.get('secure', None)

        if not secure:
            return JsonResponse({'ERROR': '보안이 없는 요청입니다.'})
        if not is_valid_secure(secure):
            return JsonResponse({'ERROR': '보안 입력값이 올바르지 않습니다.'})

        unique_id = str(uuid4())  # create a unique ID.

        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

        task = scrapyd.schedule('default', 'stockbot',
                                    settings=settings)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
