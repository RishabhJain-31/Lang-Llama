import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatbotPage from "./ChatbotPage";
import LandingPage from "./LandingPage";
import Navbar from "./components/navbar";
import Login from "./components/login";
import "./index.css";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 text-slate-900 font-sans antialiased overflow-hidden flex flex-col">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/chat" element={<ChatbotPage />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;