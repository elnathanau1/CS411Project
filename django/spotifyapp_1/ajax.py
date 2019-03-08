import json
from django.http import Http404, HttpResponse

def more_todo(request):
    if request.is_ajax():
        print("clicked button")
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
