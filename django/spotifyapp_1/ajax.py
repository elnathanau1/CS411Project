import json
import os
from django.http import Http404, HttpResponse

CACHE = '.spotipyoauthcache'

def more_todo(request):
    if request.is_ajax():
        os.remove(CACHE)
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
