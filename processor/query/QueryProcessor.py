class QueryProcessor:
    def __init__(self, llm_model, vector_store):
        self.llm_model = llm_model
        self.vector_store = vector_store

    def process_query(self, query):
        relevent_docs = self.vector_store.similary_search(query)
        context = self.prepare_context(relevent_docs)
        response = self.llm.generate_response(query, context)
        return self.validate_response(response)
