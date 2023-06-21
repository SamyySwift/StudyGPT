import os

import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, FAISS
import pickle

from utils.firebase import upload_to_firestore, storage
import tempfile


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


# class questionAnswer:
#     def __init__(self) -> None:
#         # key = key
#         embeddings = OpenAIEmbeddings()
#         llm = OpenAI()
#         files = os.listdir("docs")
#         texts = ""

# files = storage.bucket.list_blobs(prefix="Documents/")

llm = OpenAI()
embeddings = OpenAIEmbeddings()


if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        input_key="question",
        output_key="answer",
        memory_key="chat_history",
        return_messages=True,
    )


def load_and_split_doc(pdf_files):
    loaders = []

    for file in pdf_files:
        file_data = file.getvalue()
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f"{file.name}"
        ) as temp_file:
            temp_file.write(file_data)

        loaders.append(PyPDFLoader(temp_file.name))
        temp_file.close()

    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    return chunks


def create_vectordb(persist_dir: str, files):
    print("--Creating Index")
    text_chunks = load_and_split_doc(files)

    vectorstore = FAISS.from_documents(text_chunks, embeddings)
    with open(f"{persist_dir}.pkl", "wb") as f:
        pickle.dump(vectorstore, f, protocol=pickle.HIGHEST_PROTOCOL)

    upload_to_firestore(persist_dir, f"{persist_dir}.pkl")
    os.remove(f"{persist_dir}.pkl")
    return vectorstore


def load_vectordb(persist_dir: str):
    print("--Loading Index")
    # loaded_vectordb = Chroma(
    #     persist_directory=persist_dir, embedding_function=embeddings
    # )
    storage.download(persist_dir, f"{persist_dir}.pkl")
    print("Done Downloading")

    with open(f"{persist_dir}.pkl", "rb") as file:
        loaded_vectordb = pickle.load(file)

    return loaded_vectordb


def query(query, vectordb, source=False):
    sources = []
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=st.session_state.memory,
        retriever=vectordb.as_retriever(),
        return_source_documents=source,
    )

    result = qa({"question": query})
    response = result["answer"]

    if source:
        for document in result["source_documents"]:
            sources.append(
                f"Retrieved answers from {document.metadata['source']} at Page:{document.metadata['page']}\n"
            )
        return f"StudyGPT Response: {response} \n\nCited Sources:\n{' '.join(sources)}"
    else:
        return response
