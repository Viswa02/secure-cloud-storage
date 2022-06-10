from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, uuid

from azure.storage.blob import BlobServiceClient, __version__, generate_blob_sas, BlobSasPermissions
from bloom_filter import BloomFilter
import pickle
from io import BytesIO

from config import (
    FILE_CONTAINER_NAME,
    META_CONTAINER_NAME,
    SAS_DURATION
)

from config import (
    ERROR_RATE,
    MAX_ELEMENTS,
    CHUNK_SIZE
)

ENV = os.environ.get('ENV', 'dev')

if ENV == 'dev':
    load_dotenv()

# print(__version__)

CONNECTION_STR = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
ACC_NAME = os.environ.get('AZURE_STORAGE_ACC_NAME')
PRIMARY_KEY = os.environ.get('AZURE_STORAGE_PRIMARY_KEY')

blobServiceClient = BlobServiceClient.from_connection_string(CONNECTION_STR)

def createBloomFilter():
    '''
        creates a bloom-filter with the project configuration.
    '''
    
    return BloomFilter(max_elements=MAX_ELEMENTS, error_rate=ERROR_RATE)

def generateMetaData(fileDataBytes, fileName):
    '''
        generates meta data(BloomFilter) from 'fileDataBytes'

        :param fileDataBytes: BytesIO file-data
        :param fileName: str file-name
        :return: dict meta-data
    '''

    file_name = fileName
    file_size = len(fileDataBytes)
    meta = {
        'name': file_name,
        'size': file_size
    }
    bf = createBloomFilter()
    remaining_size = file_size
    i = 0
    print('loop started')
    while remaining_size > 0:
        pos = i * CHUNK_SIZE
        if remaining_size <= CHUNK_SIZE:
            file_bytes = fileDataBytes[pos : pos + remaining_size]
            remaining_size -= remaining_size
        else:
            file_bytes = fileDataBytes[pos : pos + CHUNK_SIZE]
            remaining_size -= CHUNK_SIZE
        i += 1
        bf.add(file_bytes)
    print('loop ended')

    meta['bf'] = bf

    return meta

def storeMetaBlob(blobName, metaData):
    '''
        Stores 'metaData' in 'meta container'

        :param blobName: str - name for new blob
        :param metaData: dict - meta data
        :return: None
    '''
    blobName += '.meta'
    blobClient = blobServiceClient.get_blob_client(container=META_CONTAINER_NAME, blob=blobName)
    metaDataBytes = pickle.dumps(metaData)
    metaDataBufferIO = BytesIO(metaDataBytes)
    blobClient.upload_blob(metaDataBufferIO)

def storeFileBlob(blobName, file):
    '''
        Stores 'file' in 'iotfiles' container
        
        :param blobName: str - name for new blob
        :param file: BytesIO - file-data
        :return: None
    '''
    blobClient = blobServiceClient.get_blob_client(container=FILE_CONTAINER_NAME, blob=blobName)
    blobClient.upload_blob(file)

def uploadFile(fileName, file):
    '''
        Stores 'meta-data' & 'file-data' of 'file' in proper containers
        
        :param file: fileobject - file needs to be uploaded
        :return: None
    '''
    bf = createBloomFilter()

    dataBytes = file.read()
    dataBytesIO = BytesIO(dataBytes)

    meta = generateMetaData(dataBytes, file.name)

    dataBytesIO = BytesIO(dataBytes)
    storeFileBlob(fileName, dataBytesIO)
    print('file uploaded to cloud')

    storeMetaBlob(fileName, meta)
    print('meta data saved')

    return meta



# with open('config.py', 'rb') as file:
#     uploadFile(file)

def listContainerBlobs(containerName):
    '''
        Lists all available blobs in 'containerName'
        
        :param containerName: str - container name
        :return: None
    '''
    containerClient = blobServiceClient.get_container_client(containerName)

    blobList = containerClient.list_blobs()
    for blob in blobList:
        print(blob.name)

def listFileBlobs():
    '''
        List all available blobs in 'iotfiles' container
    '''
    listContainerBlobs(FILE_CONTAINER_NAME)

# listFileBlobs()

def downloadFile(blobServiceClient, containerName, blobName):
    '''
        Downloads a 'blobName' blob from 'containerName' container
        
        :param blobServiceClient: BlobServiceClient
        :param containerName: str - name of the container
        :param blobName: str - name of the blob
        :return: BufferedReader - downloaded file
    '''
    blobClient = blobServiceClient.get_blob_client(container=containerName, blob=blobName)
    print(blobClient.get_block_list())
    return blobClient.download_blob().readall()

def downloadFileBlob(blobName):
    '''
        Downloads 'blobName' blob from files container
        
        :param blobName: str - name of the blob
        :return: BufferedReader - downloaded file
    '''
    return downloadFile(blobServiceClient, FILE_CONTAINER_NAME, blobName)

def downloadMetaBlob(blobName):
    '''
        Downloads 'blobName' blob from meta container
        
        :param blobName: str - name of the blob
        :return: BufferedReader - downloaded file
    '''
    return downloadFile(blobServiceClient, META_CONTAINER_NAME, blobName+'.meta')

def getMetaData(blobName):
    '''
        Fetches meta-data for blob 'blobName'
        
        :param blobName: str - name of the blob
        :return: dict - meta-data
    '''
    data = downloadMetaBlob(blobName)
    metaData = pickle.loads(data)
    return metaData  

# print(getMetaData('config.py.meta'))

def verifyIntegrity(blobName):
    meta = getMetaData(blobName)
    fileDataBytes = downloadFileBlob(blobName)
    bf = meta['bf']

    file_size = len(fileDataBytes)

    if(file_size != meta['size']):
        return (0, False)

    remaining_size = file_size
    i = 0
    errorCount = 0
    print('loop started')
    while remaining_size > 0:
        pos = i * CHUNK_SIZE
        if remaining_size <= CHUNK_SIZE:
            file_bytes = fileDataBytes[pos : pos + remaining_size]
            remaining_size -= remaining_size
        else:
            file_bytes = fileDataBytes[pos : pos + CHUNK_SIZE]
            remaining_size -= CHUNK_SIZE
        i += 1
        if file_bytes not in bf:
            errorCount += 1
    print('loop ended')
    if errorCount == 0:
        integrity = True
    else:
        integrity = False

    totalBlocks = i
    validChunks = totalBlocks - errorCount
    integrityScore = (validChunks / totalBlocks) * 100

    return (integrityScore, integrity)

# print(verifyIntegrity('summa2022-06-04 08-17-56.679445.py'))

def generateBlobReadOnlySasKey(blobName):
    '''
        Generates readonly sas key for blob 'blobName' in files container
        
        :param blobName: str - name of the blob
        :return: str - sas token readonly access
    '''
    sasKey = generate_blob_sas(
        account_name=ACC_NAME, 
        container_name=FILE_CONTAINER_NAME, 
        blob_name=blobName, 
        account_key=PRIMARY_KEY, 
        permission=BlobSasPermissions.from_string('r'), 
        start=datetime.utcnow(), 
        expiry=datetime.utcnow() + timedelta(hours=SAS_DURATION)
    )
    return sasKey

def generateBlobReadOnlySasUrl(blobName):
    '''
        Generates readonly sas url for blob 'blobName' form files container
        
        :param blobName: str - name of the blob
        :return: str - sas url readonly access
    '''
    sasKey = generateBlobReadOnlySasKey(blobName)
    sasUrl = 'https://'+ACC_NAME+'.blob.core.windows.net/'+FILE_CONTAINER_NAME+'/'+blobName+'?'+sasKey
    return sasUrl