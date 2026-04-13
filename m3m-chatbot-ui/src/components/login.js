import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Building } from "lucide-react";

function Login() {
  return (
    <div className="flex min-h-screen bg-slate-950 items-center justify-center p-4">
      <div className="w-full max-w-md bg-slate-900 border border-white/10 rounded-3xl shadow-2xl overflow-hidden backdrop-blur-xl relative">
        <div className="absolute top-0 right-0 -m-16 w-32 h-32 bg-emerald-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -m-16 w-32 h-32 bg-teal-500/20 rounded-full blur-3xl pointer-events-none" />
        
        <div className="p-8 relative z-10">
          <div className="flex justify-center mb-8">
            <Link to="/" className="flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 text-white font-bold shadow-lg shadow-emerald-500/20">
                M
              </div>
              <span className="text-2xl font-semibold text-white tracking-tight">M3M AI</span>
            </Link>
          </div>
          
          <h2 className="text-2xl font-bold text-center text-white mb-2">Welcome Back</h2>
          <p className="text-slate-400 text-center text-sm mb-8">Sign in to sync your M3M real estate conversations</p>
          
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="email">Email</label>
              <input 
                type="email" 
                id="email" 
                className="w-full rounded-xl bg-slate-800 border border-white/10 p-3 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all placeholder-slate-500"
                placeholder="name@example.com"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="password">Password</label>
              <input 
                type="password" 
                id="password" 
                className="w-full rounded-xl bg-slate-800 border border-white/10 p-3 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all placeholder-slate-500"
                placeholder="••••••••"
              />
            </div>
            
            <div className="flex items-center justify-between mt-2 mb-6">
              <label className="flex items-center gap-2 text-sm text-slate-400">
                <input type="checkbox" className="rounded bg-slate-800 border-white/10 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-slate-900" />
                Remember me
              </label>
              <a href="#" className="text-sm font-medium text-emerald-400 hover:text-emerald-300 transition-colors">Forgot password?</a>
            </div>
            
            <button 
              type="button"
              className="w-full flex justify-center items-center gap-2 rounded-xl bg-emerald-500 p-3 text-sm font-bold text-white shadow-lg shadow-emerald-500/20 hover:bg-emerald-600 transition-all"
            >
              Sign In <ArrowRight size={16} />
            </button>
          </form>
          
          <p className="text-center text-slate-400 text-sm mt-8">
            Don't have an account? <a href="#" className="font-semibold text-emerald-400 hover:text-emerald-300 transition-colors">Sign up</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;