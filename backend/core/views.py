from django.http import HttpResponse
#pa ver su andava la api :p
def inicio(request):
    return HttpResponse("API Delivery funcionando")