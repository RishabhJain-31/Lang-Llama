import os, json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

docs = []

for item in data:
    text = f"""
Project: {item['name']}
Location: {item.get('location')}
Status: {item.get('status')}
Price Range: {item.get('price')}
Address: {item.get('address')}
Link: {item.get('link')}
Image: {item.get('image')}
Description: {item.get('description')}
Amenities: {", ".join(item.get("amenities", []))}

Configurations:
"""
    for config in item.get("configurations", []):
        text += f"\n  - {config['type']}"
        for v in config["variants"]:
            text += f"\n    Area: {v['area']}, Price: {v['price']}"

    docs.append(Document(page_content=text.strip()))

# Chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# Embed
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
vectordb = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma")
vectordb.persist()

print("✅ Embeddings stored.")
