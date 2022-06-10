from msrest import Configuration


# container configuration
FILE_CONTAINER_NAME = "iotfiles"
META_CONTAINER_NAME = "metadata"

# sas configuration
SAS_DURATION = 100

# bloom filter configuration
MAX_ELEMENTS = 1000
ERROR_RATE = 0.1
CHUNK_SIZE = 20
SAMPLE_PARAM = 0.3