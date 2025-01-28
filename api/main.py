from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.logging.config import LoggerConfig

from processor.query.QueryProcessor import QueryProcessor

app = FastAPI(
    title="Enterprise Data Analyzer API",
    description="API for processing enterprise data using vector embeddings and LLM",
    version="1.0.0",
    openapi_tags=[
        {"name": "Query", "description": "Query processing endpoints"},
        {"name": "Data Sources", "description": "Data source management endpoints"},
        {
            "name": "Vector Processing",
            "description": "Vector processing and embedding endpoints",
        },
    ],
)

logger_config = LoggerConfig("API")
logger = logger_config.logger


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str
    confidence: float
    relevantSources: list[str]


@app.post(
    "/query",
    response_model=QueryResponse,
    tags=["Query"],
    summary="Process a natural language query",
)
async def process_query(request: QueryRequest):
    try:
        logger.info("Processing query")
        llm_model, vector_store = None, None
        query_processor = QueryProcessor(llm_model, vector_store)
        result = await query_processor.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# run using `PYTHONPATH=. uvicorn api.main:app --reload`
