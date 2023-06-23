import pickle
import tempfile

import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from utils.firebase import upload_to_firestore, download_from_firestore

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


# class questionAnswer:
#     def __init__(self) -> None:
#         # key = key
#         embeddings = OpenAIEmbeddings()
#         llm = OpenAI()
#         files = os.listdir("docs")
#         texts = ""


llm = OpenAI()
embeddings = OpenAIEmbeddings()


def load_and_split_doc(pdf_files):
    loaders = []

    for file in pdf_files:
        if file.name.endswith(".pdf"):
            file_data = file.read()
            with open(f"{file.name}", "wb") as f:
                f.write(file_data)
            loaders.append(PyPDFLoader(file.name))
        elif file.name.endswith(".txt"):
            file_data = file.read()
            with open(f"{file.name}", "w") as f:
                f.write(file_data.decode("utf-8"))
            loaders.append(TextLoader(file.name))

    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    return chunks


def index_cam_input(fname):
    loader = TextLoader(f"{fname}.txt")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def create_vectordb(persist_dir: str, files):
    print("--Creating Index")
    text_chunks = load_and_split_doc(files)
    vectorstore = FAISS.from_documents(text_chunks, embeddings)
    with open(f"{persist_dir}.pkl", "wb") as f:
        pickle.dump(vectorstore, f, protocol=pickle.HIGHEST_PROTOCOL)
    upload_to_firestore(f"{persist_dir}_index.pkl", f"{persist_dir}.pkl")

    return vectorstore


# @st.cache_resource
def load_vectordb(persist_dir: str):
    print("--Loading Index")
    try:
        download_from_firestore(f"{persist_dir}_index.pkl", f"{persist_dir}.pkl")
        with open(f"{persist_dir}.pkl", "rb") as file:
            loaded_vectordb = pickle.load(file)

        return loaded_vectordb
    except AttributeError:
        st.error("Error Downloading Index")


def query(query, vectordb, source=False):
    sources = []

    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            input_key="question",
            output_key="answer",
            memory_key="chat_history",
            return_messages=True,
        )
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=st.session_state.memory,
        retriever=vectordb.as_retriever(),
        return_source_documents=source,
    )

    result = qa({"question": query})
    response = result["answer"]

    if source:
        for document in result["source_documents"][:1]:
            sources.append(
                f"Retrieved answer from ==> {document.metadata['source']} at Page: {document.metadata['page']}<br>"
            )
        return f"{response} <br><br>Cited Sources:<br>{' '.join(sources)}"

    else:
        return response
