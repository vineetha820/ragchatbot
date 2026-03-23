"# RAG Chatbot

A conversational AI chatbot powered by **Retrieval-Augmented Generation (RAG)** that allows users to upload PDF documents and ask questions about their content. The chatbot uses advanced LLMs and semantic search to provide accurate, context-aware answers.

## 🚀 Features

- **PDF Document Upload**: Upload and process PDF files with text extraction
- **Semantic Search**: Uses FAISS vector store with HuggingFace embeddings for intelligent document retrieval
- **Conversational AI**: Powered by LLama 3.1 (via Groq API) for generating natural responses
- **Query Rewriting**: Automatically rewrites user questions to standalone queries for better retrieval
- **Chat History Management**: Maintains conversation context across multiple turns
- **Maximum Marginal Relevance (MMR)**: Uses MMR search strategy to diversify retrieved documents
- **User-Friendly Interface**: Built with Streamlit for an intuitive web-based UI

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **LLM**: LLama 3.1-8b-instant (via Groq API)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS
- **PDF Processing**: pdfplumber
- **LLM Framework**: LangChain
- **Environment Management**: python-dotenv

## 📋 Requirements

All dependencies are listed in `requirement.txt`:

```
streamlit
pdfplumber
langchain
langchain-core
langchain-community
langchain-text-splitters
langchain-groq
faiss-cpu
python-dotenv
```

## ⚙️ Installation

1. **Clone or download the project:**
   ```bash
   cd ragchatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

3. **Set up environment variables:**
   Copy `.env.example` to `.env` and add your Groq API key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## � Configuration

### Environment Variables

This project uses environment variables to securely manage API keys:

1. **Create a `.env` file** in the project root:
   ```bash
   GROQ_API_KEY=your_actual_api_key_here
   ```

2. **Never commit `.env` to GitHub!** The `.gitignore` file already excludes it.

3. For template reference, see `.env.example` (safe to commit)

### Getting Your API Key

1. Sign up at [Groq Console](https://console.groq.com)
2. Generate a new API key
3. Add it to your `.env` file

## �🚀 Usage

To run the application:

```bash
streamlit run ragchatbot.py
```

The app will open in your default browser at `http://localhost:8501`

### How to Use:

1. **Upload a PDF**: Use the sidebar to upload a PDF document
2. **Ask Questions**: Type your questions about the document in the chat input
3. **Get Answers**: The chatbot will retrieve relevant sections and generate answers
4. **Continue Conversation**: Ask follow-up questions to maintain context

## 🔍 How It Works

### RAG Pipeline:

1. **Document Processing**:
   - PDF text is extracted using pdfplumber
   - Text is split into chunks (1000 tokens with 200 token overlap)

2. **Vector Embedding**:
   - Text chunks are converted to embeddings using HuggingFace's all-MiniLM-L6-v2 model
   - Embeddings are stored in a FAISS vector store for fast retrieval

3. **Query Processing**:
   - User queries are rewritten to standalone questions for better retrieval
   - The system performs MMR search to find relevant documents

4. **Response Generation**:
   - Retrieved documents are formatted and sent to the LLM
   - LLama 3.1 generates contextual answers based on the retrieved information
   - Conversation history is maintained for coherent multi-turn dialogue

## � Advanced Configuration

Key parameters in `ragchatbot.py`:

- **Chunk Size**: 1000 tokens (adjustable in `RecursiveCharacterTextSplitter`)
- **Chunk Overlap**: 200 tokens
- **MMR Search**: retrieves top 5 most relevant chunks with fetch_k=20
- **LLM Model**: llama-3.1-8b-instant
- **Temperature**: 0 (deterministic responses)

## 🐛 Troubleshooting

- **API Key Error**: Ensure your Groq API key is valid and properly set
- **Out of Memory**: Reduce chunk size or use fewer documents
- **Slow Responses**: This is normal for the first query; embeddings are cached after

## 🎯 Future Enhancements

- Support for multiple document formats (DOCX, TXT, etc.)
- Web search integration for extended knowledge
- Fine-tuned models for specific domains
- Multi-language support
- Document summarization feature
- Export conversation history

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a learning project for RAG-based chatbot development.

---

**Happy chatting! 🤖💬**" 
