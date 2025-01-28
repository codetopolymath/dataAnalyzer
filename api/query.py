from fastapi import FastAPI

app = FastAPI()

@app("/query")
async def process_query(query: str):
    query_processor = QueryProcessor(llm_model, vector_store)
    return await query_processor.process_query(query)