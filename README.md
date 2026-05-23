# LUCAS - AI-Powered Document Intelligence Platform

<div align="center">

**Enterprise-grade RAG (Retrieval-Augmented Generation) chatbot for intelligent document search and conversational AI**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.4-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9.5-3178C6.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)

---

## 🎯 Overview

**LUCAS** is a production-ready, multi-tenant RAG-based chatbot system that enables organizations to interact with their documents using natural language. Built for a startup environment, it integrates seamlessly with **Azure Data Lake Storage** and leverages advanced AI models for semantic search and intelligent responses.

### What Makes LUCAS Special?

- **🧠 Advanced RAG Pipeline**: Combines vector search with re-ranking for highly accurate document retrieval
- **☁️ Cloud-Native**: Built for Azure with Data Lake integration and scalable architecture
- **🏢 Multi-Tenant**: Supports multiple organizations/sites with isolated data collections
- **⚡ Real-Time Streaming**: Provides streaming chat responses for better UX
- **🔒 Enterprise-Ready**: Includes file management, deduplication, and comprehensive logging

---

## ✨ Key Features

### 🤖 Intelligent Chatbot
- Natural language queries across uploaded documents
- Context-aware responses using GPT-4o-mini
- Streaming responses for real-time interaction
- Source attribution with file names and departments

### 📁 Document Management
- Upload/download/delete files via Azure Data Lake
- MD5 hash-based deduplication
- Support for multiple file formats (PDF, DOCX, etc.)
- Batch file operations with ZIP download

### 🔍 Advanced Search
- **Vector Similarity Search**: Using pgvector with 30 nearest neighbors
- **Semantic Embeddings**: Azure OpenAI embeddings (1536 dimensions)
- **Re-ranking**: Cohere re-ranking for improved relevance
- **Token-Aware Chunking**: 512 tokens with 72-token overlap

### 🏗️ Production Features
- Docker containerization with multi-stage builds
- PostgreSQL with pgvector extension
- Connection pooling and caching
- Comprehensive error handling and logging
- Multi-tenant data isolation

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  React Frontend  │              │ Streamlit UI     │        │
│  │  (TypeScript)    │              │ (Python)         │        │
│  └────────┬─────────┘              └────────┬─────────┘        │
└───────────┼────────────────────────────────┼──────────────────┘
            │                                 │
            ▼                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Routers    │  │   Modules    │  │ Dependencies │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────┬─────────────────────────────────┬──────────────────┘
            │                                  │
            ▼                                  ▼
┌──────────────────────┐          ┌──────────────────────┐
│   Azure Data Lake    │          │  PostgreSQL + Vector │
│   (File Storage)     │          │  (pgvector)          │
└──────────────────────┘          └──────────────────────┘
            │                                  │
            └──────────────┬───────────────────┘
                           ▼
                  ┌─────────────────┐
                  │  AI Services    │
                  │  • OpenAI GPT   │
                  │  • Embeddings   │
                  │  • LlamaParse   │
                  │  • Cohere       │
                  └─────────────────┘
```

### Data Flow

1. **Document Upload** → Azure Data Lake → LlamaParse → Text Chunking → Embeddings → Vector DB
2. **User Query** → Embedding → Vector Search (k=30) → Cohere Re-ranking → Context Assembly → GPT Response

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | REST API framework | 0.115.4 |
| **Python** | Core language | 3.10+ |
| **PostgreSQL** | Primary database | Latest |
| **pgvector** | Vector similarity search | 0.2.5 |
| **LangChain** | AI orchestration | 0.2.15 |
| **LlamaParse** | Document parsing | 0.5.1 |
| **Azure SDK** | Cloud integration | Latest |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI framework | 18.3.1 |
| **TypeScript** | Type safety | 4.9.5 |
| **Ant Design** | Component library | 5.21.2 |
| **TailwindCSS** | Styling | 3.4.13 |
| **Streamlit** | Alternative UI | Latest |

### AI/ML
| Service | Purpose |
|---------|---------|
| **Azure OpenAI** | Embeddings & Chat completions |
| **GPT-4o-mini** | Language model |
| **Cohere** | Document re-ranking |
| **Sentence Transformers** | Token splitting |

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Poetry** - Python dependency management
- **Git** - Version control

---

## 📂 Project Structure

```
LUCAS/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── core/              # Core configurations
│   │   ├── routers/           # API endpoints
│   │   ├── modules/           # Business logic
│   │   │   ├── adls.py        # Azure Data Lake operations
│   │   │   ├── ragPreProcess.py    # Document processing pipeline
│   │   │   ├── ragRetrivalProcess.py  # Query & retrieval
│   │   │   ├── openai.py      # OpenAI integration
│   │   │   └── db/            # Database operations
│   │   └── main.py            # Application entry point
│   ├── pyproject.toml         # Poetry dependencies
│   └── Dockerfile
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── views/             # Page views
│   │   ├── controllers/       # Business logic
│   │   └── App.tsx            # Main app component
│   └── package.json
│
├── app_pages/                 # Streamlit pages
│   ├── chat.py               # Chat interface
│   └── files.py              # File management UI
│
├── config/                    # Configuration files
│   └── tenant_site_mapping.py
│
├── buildout/                  # Docker configurations
│   └── docker/
│       └── development/
│           ├── Dockerfile
│           └── docker-compose.yml
│
├── main.py                    # Streamlit entry point
├── Requirements.txt           # Python dependencies
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- **Docker** & Docker Compose
- **Python 3.10+**
- **Node.js 16+** (for frontend development)
- **PostgreSQL 14+** with pgvector extension
- **Azure Account** (for Data Lake access)
- **OpenAI API Key**
- **Cohere API Key**

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd LUCAS

# 2. Create environment file
cp template.env .env
# Edit .env with your credentials

# 3. Build and run with Docker
docker compose -f buildout/docker/development/docker-compose.yml build --no-cache
docker compose -f buildout/docker/development/docker-compose.yml up -d

# 4. Access the application
# Streamlit UI: http://localhost:8501
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install poetry
poetry install

# Run backend
uvicorn app.main:app --reload
# API: http://localhost:8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start
# UI: http://localhost:3000
```

#### Streamlit Setup

```bash
# From project root
python -m venv .venv
.\.venv\Scripts\Activate

# Install dependencies
pip install -r Requirements.txt

# Run Streamlit
streamlit run main.py
# UI: http://localhost:8501
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Azure Data Lake Configuration
AZURE_ADLS_STORAGE_URL=https://<account>.dfs.core.windows.net
AZURE_ADLS_CLIENT_SECRET=<your-client-secret>
AZURE_ADLS_TENANT_ID=<your-tenant-id>
AZURE_ADLS_CLIENT_ID=<your-client-id>

# Database Configuration
HOST=<postgres-host>
PORT=5432
DBNAME=<database-name>
USERNAME=<db-username>
PASSWORD=<db-password>

# API Keys
OPENAI_API_KEY=<your-openai-key>
LLAMA_CLOUD_API_KEY=<your-llama-key>

# Tenant Configuration
TENANT_ID=<your-tenant-id>
```

### Database Setup

```sql
-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Database will auto-create collections per tenant
```

---

## 💻 Usage

### Streamlit Interface

1. **Select Site**: Choose your organization/site from the sidebar
2. **Upload Documents**: Navigate to "Directory Control" and upload files
3. **Chat**: Switch to "Chatbot Interface" and ask questions about your documents

### API Endpoints

```bash
# Health check
GET http://localhost:8000/health

# Upload file
POST http://localhost:8000/api/upload
Content-Type: multipart/form-data

# Query chatbot
POST http://localhost:8000/api/chat
{
  "query": "What is the project timeline?",
  "site_id": "site-123",
  "tenant_id": "tenant-456"
}

# List files
GET http://localhost:8000/api/files?site_id=site-123
```

---

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔬 Technical Highlights

### RAG Pipeline Implementation

```python
# Document Processing (ragPreProcess.py)
1. Upload → LlamaParse (Markdown extraction)
2. Text Splitting → SentenceTransformers (512 tokens, 72 overlap)
3. Embedding → Azure OpenAI (1536-dim vectors)
4. Storage → PostgreSQL with pgvector

# Query Processing (ragRetrivalProcess.py)
1. Query → Embedding
2. Vector Search → Top 30 similar chunks
3. Re-ranking → Cohere (relevance scoring)
4. Context Assembly → File names + content
5. Response → GPT-4o-mini with streaming
```

### Key Optimizations

- **Vector Store Caching**: Reuses connections per collection
- **Connection Pooling**: psycopg_pool for database efficiency
- **Async Operations**: FastAPI async endpoints
- **Chunking Strategy**: Optimized for semantic coherence
- **Multi-stage Docker**: Reduces image size by 60%

---

## 🎨 Screenshots

*Note: Add screenshots of your application here*

---

## 🤝 Contributing

This project was developed as part of a startup internship. For inquiries or collaboration:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is proprietary and was developed for [Startup Name]. All rights reserved.

---

## 👨‍💻 Author

**[Your Name]**
- Role: Software Engineering Intern
- Duration: [Internship Period]
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]

---

## 🙏 Acknowledgments

- Built during internship at [Startup Name]
- Leverages OpenAI, Azure, and LangChain technologies
- Special thanks to the team for guidance and support

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ during my internship journey

</div>