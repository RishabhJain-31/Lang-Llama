import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X, ArrowRight } from "lucide-react";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-white/10 bg-black/50 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <Link to="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 text-white font-bold shadow-lg shadow-emerald-500/20">
              M
            </div>
            <span className="text-xl font-semibold text-white tracking-tight">M3M AI</span>
          </Link>
        </div>

        {/* Desktop Menu */}
        <div className="hidden md:flex md:items-center md:gap-8">
          <Link to="/" className="text-sm font-medium text-slate-300 transition-colors hover:text-white">Home</Link>
          <button className="text-sm font-medium text-slate-300 transition-colors hover:text-white">Upload Docs</button>
          <Link to="/chat" className="text-sm font-medium text-slate-300 transition-colors hover:text-white">Chat</Link>
          <Link 
            to="/login" 
            className="inline-flex items-center justify-center rounded-full bg-white/10 px-4 py-2 text-sm font-medium text-white shadow-sm ring-1 ring-inset ring-white/20 transition-all hover:bg-white/20"
          >
            Login
          </Link>
        </div>

        {/* Mobile menu button */}
        <div className="flex md:hidden">
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-md p-2 text-slate-400 hover:bg-white/10 hover:text-white focus:outline-none"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <span className="sr-only">Open main menu</span>
            {menuOpen ? <X className="h-6 w-6" aria-hidden="true" /> : <Menu className="h-6 w-6" aria-hidden="true" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden border-t border-white/10 bg-slate-900 px-2 pb-3 pt-2 space-y-1">
          <Link to="/" className="block rounded-md px-3 py-2 text-base font-medium text-white hover:bg-white/10">Home</Link>
          <button className="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-slate-300 hover:bg-white/10 hover:text-white">Upload Docs</button>
          <Link to="/chat" className="block rounded-md px-3 py-2 text-base font-medium text-slate-300 hover:bg-white/10 hover:text-white">Chat</Link>
          <Link to="/login" className="block rounded-md px-3 py-2 text-base font-medium text-slate-300 hover:bg-white/10 hover:text-white">Login</Link>
        </div>
      )}
    </nav>
  );
}

export default Navbar;