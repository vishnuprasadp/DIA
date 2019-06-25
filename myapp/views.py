from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpRequest
import datetime
from SPARQLWrapper import SPARQLWrapper, JSON ,XML
import myapp.Query 
import json
from django.views.decorators.csrf import csrf_exempt


# def index(request):
#     return HttpResponse("Hello, world!!! ")

# def index(request):
#    return render(request, "hello.html", {})

def hello(request):
   today = datetime.datetime.now().date()
   return render(request, "hello.html", {"today" : today})

@csrf_exempt
def deptList(request):
    if request.method == 'GET':
        results=myapp.Query.selDeptList()
        print(results)
        return HttpResponse(results, content_type='application/json')
    elif request.method == 'POST':
        request=json.loads(request.body)
        myapp.Query.enterDept(request)
        return HttpResponse("Sucessfully Added Department")

@csrf_exempt
def deptDetail(request):
   a=request.META['HTTP_DEPTID']
   print(a)
   results=myapp.Query.selDeptDetail(a)
   res=json.dumps(results)
   return HttpResponse(res, content_type='application/json')


def viewArticle(request, articleId):
   text = ("Displaying article Number : %s"%articleId)
   return HttpResponse(text)

def viewArticles(request, month, year):
   text = "Displaying articles of : %s/%s"%(year, month)
   return HttpResponse(text)

# Create your views here.
# @csrf_exempt
# def deptList(request, *args, **kwargs):
#    print(request)
#    results,orglist=myapp.Query.select()
#    print(results)
#    return JsonResponse(results)

# received_json_data=json.loads(request.body)
#         print (received_json_data)