# 1_process_and_embed.py
# This script reads data.json, processes it to create clean metadata,
# chunks the content, and stores it in a Chroma vector database.

import os
import json
import re
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
import shutil

print("--- Starting Data Processing and Embedding ---")

# --- Setup ---
load_dotenv()


with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        print(f"📄 Loaded {len(data)} properties from data.json")

# --- Helper Functions ---
def parse_price(price_str):
    """A helper function to extract a numerical price in Crores."""
    if not isinstance(price_str, str):
        return None
    numbers = re.findall(r'[\d\.]+', price_str)
    if not numbers:
        return None
    price = float(numbers[0])
    if "L" in price_str.upper() and "CR" not in price_str.upper():
         return price / 100 # Convert Lakhs to Crores
    return price

# --- Main Processing Loop ---
docs = []
for entry in data:
    bhk_options = []
    min_price_cr = float('inf')
    max_price_cr = float('-inf')

    # Process configurations to get BHK options and price range
    for config in entry.get("configurations", []):
        bhk_str = config.get("type", "")
        bhk_num_match = re.findall(r'[\d\.]+', bhk_str)
        if bhk_num_match:
            bhk_options.append(float(bhk_num_match[0]))
        
        for variant in config.get("variants", []):
            price = parse_price(variant.get("price"))
            if price:
                if price < min_price_cr: min_price_cr = price
                if price > max_price_cr: max_price_cr = price

    # Clean up values
    if min_price_cr == float('inf'): min_price_cr = None
    if max_price_cr == float('-inf'): max_price_cr = None

    # This is the new, clean metadata for filtering
    metadata = {
        "name": entry.get("name", ""),
        "location": entry.get("location", ""),
        "status": entry.get("status", ""),
        "link": entry.get("link", ""),
        "image": entry.get("image", ""),
        "min_price_cr": min_price_cr,
        "max_price_cr": max_price_cr,
        # FIX: Convert the list of BHKs to a comma-separated string for ChromaDB
        "bhk_options": ", ".join(map(str, sorted(list(set(bhk_options))))),
    }
    
    # Create the text content for semantic search
    page_content = f"""
    Property Name: {entry.get('name')}.
    Location: {entry.get('location')}.
    Status: {entry.get('status')}.
    Price Range: {entry.get('price')}.
    Description: {entry.get('description')}.
    Amenities: {', '.join(entry.get('amenities',[]))}.
    Link: {entry.get('link')}
    Image: ![Image]({entry.get('image')})
    """
    
    docs.append(Document(page_content=page_content.strip(), metadata=metadata))

print(f"✅ Processed {len(docs)} documents with structured metadata.")

# --- Chunking and Embedding ---
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- Create a new, clean database ---
db_directory = "./chroma_filtered"
if os.path.exists(db_directory):
    print(f"🗑️ Deleting old database directory: {db_directory}")
    shutil.rmtree(db_directory)

print(f"🧠 Creating new embeddings and storing in ChromaDB at {db_directory}...")
vectordb = Chroma.from_documents(
    documents=chunks, 
    embedding=embedding_model, 
    persist_directory=db_directory
)
vectordb.persist()

print(f"✅ Success! Fresh, filterable database created at '{db_directory}'")