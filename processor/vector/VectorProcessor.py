from utils.logging.config import LoggerConfig


class VectorProcessor:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = VectorStore()

        config = LoggerConfig("VectorProcessor")
        self.logger = config.logger

    def process_document(self, document):
        chunks = self.chunking(document)
        embeddings = self.embedding_model.embed(chunks)
        self.logger.info(f"using {self.embedding_model} to embed document")
        self.store_vectors(embeddings)
