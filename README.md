# ENTERPRISE DATA ANALYZER

## DATA SOURCE

Enterprise Data Sources

- Structured Data (Databases)
  - SQL Databases
  - NoSQL Databases
- Unstructured Data
  - Documents (PDFs, DOCs)
  - Text Files
- Semi-structured Data
  - JSON Files
  - XML Documents

## DATA PROCESSING PIPELINE

```markdown
Raw Data → Data Connector → Data Chunking → Vector Embedding → Vector Store
                                   │
                                   └── Metadata Extraction
```

## FLOWCHART

```mermaid
flowchart TB
    subgraph DataSources[Enterprise Data Sources]
        DB[(Databases)]
        Files[Documents & Files]
        API[API Data]
    end

    subgraph DataProcessing[Data Processing Layer]
        Connectors[Data Connectors]
        Parser[Document Parser]
        Chunker[Text Chunker]
    end

    subgraph VectorProcessing[Vector Processing]
        Embeddings[Embedding Generator]
        VStore[(Vector Store)]
        MetaStore[(Metadata Store)]
    end

    subgraph LLMLayer[LLM Processing Layer]
        Ollama[Ollama Server]
        LlamaIndex[LlamaIndex]
        RAG[RAG Pipeline]
    end

    subgraph QueryLayer[Query Processing]
        Router[Query Router]
        Cache[Response Cache]
        Validator[Response Validator]
    end

    subgraph API[API Layer]
        REST[REST API]
        WebSocket[WebSocket]
    end

    DataSources --> DataProcessing
    DataProcessing --> VectorProcessing
    VectorProcessing --> LLMLayer
    LLMLayer --> QueryLayer
    QueryLayer --> API

    %% Additional connections
    VStore -.-> RAG
    MetaStore -.-> RAG
    Cache -.-> Router
```

### Branching Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/\***: New features and non-emergency fixes
- **hotfix/\***: Emergency production fixes
- **release/\***: Release preparation
