# from pyexpat.errors import messages

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import pdfplumber
# from operator import itemgetter
# import streamlit as st
# from langchain_groq import ChatGroq

# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import ChatPromptTemplate

# from langchain_core.output_parsers import StrOutputParser

# api_key = "**"
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None

# if "retriever" not in st.session_state:
#     st.session_state.retriever = None

# if "file_name" not in st.session_state:
#     st.session_state.file_name = None
# st.title("Conversational RAG Chatbot")

# with st.sidebar:
#     st.title("your documents, your chatbot")
#     file=st.file_uploader("Upload your documents", type=["pdf"  ])


# if file is not None and st.session_state.file_name != file.name:
#     with pdfplumber.open(file) as pdf:
#         text = ""
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         separators=["\n\n", "\n", " ", ""]
#     )
#     chunks = text_splitter.split_text(text)

#     embedding_model = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     vectorstore = FAISS.from_texts(chunks, embedding_model)

#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={"k": 5, "fetch_k": 20}
#     )

#     st.session_state.vectorstore = vectorstore
#     st.session_state.retriever = retriever
#     st.session_state.file_name = file.name
#     st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])



#     user_question = st.chat_input("Ask a question about your PDF")
#     if user_question:
#         st.session_state.messages.append({"role": "user", "content": user_question})
#         with st.chat_message("user"):
#                 st.markdown(user_question)
#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)
    
#     def get_chat_history(messages, max_turns=6):
#         recent_messages = messages[-max_turns:]
#         history = []
#         for msg in recent_messages:
#             role = "User" if msg["role"] == "user" else "Assistant"
#             history.append(f"{role}: {msg['content']}")
#         return "\n".join(history)
#     llm = ChatGroq(
#             model="llama-3.1-8b-instant",   # or "llama-3.3-70b-versatile"
#             temperature=0,
#            api_key=api_key
#         )

#     rewrite_prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         "You are a query rewriting assistant. "
#         "Given the conversation history and the latest user question, "
#         "rewrite the latest question into a standalone question for document retrieval. "
#         "If it is already standalone, return it unchanged."
#     ),
#     (
#         "human",
#         "Chat history:\n{chat_history}\n\nLatest question:\n{question}"
#     )
#     ])
#     answer_prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         "You are a helpful assistant for answering questions about the uploaded PDF.\n"
#         "Use only the provided context to answer.\n"
#         "If the answer is not in the context, say: "
#         "'I don't know based on the uploaded document.'\n"
#         "Answer clearly and concisely."
#     ),
#     (
#         "human",
#         "Chat history:\n{chat_history}\n\n"
#         "Context:\n{context}\n\n"
#         "Question:\n{question}\n\n"
#         "Answer:"
#     )
#     ])
#     if user_question:
#         if st.session_state.retriever is None:
#             st.error("Upload a PDF first.")
#             st.stop()

#         st.session_state.messages.append({"role": "user", "content": user_question})
#         with st.chat_message("user"):
#             st.markdown(user_question)

#     chat_history = get_chat_history(st.session_state.messages[:-1])

#     standalone_question = llm.invoke(
#         rewrite_prompt.format_messages(
#             chat_history=chat_history,
#             question=user_question
#         )
#     ).content.strip()

#     docs = st.session_state.retriever.invoke(standalone_question)
#     context = format_docs(docs)

#     answer = llm.invoke(
#         answer_prompt.format_messages(
#             chat_history=chat_history,
#             context=context,
#             question=user_question
#         )
#     ).content

#     with st.chat_message("assistant"):
#         st.markdown(answer)

#     st.session_state.messages.append({"role": "assistant", "content": answer})



from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found! Please set it in your .env file.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

st.title("Conversational RAG Chatbot")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_chat_history(messages, max_turns=6):
    recent_messages = messages[-max_turns:]
    history = []
    for msg in recent_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        history.append(f"{role}: {msg['content']}")
    return "\n".join(history)

with st.sidebar:
    st.title("Your documents, your chatbot")
    file = st.file_uploader("Upload your PDF", type=["pdf"])

# Step 1: Build vectorstore only when a NEW file is uploaded
if file is not None and st.session_state.file_name != file.name:
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        st.error("No text could be extracted from this PDF.")
        st.stop()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(chunks, embedding_model)

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20}
    )

    st.session_state.vectorstore = vectorstore
    st.session_state.retriever = retriever
    st.session_state.file_name = file.name
    st.session_state.messages = []

# Step 2: Render chat history on EVERY rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Step 3: Chat input on EVERY rerun
user_question = st.chat_input("Ask a question about your PDF")

if user_question:
    if st.session_state.retriever is None:
        st.error("Upload a PDF first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=api_key
    )

    rewrite_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a query rewriting assistant. "
            "Given the conversation history and the latest user question, "
            "rewrite the latest question into a standalone question for document retrieval. "
            "If it is already standalone, return it unchanged."
        ),
        (
            "human",
            "Chat history:\n{chat_history}\n\nLatest question:\n{question}"
        )
    ])

    answer_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant for answering questions about the uploaded PDF.\n"
            "Use only the provided context to answer.\n"
            "If the answer is not in the context, say: "
            "'I don't know based on the uploaded document.'\n"
            "Answer clearly and concisely."
        ),
        (
            "human",
            "Chat history:\n{chat_history}\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
    ])

    try:
        chat_history = get_chat_history(st.session_state.messages[:-1])

        standalone_question = llm.invoke(
            rewrite_prompt.format_messages(
                chat_history=chat_history,
                question=user_question
            )
        ).content.strip()

        docs = st.session_state.retriever.invoke(standalone_question)
        context = format_docs(docs)

        answer = llm.invoke(
            answer_prompt.format_messages(
                chat_history=chat_history,
                context=context,
                question=user_question
            )
        ).content

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)