from http import HTTPStatus
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (
    TokenAuthentication, 
    BasicAuthentication, 
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view, 
    permission_classes, 
    authentication_classes
)

from .models import File

from cloud_handler import uploadFile, verifyIntegrity

def generateBlobName(fileName, time):
    filename, extention = fileName.split('.')
    blob_name = filename + str(time) + '.' + extention
    blob_name = blob_name.replace(' ', '')
    return blob_name.replace(':', '-')

# Create your views here.
class FileView(APIView):
    authentication_classes = [
        # SessionAuthentication, 
        # BasicAuthentication, 
        TokenAuthentication
    ]
    permission_classes = [IsAuthenticated]

    def get(self, req, format=None):
        files = File.objects.all()
        listFiles = list(map(lambda x: x.getDict(), files))
        return Response(listFiles)

    def post(self, req, format=None):
        FILE_KEY_NAME = 'uploadfile'
        if FILE_KEY_NAME not in req.FILES:
            return Response({'error': 'No file uploaded'}, status=HTTPStatus.BAD_REQUEST)

        file = req.FILES['uploadfile']
        time = datetime.utcnow()
        blob_name = generateBlobName(file.name, time)
        
        metaData = uploadFile(blob_name, file)
        dbFile = File(name=file.name, blob_name=blob_name, size=metaData['size'], created_at=time)
        dbFile.save()
        dbFile.generateSasUrl()
        print('file saved')
        return Response(dbFile.getDict(), status=HTTPStatus.CREATED)

class FileDetailView(APIView):
    authentication_classes = [
        # SessionAuthentication, 
        # BasicAuthentication, 
        TokenAuthentication
    ]
    permission_classes = [IsAuthenticated]

    def get(self, req, blob_name, format=None):
        try:
            fileDb = File.objects.get(blob_name = blob_name)
        except File.DoesNotExist as e:
            return Response({"error": "file not found"}, status=HTTPStatus.NOT_FOUND)
        print(fileDb.sas_url)
        fileDb.generateSasUrl()
        return Response(fileDb.getDict(), status=HTTPStatus.OK)

def verifySaveFileIntegrity(file):
    blob_name = file.blob_name

    integrityScore, integrity = verifyIntegrity(blob_name)

    file.integrity_score = integrityScore
    file.integrity = integrity
    file.verified_at = datetime.now()
    file.save()

    return file

@api_view(['POST'])
@authentication_classes([
    # SessionAuthentication, 
    # BasicAuthentication, 
    TokenAuthentication
    ])
@permission_classes([IsAuthenticated])
def verifyFileIntegrityView(req, blob_name):
    print(req.POST)
    try:
        fileDb = File.objects.get(blob_name = blob_name)
    except File.DoesNotExist as e:
        return Response({"error": "file not found"}, status=HTTPStatus.NOT_FOUND)
    print(fileDb)
    verifySaveFileIntegrity(fileDb)
    return Response(fileDb.getDict(), status=HTTPStatus.OK)

@api_view(['POST'])
@authentication_classes([
    # SessionAuthentication, 
    # BasicAuthentication, 
    TokenAuthentication
])
@permission_classes([IsAuthenticated])
def verifyIntegrityView(req):
    files = File.objects.all()
    filesRes = list(map(lambda file: verifySaveFileIntegrity(file).getDict(), files))
    return Response(filesRes, status=HTTPStatus.ACCEPTED)