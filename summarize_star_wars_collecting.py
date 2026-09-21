#!/usr/bin/env python3

import os
import sys
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# 1. Data Not in git for copyright reasons...
FOLDER_PATH = "./data"

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

query_text = sys.argv[1]
docs = vector_store.similarity_search(
    query=query_text,
    k=3
)
input_text = f"summarize the following text to answer the question '{query_text}' : {docs[0].page_content}"
for doc in docs:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}\n---")


model_name = "google-t5/t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tokenize and generate summary
inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
outputs = model.generate(
    inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4
)

# Decode and print result
summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"\n---\nquery:\n{query_text}\n")
print("\n---\nSummary:\n")
print(summary)

