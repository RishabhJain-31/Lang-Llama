import os
import re
from typing import TypedDict
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from MESSAGE import send_lead 

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
chroma_db = Chroma(persist_directory="./chromadb", embedding_function=embedding_model)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)

# State
class GraphState(TypedDict):
    query: str
    retrieved_docs: list[str]
    response: str
    history: list[str]
    summary: str
    lead_name: str | None  # Name of the lead
    lead_phone: str | None  # Phone number of the lead
    lead_sent: bool  # Whether lead has been sent
    # awaiting: bool # Track lead flow state


# def query_enrichment(state: GraphState) -> str:
#     user_query = state['query'].strip()
#     if len(user_query.split()) <= 3:
#         recent = state.get("history", [])[-4:]
#         context = "\n".join([msg for msg in recent if isinstance(msg, str)])
#         return f"{context}\nUser: {user_query}"
#     return user_query

def query_enrichment(state: GraphState)-> str:
    query=state['query'].strip()
    history="\n".join(i for i in state.get("history",[])[-4:] if isinstance(i, str))
    
    prompt = f"""You are an assistant that rewrites user queries for real estate search.
If the query is vague or short, expand it using context relevantly.Focus more on recent query only if needed then add the previous history queries to it.
Also if the query is short ,go for follow up question for more specificity.
Context (chat history):
{history}
User Query:
{query}

Rewrite it as a complete and clear search query:"""
    enriched=llm([HumanMessage(content=prompt)]).content.strip()
    return enriched
# Duplicate Query Detection
def is_duplicate_query(state: GraphState) -> bool:
    recent_queries = [
    msg for msg in state.get("history", []) if isinstance(msg, str) and msg.startswith("User: ")
]
    last_queries = [q.replace("User: ", "") for q in recent_queries[-5:]]
    return state["query"].strip().lower() in [q.strip().lower() for q in last_queries]

def retrieve(state: GraphState) -> GraphState:
    if is_duplicate_query(state):
        print("🔁 Skipping duplicate query")
        return state  # or return same docs again without re-fetching
    # query enrichment, enhance 
    enriched_query = query_enrichment(state)
    print(f"🔍 Searching for: {enriched_query}")
    docs=chroma_db.similarity_search(enriched_query, k=5 )
    # ✅ Optional: Deduplication by metadata ID
    shown_ids = set()
    for msg in state.get("history", []):
        if isinstance(msg, str) and "metadata" in msg:           #Check if msg is a string and contains metadata
            match = re.search(r'"id":\s*"(.+?)"', msg)         # Extract ID from metadata
            if match:
                shown_ids.add(match.group(1))                  #sh

    filtered_docs = []
    for doc in docs:
        doc_id=doc.metadata.get("id")
        if doc_id not in shown_ids:                         #if the id is not in shown_ids then append the doc otherwise not
            filtered_docs.append(doc)
        if len(filtered_docs) >= 5:
            break

    # query boosting, create multiple variations of the query
    # de-duplicate documents
    # top 5 documents based on similarity search score OR
    # re-ranking to select top 5 - optional

    # Extract keywords from user query (split by space, remove common stopwords)
    # query = state['query'].lower()
    # keywords = [w for w in re.findall(r'\w+', query) if w not in {'i', 'am', 'for', 'in', 'the', 'a', 'an', 'is', 'are', 'me', 'show', 'want', 'with', 'to', 'of', 'and', 'or', 'on', 'at', 'by', 'my', 'please', 'can', 'you', 'find', 'give', 'need', 'looking', 'like', 'any', 'near', 'project', 'group', 'bhk', 'apartment', 'apartments'}]

    # Find docs that match any keyword (location, amenities, price, etc.)
    # relevant_docs = []
    # for doc in docs:
    #     content = doc.page_content.lower()
    #     if any(k in content for k in keywords):
    #         relevant_docs.append(doc)

    # If relevant docs found, use them; else fallback to similarity search
    # if relevant_docs:
    #     result_docs = relevant_docs[:4]
    # else:
    #     result_docs = docs[:4]

    return {**state, "retrieved_docs": [doc.page_content for doc in filtered_docs]}


# Node: Generate
def LLM(state: GraphState) -> GraphState:
    query= state['query'].strip()
    prompt = f"""You are a smart real estate assistant for the company m3m.
    Rules:
    - Only use the information from the retrieved documents.
    - Understand and respond to queries in both Hindi and English and HINGLISH also. (हिंदी और अंग्रेज़ी दोनों में समझें और जवाब दें)
    - Keep the appropriate spaces between your output, not too much, not too less.
    - NEVER guess. Say “I'm not sure” if no relevant info is found.
    -DON'T HALLUCINATE. GIVE THE PROPER RELEVANT ANSWER FOR THE QUERY 
    - Do not repeat the same project unless the user asks again.
    - Avoid repeating project names already discussed.
    - For short queries like "yes", "no", "ok", continue the conversation politely.
    - If user says just "3bhk" or anything like that then ask: "Which location or project are you referring to?"
    - If user asks for image/link, use fields in metadata or page content.
    - If user provides phone number, acknowledge it briefly but don't ask again.
    - You can use emojis to make the conversation more engaging.
    - Ask for phone number if you observe the user is interested.
    - Do not repeat the response once produced for a user until they demand.
    -Learn from the conversation and adapt your responses.
    - If info about the requested location is not found, suggest similar nearby locations.
    - Do not say "I’m not sure" unless absolutely no information is available.

    When you done with the follow ups and have clear understanding what user wants then Use this formatting:
    - Project Name as heading (###)
    - Ask for more details if needed.
    - Always follow the assistant rules.
    For example-
        I am looking for 3
        hk in Bangalore.
        Sure! Which project or location are you referring to? Here are some options:    
        I am looking for 3bhk in Prestige Group.
        Here are the details for 3bhk in Prestige Group:
    example 2-
        I am looking for 3bhk in Bangalore.
        Can you mention your budget?
        This is how you can answer on your own way 

    example 3-
         i want 5 bhk under 10 crore
         Sure! Here are some options for 5 BHK properties under 10 crore in Bangalore:
         I'm Interested 
         That's nice to hear! Can you please share your name, phone number, and preferred time for a call or site visit?
    - Respond in a friendly and helpful manner.
    - Well structured response with proper formatting.
    - Easily readable and understandable.
    -If you feel that user is interested in a project, ask for their name, phone number and preferred time for call or site visit.
    Use this formatting for each project:

    🏢 **Project Name**
    📍 **Location:** location of that project
    🛏️ **BHK Options:** 2 BHK, 3 BHK (etc.)
    💰 **Price:** 
            • 2 BHK – ₹ X Cr Size in sq ft or sq yard
            • 3 BHK – ₹ Y Cr Size in sq ft or sq yard
    ⭐ **Amenities:** amenity1, amenity2
    🔗 **Link:** [Click Here](project_link)
    🖼️ **Image:** (just paste the image in medium appropriate size)

    If the user seems interested, you MUST collect the following details:
- Name and Phone number (Indian 10-digit only) in one pass or in one message ensure.
- Preferred time for call or site visit

Once you collect all 3, summarize them clearly like this at the end:
---
Lead Info
👤 Name: NAME
📞 Phone: NUMBER
⏰ Time: TIME
---

Only ask for missing details one by one.
Once all are collected, say: "✅ I've shared your details with the team!"

---

Conversation Summary
  {state.get('summary', "")}

User Query:
{state['query']}

Retrieved Docs:
{state['retrieved_docs']}
"""
    result = llm.invoke([
        SystemMessage(content="Always follow assistant rules."),
        HumanMessage(content=prompt)
    ]).content.strip()

    # Extract name & phone via LLM
        # Extract name & phone via LLM
    
    # Detect phone number
    phone_match = re.search(r"\b[6-9]\d{9}\b", query)
    phone = phone_match.group(0) if phone_match else state.get("lead_phone")

    # Detect name (naive approach for now)
    name_match = re.search(r"\b(?:my name is|i am|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", query, re.IGNORECASE)
    name = name_match.group(1).strip() if name_match else state.get("lead_name")

    if name:
        print(f"✅ Name captured: {name}")
    else:
        print("❌ No name found")

    if phone:
        print(f"✅ Phone captured: {phone}")
    else:
        print("❌ No phone found")

    if name and phone and not state.get("lead_sent"):
        print(f"📤 Sending lead to WhatsApp: {name}, {phone}")
        send_lead(name, phone)
        return {**state, "response": result, "lead_name": name, "lead_phone": phone, "lead_sent": True}

    return {**state, "response": result, "lead_name": name, "lead_phone": phone, "lead_sent": state.get("lead_sent", False)}



# Node: Summarize
def summarize(state: GraphState) -> GraphState:
    summary_prompt = f"""
Previous Summary:
{state.get('summary', "")}

User asked:
{state['query']}

Bot replied:
{state['response']}

Update the summary in 2 lines:
Focus more on latest user query and bot response.
Make it concise and relevant to the conversation.
"""
    summary = llm([HumanMessage(content=summary_prompt)]).content.strip()
    history = (state.get("history") or []) + [f"User: {state['query']}", f"Bot: {state['response']}"]
    
    updated_state = {**state, "summary": summary, "history": history}   
    # updated_state = handle_lead_capture(updated_state)

    return updated_state


# Graph Build
builder = StateGraph(GraphState)
builder.add_node("retrieve", retrieve)
builder.add_node("LLM", LLM)
builder.add_node("summarize", summarize)
builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "LLM")
builder.add_edge("LLM", "summarize")
builder.set_finish_point("summarize")
app = builder.compile()
app.name="M3M AGENT"


# todo: check max token limit
