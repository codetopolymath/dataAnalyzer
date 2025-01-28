

class VectorProcessor():
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = VectorStore()

    def process_document(self, document):
        chunks = self.chunking(document)
        embeddings = self.embedding_model.embed(chunks)
        self.store_vectors(embeddings)