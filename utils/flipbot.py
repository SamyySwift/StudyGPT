import os

import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


# class questionAnswer:
#     def __init__(self) -> None:
#         # key = key
#         embeddings = OpenAIEmbeddings()
#         llm = OpenAI()
#         files = os.listdir("docs")
#         texts = ""

files = os.listdir("docs")
llm = OpenAI()
embeddings = OpenAIEmbeddings()


if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        input_key="question",
        output_key="answer",
        memory_key="chat_history",
        return_messages=True,
    )


def load_and_split_doc(scan=False):
    if scan:
        loader = DirectoryLoader("docs")
        docs = loader.load()
        return docs
    else:
        # Load documents
        loaders = []
        for file in files:
            # if file.endswith(".pdf"):
            loaders.append(PyPDFLoader(file))

        # Extract documnt contents
        documents = []
        for loader in loaders:
            documents.extend(loader.load())

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        texts = text_splitter.split_documents(documents)

        return texts


def create_vectordb(persist_dir: str, scan: bool):
    print("--Creating Index")
    texts = load_and_split_doc(scan)

    vectorstore = Chroma.from_documents(
        texts, embeddings, persist_directory=persist_dir
    )
    vectorstore.persist()
    return vectorstore


@st.cache_resource
def load_vectordb(persist_dir: str):
    print("--Loading Index")
    loaded_vectordb = Chroma(
        persist_directory=persist_dir, embedding_function=embeddings
    )

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
