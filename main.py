# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from assistant import app as assistant_app  # your existing LangGraph app
# from fastapi import FastAPI
# import json


# app = FastAPI()

# # For HTML and static files
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# # Initial state
# chat_state = {
#     "query": "",
#     "retrieved_docs": [],
#     "response": "",
#     "history": [],
#     "summary": "",
#     # "awaiting": False  # Track if we're in lead flow
#     }

# # Serve ChatGPT-like HTML frontend
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# #@app.post("/chat")
# async def chat_route(request: Request):
#     body=await request.json()
#     user_input=body.get("message")
#     state = {
#         "query": user_input,
#         "retrieved_docs": [],
#         "response": "",
#         "history":  chat_state.get("history", []),
#         "summary": chat_state.get("summary", ""),
#     }
#     state= assistant_app.invoke(state)
#     chat_state["history"] = state.get("history", [])
#     chat_state["summary"] = state.get("summary", "")


#     return {"response": state["response"]}
# # class Lead(BaseModel):
# #     name: str
# #     phone: str
# #     preferred_time: str

# # @app.post("/save_lead")
# # async def save_lead(lead: Lead):
# #     print("🔥 /save_lead endpoint hit!")
# #     try:
# #         print("📥 Incoming Lead:", lead.dict())
# #     except Exception as e:
# #         print("❌ Error parsing lead:", e)

# #     lead_entry = {
# #         "name": lead.name,
# #         "phone": lead.phone,
# #         "preferred_time": lead.preferred_time,
# #         "timestamp": datetime.now().isoformat()
# #     }

# #     try:
# #         with open("leads.json", "r") as f:
# #             leads = json.load(f)
# #         print("✅ leads.json loaded")
# #     except FileNotFoundError:
# #         print("⚠️ leads.json not found, creating new one")
# #         leads = []
# #     except Exception as e:
# #         print("❌ Error reading leads.json:", e)
# #         leads = []

# #     leads.append(lead_entry)

# #     try:
# #         with open("leads.json", "w") as f:
# #             json.dump(leads, f, indent=4)
# #         print("✅ Lead written successfully:", lead_entry)
# #     except Exception as e:
# #         print("❌ Error writing leads.json:", e)

# #     return {"message": "Lead saved successfully!"}


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from assistant import app as assistant_app  # LangGraph assistant

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Persistent conversation state (in-memory)
chat_state = {
    "query": "",
    "retrieved_docs": [],
    "response": "",
    "history": [],
    "summary": ""
}

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle chat
@app.post("/chat")
async def chat_route(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")

        if not user_input:
            return {"reply": "❌ No input provided."}

        # Construct LangGraph state
        state = {
            "query": user_input,
            "retrieved_docs": [],
            "response": "",
            "history": chat_state.get("history", []),
            "summary": chat_state.get("summary", "")
        }

        # Run LangGraph
        state = assistant_app.invoke(state)

        # Update memory
        chat_state["history"] = state.get("history", [])
        chat_state["summary"] = state.get("summary", "")

        return {"reply": state["response"]}
    
    except Exception as e:
        print("❌ Error in /chat route:", e)
        return {"reply": f"❌ Server error: {str(e)}"}
