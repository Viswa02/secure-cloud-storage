from django.shortcuts import render

# Create your views here.
def homePage(req):
    return render(req, 'frontend/index.html')

def filesPage(req):
    return render(req, 'frontend/upload_file.html')

def fileDetailsPage(req, blob_name):
    return render(req, 'frontend/detail_file.html', {'blob_name': blob_name})

def verifyPage(req):
    return render(req, 'frontend/verify.html')

def loginPage(req):
    return render(req, 'frontend/login.html')

def logoutPage(req):
    return render(req, 'frontend/login.html')