from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

"""
def home(request):
    #return HttpResponse("hello world")
    template = loader.get_template("home/index.mhtml")
    return HttpResponse(template.render())
    #return render(request, 'home.html')
"""
def BCAT(request):
    #return HttpResponse("hello world")
    template = loader.get_template("BCAT/index.html")
    return HttpResponse(template.render())


"""

def test(request):
    template = loader.get_template("test/index.html")

    #path = "C:\\Users\\Rashed\\Desktop\\testing.txt"

    #file = open(path, "w")
    #file.write("all your base are belong to us")
    #file.close()
    
    return HttpResponse(template.render())

@csrf_exempt
def api(request):
    template = loader.get_template("api/index.html")
    return HttpResponse(template.render())

    
    if request.method == 'POST':
        my_data = {'foo': 'bar', 'baz': [1, 2, 3]}
        json_data = json.dumps(my_data)
        return render(request, 'index.html', {'json_data': json_data})

        #data = json.loads(request.body)
        #message = data['message']
        #return JsonResponse({'message': message})
        
    elif request.method == 'GET':
        template = loader.get_template("home/index.html")
        return HttpResponse(template.render())
        #return render(request, 'api/index.html')
   
    """
