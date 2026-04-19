🏡 M3M Real Estate Chatbot (LangGraph Powered)

An intelligent real estate chatbot built using LangGraph + LLMs that helps users explore M3M properties, answer queries, and provide contextual, memory-aware responses.

🚀 Features
💬 Conversational AI chatbot for real estate queries
🧠 Memory-aware responses using LangGraph state management
📊 Handles structured + unstructured property data
🔍 Smart retrieval using RAG (Retrieval-Augmented Generation)
🏢 Focused on M3M real estate projects
⚡ FastAPI backend for scalable API handling
🔐 User session tracking & chat history
🛠️ Tech Stack
Backend: FastAPI
LLM: Gemini / OpenAI (configurable)
Framework: LangGraph
Vector DB: Pinecone / FAISS
Embeddings: Gemini / OpenAI
Frontend (optional): React
Language: Python
📂 Project Structure
m3m-chatbot/
│
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── routes/             # API routes
│   ├── services/           # LLM + LangGraph logic
│   ├── models/             # Data models
│   ├── utils/              # Helper functions
│   └── config/             # Config files
│
├── data/                   # Property documents
├── vectorstore/            # Vector DB setup
├── graph/                  # LangGraph workflow
│   └── graph_builder.py
│
├── requirements.txt
├── .env
└── README.md
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/m3m-chatbot.git
cd m3m-chatbot
2️⃣ Create virtual environment
python -m venv venv
3️⃣ Activate environment

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
4️⃣ Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in root:

OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_ENV=your_env
▶️ Running the Project
Start FastAPI server
uvicorn app.main:app --reload

Server will run at:

http://127.0.0.1:8000

Swagger Docs:

http://127.0.0.1:8000/docs
🧠 LangGraph Workflow

The chatbot is powered by a LangGraph state machine:

Flow:

User Query → Retrieve Context → LLM → Response → Memory Update
Nodes:
input_node
retriever_node
llm_node
memory_node
response_node
🔍 API Endpoints
1. Chat Query
POST /api/chat

Request Body

{
  "user_id": "123",
  "query": "Show me M3M projects in Gurgaon"
}

Response

{
  "response": "Here are some M3M projects in Gurgaon..."
}
2. Upload Property Data
POST /api/upload
3. Get Chat History
GET /api/history/{user_id}
📊 Data Handling
Documents are chunked and embedded
Stored in vector DB with metadata:
project_name
location
price
amenities
🧪 Testing

Run tests:

pytest
🧩 Example Queries
“2 BHK in Gurgaon under 1.5 Cr”
“M3M projects near Dwarka Expressway”
“Amenities in M3M Golf Estate”
“Compare M3M vs DLF properties”
🛡️ Future Improvements
🔊 Voice-based interaction
📱 Mobile app integration
🧠 Better personalization using long-term memory
📍 Map-based property suggestions
💰 Price prediction models
🤝 Contributing
Fork the repo
Create a new branch
Commit changes
Push & open PR
📄 License

MIT License

👨‍💻 Author

Rishabh
Backend Developer | AI Enthusiast

⭐ Support

If you like this project, give it a ⭐ on GitHub!
