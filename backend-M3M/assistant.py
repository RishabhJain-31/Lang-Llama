import os
import json
import re
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Lazy-load embedding model and ChromaDB
_embedding_model = None
_chroma_db = None
_llm = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        # Use a smaller model if needed: "paraphrase-MiniLM-L3-v2"
        _embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embedding_model

def get_chroma_db():
    global _chroma_db
    if _chroma_db is None:
        from langchain_community.vectorstores import Chroma
        _chroma_db = Chroma(persist_directory="./chroma_filtered", embedding_function=get_embedding_model())
    return _chroma_db

def get_llm():
    global _llm
    if _llm is None:
        from langchain_groq import ChatGroq
        _llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0, groq_api_key=GROQ_API_KEY)
    return _llm


# State definition
class GraphState(TypedDict):
    query: str
    retrieved_docs: list[str]
    response: str
    history: list[str]
    summary: str
    filters: dict


# ── Node 1: Extract filters from user query ──
def extract_filters(state: GraphState) -> GraphState:
    query = state["query"]
    history = "\n".join(state.get("history", [])[-4:])

    prompt = f"""Extract metadata filters from this real estate query.
Return ONLY valid JSON with these optional keys: "bhk", "location", "min_price_cr", "max_price_cr", "status".
- "bhk" should be a float like 3.0 or 4.0
- "min_price_cr" / "max_price_cr" should be numbers in crores
- "location" should be a city or area name
- "status" should be "ongoing" or "completed"
Only include keys you can confidently extract. If nothing is extractable, return {{}}.

Chat history:
{history}

User query: {query}
"""
    raw = get_llm().invoke([HumanMessage(content=prompt)]).content.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```", "", raw)
    try:
        filters = json.loads(raw)
    except json.JSONDecodeError:
        filters = {}
    return {**state, "filters": filters}


# ── Node 2: Retrieve from ChromaDB ──
def retrieve(state: GraphState) -> GraphState:
    query = state["query"].strip()
    history = "\n".join(state.get("history", [])[-4:])
    filters = state.get("filters", {})

    # Enrich the query using history for better semantic search
    enrich_prompt = f"""Rewrite this user query into a clear, detailed real estate search query in 1-2 sentences.
Use the chat history for context if the query is vague (like "yes", "ok", "tell me more").

Chat history:
{history}

User query: {query}

Return ONLY the rewritten query, nothing else."""

    enriched_query = get_llm().invoke([HumanMessage(content=enrich_prompt)]).content.strip()
    print(f"🔍 Enriched query: {enriched_query}")

    # Build ChromaDB where filter from extracted filters
    chroma_db = get_chroma_db()
    where_filter = {}
    if "location" in filters:
        where_filter["location"] = filters["location"]
    if "status" in filters:
        where_filter["status"] = filters["status"]

    try:
        if where_filter:
            docs = chroma_db.similarity_search(enriched_query, k=10, filter=where_filter)
        else:
            docs = chroma_db.similarity_search(enriched_query, k=10)
    except Exception as e:
        print(f"⚠️ Filtered search failed ({e}), falling back to unfiltered search")
        docs = chroma_db.similarity_search(enriched_query, k=10)

    print(f"📄 Retrieved {len(docs)} documents")
    return {**state, "retrieved_docs": [doc.page_content for doc in docs]}


# ── Node 3: Generate response with LLM ──
def generate(state: GraphState) -> GraphState:
    query = state["query"].strip()
    history = "\n".join(state.get("history", [])[-6:])
    retrieved = "\n---\n".join(state.get("retrieved_docs", []))

    prompt = f"""You are a smart, friendly real estate assistant for the company M3M.

RULES:
- Only use the information from the retrieved documents below.
- Understand and respond in English.
- DON'T HALLUCINATE. Only give answers based on retrieved data.
- Avoid repeating project names already discussed in history.
- For short queries like "yes", "no", "ok", continue the conversation politely.
- If user says just "3bhk" or similar, ask: "Which location or project are you referring to?"
- If info about the requested location is not found, suggest similar nearby locations from the data.
- Do not say "I'm not sure" unless absolutely no information is available.
- Use emojis to make the conversation engaging.
- Ask for phone number if the user seems interested.
- Keep proper spacing and formatting in your output.

When you have enough info about what the user wants, format each project like this:

🏢 Project Name
📍Location:location
🛏️ BHK Options:2 BHK, 3 BHK, etc.
💰 Price Range:₹X Cr – ₹Y Cr
⭐ Amenities:** amenity1, amenity2
🖼️ Image : Show the actual image in the chat to the user properly by rendering it properly.

Always include a plain image URL (no markdown) for each property.
If the user seems interested, collect these details ONE BY ONE:
1. Name
2. Phone number (Indian 10-digit)
3. Preferred time for call or site visit

Once all 3 are collected, summarize like:
---
👤 Name: NAME
📞 Phone: NUMBER
⏰ Preferred Time: TIME
---
Then say: "✅ I've shared your details with the team!"

---

Conversation History:
{history}

Retrieved Documents:
{retrieved}

User Query: {query}
"""

    result = get_llm().invoke([
        SystemMessage(content="You are M3M's real estate assistant. Always follow the rules above."),
        HumanMessage(content=prompt)
    ]).content.strip()

    return {**state, "response": result}


# ── Node 4: Update history ──
def update_history(state: GraphState) -> GraphState:
    history = list(state.get("history") or [])
    history.append(f"User: {state['query']}")
    history.append(f"Bot: {state['response']}")
    # Keep last 20 exchanges to avoid token overflow
    history = history[-20:]

    summary = f"Last topic: {state['query']}"
    return {**state, "history": history, "summary": summary}


# ── Build the Graph ──
builder = StateGraph(GraphState)
builder.add_node("extract_filters", extract_filters)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("update_history", update_history)

builder.set_entry_point("extract_filters")
builder.add_edge("extract_filters", "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "update_history")
builder.set_finish_point("update_history")

app = builder.compile()
app.name = "M3M AGENT"