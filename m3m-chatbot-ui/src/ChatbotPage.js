import React, { useState, useEffect, useRef } from "react";
import { 
  MessageSquare, 
  Plus, 
  Settings, 
  User, 
  Send, 
  Bot, 
  MoreHorizontal, 
  PanelLeftClose, 
  PanelLeftOpen,
  LogOut,
  Paperclip
} from "lucide-react";
import { Link } from "react-router-dom";

function ChatbotPage() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Welcome to M3M Properties Assistant! How can I help you find your dream home today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);
  const [sessionId, setSessionId] = useState(null);

  const API_BASE="http://127.0.0.1:8000/api/v1";

  const renderMessageContent = (text) => {
    if (!text) return null;

    const pattern = /!\[[^\]]*\]\((https?:\/\/[^\s)]+)\)|(https?:\/\/[^\s]+)/gi;
    const imageExtPattern = /\.(png|jpe?g|gif|webp|bmp|svg)(\?.*)?$/i;
    const nodes = [];
    let lastIndex = 0;
    let match;
    let keyIndex = 0;

    while ((match = pattern.exec(text)) !== null) {
      if (match.index > lastIndex) {
        nodes.push(
          <span key={`text-${keyIndex++}`}>
            {text.slice(lastIndex, match.index)}
          </span>
        );
      }

      const rawUrl = match[1] || match[2] || "";
      const cleanUrl = match[1] ? rawUrl : rawUrl.replace(/[),.;!?]+$/, "");
      const isImage = Boolean(match[1]) || imageExtPattern.test(cleanUrl);

      if (isImage) {
        nodes.push(
          <img
            key={`img-${keyIndex++}`}
            src={cleanUrl}
            alt="Property"
            className="w-full h-auto object-cover max-h-64 rounded-lg border border-white/10 my-3"
            loading="lazy"
          />
        );
      } else {
        nodes.push(
          <a
            key={`link-${keyIndex++}`}
            href={cleanUrl}
            target="_blank"
            rel="noreferrer"
            className="text-emerald-400 underline"
          >
            {cleanUrl}
          </a>
        );
      }

      lastIndex = pattern.lastIndex;
    }

    if (lastIndex < text.length) {
      nodes.push(<span key={`text-${keyIndex++}`}>{text.slice(lastIndex)}</span>);
    }

    return <>{nodes}</>;
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    // Show user message immediately
    const userMsg = { sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          session_id: sessionId || null,
        }),
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();

      // Backend returns: { session_id, answer }
      if (data.session_id) {
        setSessionId(data.session_id);
      }

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: data.answer || "I am processing your request...",
          projects: Array.isArray(data.projects) ? data.projects : [],
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "I'm having trouble connecting right now. Please try again later." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-slate-900 overflow-hidden font-sans">
      
      {/* Sidebar */}
      <div 
        className={`${
          sidebarOpen ? "w-64" : "w-0 -translate-x-full border-r-0"
        } transition-all duration-300 ease-in-out flex-shrink-0 border-r border-white/10 bg-slate-950/50 backdrop-blur-xl flex flex-col h-full z-20`}
      >
        <div className="p-4 w-64 flex flex-col h-full shrink-0 min-w-0 overflow-hidden">
          {/* New Chat Button */}
          <button 
            className="flex w-full items-center gap-2 rounded-lg bg-emerald-600/10 hover:bg-emerald-600/20 px-4 py-3 text-sm font-medium text-emerald-400 border border-emerald-500/20 transition-all shadow-sm"
            onClick={() => {
              setSessionId(null);
              setMessages([{ sender: "bot", text: "How can I help you with M3M properties today?" }]);
            }}
          >
            <Plus size={18} />
            New Chat
          </button>

          {/* Chat History Placeholder */}
          <div className="mt-8 flex-1 overflow-y-auto space-y-1 pr-2 custom-scrollbar">
            <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-2">Recent</h3>
            {["Premium Apartments", "Properties in Gurugram", "Commercial Spaces"].map((chat, idx) => (
              <button 
                key={idx} 
                className="flex w-full items-center gap-3 rounded-lg px-2 py-2.5 text-sm text-slate-300 hover:bg-white/5 transition-colors group"
              >
                <MessageSquare size={16} className="text-slate-500 group-hover:text-emerald-400" />
                <span className="truncate flex-1 text-left">{chat}</span>
                <MoreHorizontal size={14} className="opacity-0 group-hover:opacity-100 text-slate-500" />
              </button>
            ))}
          </div>

          {/* User Settings Footer */}
          <div className="mt-auto border-t border-white/10 pt-4 space-y-1">
            <Link to="/" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-white/5 transition-colors">
              <LogOut size={16} className="text-slate-400" />
              Return to Website
            </Link>
            <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-white/5 transition-colors">
              <User size={16} className="text-slate-400" />
              My Account
            </button>
            <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-white/5 transition-colors">
              <Settings size={16} className="text-slate-400" />
              Settings
            </button>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full bg-slate-900 relative">
        
        {/* Top Navbar */}
        <header className="absolute top-0 w-full h-14 border-b border-white/5 bg-slate-900/80 backdrop-blur-md flex items-center justify-between px-4 z-10">
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1 rounded-md hover:bg-white/10 text-slate-400 transition-colors"
            >
              {sidebarOpen ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
            </button>
            <div className="font-semibold text-slate-200">M3M Assistant</div>
            <div className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[10px] font-bold text-emerald-400 uppercase tracking-widest">
              Beta
            </div>
          </div>
          <div className="flex items-center rounded-full bg-slate-800 p-1 border border-white/5">
            <div className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold text-xs ring-1 ring-emerald-500/30">
              U
            </div>
          </div>
        </header>

        {/* Chat Log */}
        <div className="flex-1 overflow-y-auto w-full pt-14 pb-24 scroll-smooth">
          <div className="max-w-3xl mx-auto w-full px-4 pt-8">
            {messages.map((msg, idx) => (
              <div 
                key={idx} 
                className={`flex w-full mb-8 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className={`flex gap-4 max-w-[85%] ${msg.sender === "user" ? "flex-row-reverse" : "flex-row"}`}>
                  
                  {/* Avatar */}
                  <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center border shadow-sm mt-1 ${
                    msg.sender === "user" 
                      ? "bg-emerald-600/20 border-emerald-500/30 text-emerald-400" 
                      : "bg-indigo-600/20 border-indigo-500/30 text-indigo-400"
                  }`}>
                    {msg.sender === "user" ? <User size={16} /> : <Bot size={16} />}
                  </div>

                  {/* Message Bubble */}
                  <div className={`flex flex-col gap-1 ${msg.sender === "user" ? "items-end" : "items-start"}`}>
                    <div className="flex items-center gap-2 mb-1 px-1">
                      <span className="text-xs font-semibold text-slate-400">
                        {msg.sender === "user" ? "You" : "M3M AI"}
                      </span>
                    </div>
                    <div 
                      className={`px-5 py-3.5 rounded-2xl text-[15px] leading-relaxed shadow-sm break-words whitespace-pre-wrap border ${
                        msg.sender === "user" 
                          ? "bg-slate-800 text-slate-100 rounded-tr-sm border-white/5" 
                          : "bg-slate-800/50 text-slate-200 rounded-tl-sm border-white/5 shadow-inner"
                      }`}
                    >
                      {renderMessageContent(msg.text)}
                      {Array.isArray(msg.projects) && msg.projects.length > 0 && (
                        <div className="mt-3 space-y-3">
                          {msg.projects.map((project, projectIndex) => (
                            <div
                              key={`${project.name || "project"}-${projectIndex}`}
                              className="rounded-xl border border-white/10 bg-slate-900/40 p-3"
                            >
                              {project.image && (
                                <img
                                  src={project.image}
                                  alt={project.name || "Property"}
                                  className="w-full h-auto object-cover max-h-64 rounded-lg border border-white/10 mb-3"
                                />
                              )}
                              <div className="text-slate-100 font-semibold">{project.name || "Property"}</div>
                              {project.location && <div className="text-slate-300 text-sm mt-1">📍 {project.location}</div>}
                              {Array.isArray(project.bhk_options) && project.bhk_options.length > 0 && (
                                <div className="text-slate-300 text-sm mt-1">🛏️ {project.bhk_options.join(", ")}</div>
                              )}
                              {project.price_range && <div className="text-slate-300 text-sm mt-1">💰 {project.price_range}</div>}
                              {Array.isArray(project.amenities) && project.amenities.length > 0 && (
                                <div className="text-slate-300 text-sm mt-1">⭐ {project.amenities.slice(0, 5).join(", ")}</div>
                              )}
                              {project.link && (
                                <a
                                  href={project.link}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="inline-block mt-2 text-emerald-400 text-sm underline"
                                >
                                  View Project
                                </a>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex w-full mb-8 justify-start">
                <div className="flex gap-4 max-w-[85%] flex-row">
                  <div className="flex-shrink-0 h-8 w-8 rounded-full bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 flex items-center justify-center mt-1">
                    <Bot size={16} />
                  </div>
                  <div className="flex flex-col gap-1 items-start">
                    <div className="px-1"><span className="text-xs font-semibold text-slate-400">M3M AI</span></div>
                    <div className="px-5 py-4 rounded-2xl rounded-tl-sm bg-slate-800/50 border border-white/5 flex items-center gap-2">
                      <span className="animate-bounce delay-75 w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
                      <span className="animate-bounce delay-150 w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
                      <span className="animate-bounce delay-300 w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="absolute w-full bottom-0 bg-gradient-to-t from-slate-900 via-slate-900 to-transparent pt-10 pb-6">
          <div className="max-w-3xl mx-auto w-full px-4">
            <div className="relative group flex items-end gap-2 bg-slate-800 rounded-2xl border border-white/10 shadow-xl focus-within:ring-2 focus-within:ring-emerald-500/50 focus-within:border-emerald-500/50 transition-all p-2">
              <button 
                className="p-3 text-slate-400 hover:text-emerald-400 rounded-xl hover:bg-slate-700 transition-colors shrink-0"
                disabled={loading}
              >
                <Paperclip size={20} />
              </button>
              
              <textarea
                className="w-full bg-transparent text-slate-200 placeholder-slate-500 max-h-48 min-h-[44px] py-3 px-2 resize-none outline-none overflow-y-auto text-[15px]"
                placeholder="Ask about M3M properties..."
                rows={1}
                value={input}
                onChange={e => {
                  setInput(e.target.value);
                  e.target.style.height = 'auto';
                  e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
                }}
                onKeyDown={e => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                    e.target.style.height = 'auto';
                  }
                }}
              />
              
              <button 
                className={`p-3 rounded-xl flex-shrink-0 transition-all ${
                  input.trim() && !loading 
                    ? "bg-emerald-500 text-white hover:bg-emerald-600 shadow-md transform hover:scale-105" 
                    : "bg-slate-700 text-slate-500 cursor-not-allowed"
                }`}
                onClick={() => {
                  sendMessage();
                  const textarea = document.querySelector('textarea');
                  if(textarea) textarea.style.height = 'auto';
                }}
                disabled={!input.trim() || loading}
              >
                <Send size={20} className={input.trim() && !loading ? "-ml-0.5 mt-0.5" : ""} />
              </button>
            </div>
            <div className="text-center mt-3 text-[11px] text-slate-500">
              M3M Assistant can make mistakes. Consider verifying important information before making a decision.
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default ChatbotPage;