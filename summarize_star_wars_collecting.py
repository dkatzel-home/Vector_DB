#!/usr/bin/env python3

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from chromadb.utils import embedding_functions

# 1. Define your folder path and setup OpenAI API Key
FOLDER_PATH = "./data/Read_Five_Book"

# 2. Load all .md files from the directory
# TextLoader is used under the hood to ensure proper text parsing
loader = DirectoryLoader(FOLDER_PATH, glob="**/*.md", loader_cls=TextLoader)
documents = loader.load()

# 3. Split the markdown text
# Optional but highly recommended: Split by Markdown headings to keep context intact
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# Further split large chunks into smaller chunks for optimal embedding size
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

final_docs = []
for doc in documents:
    # Split by markdown headers first
    header_splits = markdown_splitter.split_text(doc.page_content)
    # Further split by characters if a section is too long
    chunks = text_splitter.split_documents(header_splits)
    
    # Preserve original source metadata
    for chunk in chunks:
        chunk.metadata["source"] = doc.metadata.get("source")
        final_docs.append(chunk)

# 4. Initialize ChromaDB and embed the documents
# This creates a local directory named 'chroma_db' to persist your data
vector_store = Chroma.from_documents(
    collection_name="star_wars_summaries",
    documents=final_docs,
    persist_directory="./chroma_db"
)

print(f"Successfully loaded {len(final_docs)} chunks into ChromaDB.")

query_text = "What year was the Early Bird Certificate in stores?"
docs = vector_store.similarity_search(
    query=query_text,
    k=2
)

for doc in docs:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}\n---")
