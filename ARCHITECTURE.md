# LUCAS - System Architecture Documentation

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────┐         ┌──────────────────────────┐         │
│  │   React Web Application  │         │   Streamlit Dashboard    │         │
│  │   (TypeScript + Ant D)   │         │   (Python UI)            │         │
│  │                          │         │                          │         │
│  │  • Chat Interface        │         │  • Chat Interface        │         │
│  │  • File Management       │         │  • Directory Control     │         │
│  │  • Multi-tenant Selector │         │  • Site Selector         │         │
│  └────────────┬─────────────┘         └────────────┬─────────────┘         │
│               │                                     │                        │
└───────────────┼─────────────────────────────────────┼────────────────────────┘
                │                                     │
                │ HTTP/REST                           │ Direct Python Calls
                │                                     │
┌───────────────▼─────────────────────────────────────▼────────────────────────┐
│                           APPLICATION LAYER                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────┐         │
│  │                    FastAPI Backend Server                      │         │
│  │                                                                 │         │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │         │
│  │  │   Routers    │  │   Modules    │  │ Dependencies │        │         │
│  │  │              │  │              │  │              │        │         │
│  │  │ • /upload    │  │ • adls.py    │  │ • Auth       │        │         │
│  │  │ • /chat      │  │ • rag*.py    │  │ • DB conn    │        │         │
│  │  │ • /files     │  │ • openai.py  │  │ • Config     │        │         │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │         │
│  └────────────────────────────────────────────────────────────────┘         │
│                                                                              │
└───────────────┬──────────────────────────────────────┬───────────────────────┘
                │                                      │
                │                                      │
┌───────────────▼──────────────────┐   ┌───────────────▼───────────────────────┐
│       DATA LAYER                 │   │        AI/ML SERVICES                 │
├──────────────────────────────────┤   ├───────────────────────────────────────┤
│                                  │   │                                       │
│  ┌────────────────────────────┐  │   │  ┌─────────────────────────────────┐ │
│  │  Azure Data Lake Storage   │  │   │  │   Azure OpenAI Service          │ │
│  │                            │  │   │  │                                 │ │
│  │  • File Storage            │  │   │  │  • Embeddings (1536-dim)        │ │
│  │  • Multi-tenant Folders    │  │   │  │  • GPT-4o-mini Chat             │ │
│  │  • Blob Management         │  │   │  │  • Streaming Responses          │ │
│  └────────────────────────────┘  │   │  └─────────────────────────────────┘ │
│                                  │   │                                       │
│  ┌────────────────────────────┐  │   │  ┌─────────────────────────────────┐ │
│  │  PostgreSQL + pgvector     │  │   │  │   LlamaParse Service            │ │
│  │                            │  │   │  │                                 │ │
│  │  • Vector Embeddings       │  │   │  │  • PDF → Markdown               │ │
│  │  • Document Metadata       │  │   │  │  • Document Parsing             │ │
│  │  • File Hashes             │  │   │  └─────────────────────────────────┘ │
│  │  • Multi-tenant Collections│  │   │                                       │
│  └────────────────────────────┘  │   │  ┌─────────────────────────────────┐ │
│                                  │   │  │   Cohere Re-ranking             │ │
│                                  │   │  │                                 │ │
│                                  │   │  │  • Document Re-ranking          │ │
│                                  │   │  │  • Relevance Scoring            │ │
│                                  │   │  └─────────────────────────────────┘ │
└──────────────────────────────────┘   └───────────────────────────────────────┘
```

---

## 📊 Data Flow Diagrams

### 1. Document Upload & Processing Flow

```
┌──────────┐
│  User    │
└────┬─────┘
     │ 1. Upload File
     ▼
┌─────────────────┐
│  Streamlit/     │
│  React UI       │
└────┬────────────┘
     │ 2. Send File
     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Processing                       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Step 1: File Validation & Hash Generation           │  │
│  │  • Generate MD5 hash                                 │  │
│  │  • Check for duplicates in DB                        │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 2: Upload to Azure Data Lake                   │  │
│  │  • Store in tenant/site folder                       │  │
│  │  • Update file metadata in DB                        │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 3: Document Parsing (LlamaParse)               │  │
│  │  • Extract text as Markdown                          │  │
│  │  • Handle PDF, DOCX, etc.                            │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 4: Text Chunking                               │  │
│  │  • SentenceTransformersTokenTextSplitter            │  │
│  │  • Chunk size: 512 tokens                            │  │
│  │  • Overlap: 72 tokens                                │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 5: Generate Embeddings                          │  │
│  │  • Azure OpenAI embeddings                           │  │
│  │  • 1536-dimensional vectors                          │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 6: Store in Vector Database                     │  │
│  │  • PostgreSQL with pgvector                          │  │
│  │  • Collection: {tenant_id}_{site_id}                 │  │
│  │  • Metadata: file_name, path, hash                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────┐
│  Success        │
│  Response       │
└─────────────────┘
```

### 2. Query & Retrieval Flow (RAG)

```
┌──────────┐
│  User    │
└────┬─────┘
     │ 1. Ask Question
     ▼
┌─────────────────┐
│  Chat UI        │
└────┬────────────┘
     │ 2. Send Query
     ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                             │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Step 1: Query Embedding                              │  │
│  │  • Convert query to 1536-dim vector                  │  │
│  │  • Azure OpenAI embeddings                           │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 2: Vector Similarity Search                     │  │
│  │  • Search in collection: {tenant}_{site}             │  │
│  │  • Retrieve top k=30 similar chunks                  │  │
│  │  • Include similarity scores                         │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 3: Re-ranking (Cohere)                          │  │
│  │  • Re-rank 30 documents by relevance                 │  │
│  │  • Improve precision                                 │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 4: Context Assembly                             │  │
│  │  • Combine top documents                             │  │
│  │  • Add file names and metadata                       │  │
│  │  • Format for GPT                                    │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │ Step 5: Generate Response                            │  │
│  │  • GPT-4o-mini with context                          │  │
│  │  • Streaming response                                │  │
│  │  • HTML formatting                                   │  │
│  └──────────────────┬───────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │  Stream     │
              │  Response   │
              │  to User    │
              └─────────────┘
```

---

## 🗄️ Database Schema

### PostgreSQL Tables

#### 1. Vector Collections (Auto-created by LangChain)
```sql
-- Collection naming: {tenant_id}_{site_id}
-- Example: "company_abc_engineering_dept"

Table: langchain_pg_collection
- uuid: UUID (Primary Key)
- name: VARCHAR (Collection name)
- cmetadata: JSONB (Metadata)

Table: langchain_pg_embedding
- id: UUID (Primary Key)
- collection_id: UUID (Foreign Key)
- embedding: VECTOR(1536) (pgvector type)
- document: TEXT (Chunk content)
- cmetadata: JSONB (file_name, file_path, content_hash)
```

#### 2. File Metadata (Custom Tables)
```sql
Table: file_metadata
- id: SERIAL (Primary Key)
- file_path: VARCHAR (Azure path)
- file_name: VARCHAR
- content_hash: VARCHAR (MD5)
- uploaded_at: TIMESTAMP
- tenant_id: VARCHAR
- site_id: VARCHAR

Table: file_contents
- id: SERIAL (Primary Key)
- file_path: VARCHAR
- file_name: VARCHAR
- content_hash: VARCHAR
- chunk_count: INTEGER
- processed_at: TIMESTAMP
```

---

## 🔐 Multi-Tenant Architecture

### Tenant Isolation Strategy

```
Tenant: "CompanyA"
├── Site: "Engineering"
│   ├── Azure Path: CompanyA/Engineering/
│   ├── Vector Collection: CompanyA_Engineering
│   └── Files: [doc1.pdf, doc2.docx]
│
└── Site: "Marketing"
    ├── Azure Path: CompanyA/Marketing/
    ├── Vector Collection: CompanyA_Marketing
    └── Files: [presentation.pdf]

Tenant: "CompanyB"
└── Site: "Sales"
    ├── Azure Path: CompanyB/Sales/
    ├── Vector Collection: CompanyB_Sales
    └── Files: [report.pdf]
```

### Isolation Mechanisms

1. **File Storage**: Separate folders in Azure Data Lake
2. **Vector DB**: Separate collections per tenant/site
3. **Query Scope**: Queries only search within user's collection
4. **Access Control**: Site selection enforces data boundaries

---

## 🚀 Performance Optimizations

### 1. Vector Store Caching
```python
# Cache vector store connections per collection
vector_store_cache = {}

def get_vector_store(collection_name):
    if collection_name in vector_store_cache:
        return vector_store_cache[collection_name]
    # Create new connection
    vector_store = PGVector(...)
    vector_store_cache[collection_name] = vector_store
    return vector_store
```

### 2. Connection Pooling
- Uses `psycopg_pool` for database connection management
- Reduces connection overhead
- Handles concurrent requests efficiently

### 3. Async Operations
- FastAPI async endpoints for non-blocking I/O
- Concurrent file uploads
- Streaming responses

### 4. Chunking Strategy
- **512 tokens per chunk**: Balances context and precision
- **72-token overlap**: Ensures continuity across chunks
- **Sentence-aware splitting**: Maintains semantic coherence

### 5. Re-ranking Pipeline
- Initial retrieval: k=30 (high recall)
- Cohere re-ranking: Top results (high precision)
- Reduces false positives

---

## 🔄 System Workflows

### Workflow 1: New Tenant Onboarding

```
1. Add tenant to config/tenant_site_mapping.py
2. Create Azure folder: {tenant_id}/{site_id}/
3. Vector collection auto-created on first upload
4. Users can now upload and query documents
```

### Workflow 2: Document Lifecycle

```
Upload → Parse → Chunk → Embed → Store
  ↓
Query → Search → Re-rank → Generate
  ↓
Delete → Remove from Azure → Remove from Vector DB → Remove metadata
```

---

## 📡 API Architecture

### REST Endpoints (FastAPI)

```
POST /api/upload
- Multipart file upload
- Returns: {filename, status, hash}

POST /api/chat
- Body: {query, site_id, tenant_id}
- Returns: Streaming response

GET /api/files?site_id={id}
- Returns: [{name, size, last_modified}]

DELETE /api/files/{filename}
- Deletes from Azure + Vector DB
```

### Streamlit Direct Calls

```python
# No REST API - direct Python function calls
from modules.ragRetrivalProcess import retrive_rag_info
from modules.adls import upload_file, list_files_in_directory

response = retrive_rag_info(query, site_id, tenant_id)
files = list_files_in_directory(path)
```

---

## 🛡️ Security Considerations

### Current Implementation

1. **Azure Authentication**: Client Secret Credentials
2. **Environment Variables**: Sensitive data in .env
3. **Data Isolation**: Multi-tenant collections
4. **Hash Verification**: MD5 for file integrity

### Production Recommendations

1. **Azure Key Vault**: Store secrets securely
2. **RBAC**: Role-based access control
3. **API Authentication**: JWT tokens
4. **Rate Limiting**: Prevent abuse
5. **Input Validation**: Sanitize user inputs
6. **HTTPS**: Encrypt data in transit

---

## 📈 Scalability Considerations

### Current Capacity

- **Vector DB**: Handles millions of embeddings
- **Azure Data Lake**: Petabyte-scale storage
- **Concurrent Users**: Limited by FastAPI workers

### Scaling Strategies

1. **Horizontal Scaling**: Multiple FastAPI instances
2. **Load Balancing**: Distribute requests
3. **Database Sharding**: Partition by tenant
4. **Caching Layer**: Redis for frequent queries
5. **CDN**: Static assets delivery

---

## 🔧 Technology Decisions

### Why PostgreSQL + pgvector?

- ✅ Open-source and cost-effective
- ✅ ACID compliance for metadata
- ✅ Native vector operations
- ✅ Mature ecosystem

### Why Azure OpenAI?

- ✅ Enterprise SLA
- ✅ Data residency compliance
- ✅ Integration with Azure ecosystem
- ✅ Consistent API

### Why LangChain?

- ✅ Abstracts vector store operations
- ✅ Simplifies RAG pipeline
- ✅ Active community
- ✅ Extensible architecture

### Why Cohere Re-ranking?

- ✅ Improves retrieval precision
- ✅ Better than pure vector search
- ✅ Fast inference
- ✅ Easy integration

---

## 📊 Monitoring & Logging

### Current Logging

```python
logging.basicConfig(level=logging.INFO)
logging.info("Document uploaded")
logging.error(f"Error: {str(e)}")
```

### Production Monitoring Recommendations

1. **Application Logs**: Structured logging (JSON)
2. **Metrics**: Prometheus + Grafana
3. **Tracing**: OpenTelemetry
4. **Alerts**: Error rate, latency thresholds
5. **Cost Tracking**: Azure Cost Management

---

## 🎯 Future Enhancements

1. **Advanced Search**: Hybrid search (keyword + vector)
2. **Multi-modal**: Image and table understanding
3. **Conversation Memory**: Chat history persistence
4. **Fine-tuning**: Custom embeddings for domain
5. **Analytics Dashboard**: Usage statistics
6. **Batch Processing**: Bulk document uploads
7. **API Rate Limiting**: Protect resources
8. **User Management**: Authentication & authorization

---

<div align="center">

**This architecture supports enterprise-scale document intelligence with production-ready patterns**

</div>
