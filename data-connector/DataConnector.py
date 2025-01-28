# # Example configuration structure
# config = {
#     "data_sources": {
#         "databases": ["postgresql://..."],
#         "document_paths": ["path/to/docs"],
#         "api_endpoints": ["https://api..."]
#     },
#     "chunk_size": 512,
#     "overlap": 50
# }

from abc import ABC, abstractmethod

class DataConnector(ABC):

    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def chunking(self):
        pass