import pickle
import tempfile

import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from utils.firebase import storage, upload_to_firestore

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
        file_data = file.getvalue()
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f"+{file.name}"
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
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Save the vectorstore to the temporary file
        with open(temp_file.name, "wb") as f:
            pickle.dump(vectorstore, f, protocol=pickle.HIGHEST_PROTOCOL)
        upload_to_firestore(persist_dir, f"{temp_file.name}")
    temp_file.close()

    return vectorstore


# @st.cache_resource
def load_vectordb(persist_dir: str):
    st.write(persist_dir)
    print("--Loading Index")
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        storage.download(persist_dir, temp_file.name)
        with open(temp_file.name, "rb") as file:
            loaded_vectordb = pickle.load(file)
        temp_file.close()

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
        for document in result["source_documents"]:
            sources.append(
                f"Retrieved answer from --> {''.join(document.metadata['source'].split('+')[1:])} at Page: {document.metadata['page']}\n\n"
            )
        return f"StudyGPT Response: {response} \n\nCited Sources:\n{' '.join(sources)}"
    else:
        return response
