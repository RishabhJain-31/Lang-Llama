import React from "react";
import { Link } from "react-router-dom";
import Navbar from "./components/navbar";
import { ArrowRight, Bot, Building, ShieldCheck, Sparkles } from "lucide-react";

function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-black overflow-x-hidden w-full">
      <Navbar />

      <main className="flex-1 w-full bg-[#030303]">
        {/* Glow Effects */}
        <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-500/20 blur-[120px]" />
          <div className="absolute top-[20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-teal-600/20 blur-[150px]" />
          <div className="absolute bottom-[-20%] left-[20%] w-[60%] h-[40%] rounded-full bg-blue-900/10 blur-[150px]" />
        </div>

        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-32 pb-24 lg:pt-48">
          <div className="text-center">
            <div className="inline-flex items-center rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-sm font-semibold text-emerald-300 shadow-xl shadow-emerald-500/10 backdrop-blur-sm transition-all hover:bg-emerald-500/20 mb-8 cursor-default">
              <Sparkles className="mr-2 h-4 w-4" aria-hidden="true" />
              M3M AI Companion v1.0
            </div>
            
            <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-7xl lg:text-8xl w-full">
              Discover Premium <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">
                Real Estate Experience
              </span>
            </h1>
            
            <p className="mx-auto mt-8 max-w-2xl text-lg sm:text-xl text-slate-400">
              Engage with our advanced conversational AI designed specifically for M3M properties. Find your dream home, explore investments, and get tailored recommendations instantly.
            </p>
            
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                to="/chat"
                className="group relative inline-flex items-center justify-center overflow-hidden rounded-full p-4 px-8 font-medium text-indigo-100 bg-white"
              >
                <span className="absolute h-0 w-0 rounded-full bg-emerald-500 transition-all duration-300 ease-out group-hover:h-56 group-hover:w-full"></span>
                <span className="absolute inset-0 w-full h-full -mt-1 rounded-lg opacity-30 bg-gradient-to-b from-transparent via-transparent to-black"></span>
                <span className="relative flex items-center text-slate-900 group-hover:text-white font-semibold text-lg transition-colors duration-300 ease-in-out">
                  Start Chatting Now
                  <ArrowRight className="ml-2 h-5 w-5" />
                </span>
              </Link>
            </div>
          </div>
          
          <div className="mx-auto mt-24 max-w-5xl">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
              {[
                { name: 'Intelligent AI', desc: 'RAG-powered conversational capabilities providing accurate info.', icon: Bot },
                { name: 'Vast Portfolio', desc: 'Instant access to all M3M properties and project details.', icon: Building },
                { name: 'Secure Search', desc: 'Enterprise-grade security ensuring your data is protected.', icon: ShieldCheck },
              ].map((feature) => (
                <div key={feature.name} className="relative rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl shadow-2xl transition-all hover:-translate-y-1 hover:border-emerald-500/30">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="rounded-xl bg-emerald-500/10 p-3">
                      <feature.icon className="h-6 w-6 text-emerald-400" aria-hidden="true" />
                    </div>
                    <h3 className="text-lg font-semibold text-white">{feature.name}</h3>
                  </div>
                  <p className="text-slate-400 text-sm leading-relaxed">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default LandingPage;