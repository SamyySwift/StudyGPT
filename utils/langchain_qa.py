import glob
import os

import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


class questionAnswer:
    def __init__(self, key) -> None:
        self.key = key
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.key)
        self.files = os.listdir("docs")
        self.texts = ""

    def load_and_split_doc(self):
        # Load documents
        loaders = []

        for file in self.files:
            if file.endswith(".pdf"):
                loaders.append(PyPDFLoader(file))
            elif file.endswith(".txt"):
                loaders.append(TextLoader(file))

        # Extract documnt contents
        docs = []
        for loader in loaders:
            docs.extend(loader.load())

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.texts = text_splitter.split_documents(docs)

    def create_vectordb(self, persist_dir):
        self.load_and_split_doc()
        vectordb = Chroma.from_documents(
            self.texts, self.embeddings, persist_directory=persist_dir
        )

        vectordb.persist()
        return vectordb

    def load_vectordb(self, persist_dir):
        loaded_vectordb = Chroma(
            persist_directory=persist_dir, embedding_function=self.embeddings
        )

        return loaded_vectordb

    def query(self, query, vectordb, source=False):
        sources = []
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=self.key),
            chain_type="stuff",
            retriever=vectordb.as_retriever(),
            return_source_documents=source,
        )
        result = qa({"query": query})

        response = result["result"]

        if source:
            for document in result["source_documents"]:
                sources.append(
                    f"Retrievd the info from {document.metadata['source']} at Page:{document.metadata['page']}"
                )
            return f"{response} \n\nCited Sources:\n{' '.join(sources)}"
        else:
            return response
