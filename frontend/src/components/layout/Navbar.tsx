import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { FileText, LayoutDashboard, BarChart3, User, LogOut, Menu, X } from "lucide-react";
import { useAuth } from "@/store/AuthContext";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/dashboard", label: "Resume", icon: FileText, hidden: true }, // resume lives inside dashboard
  { to: "/analysis", label: "Analysis", icon: BarChart3 },
];

export function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const visibleLinks = links.filter((l) => !l.hidden);

  return (
    <header className="border-b border-line bg-surface/95 backdrop-blur sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <button onClick={() => navigate("/dashboard")} className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-md bg-accent flex items-center justify-center">
              <FileText size={15} className="text-white" />
            </div>
            <span className="font-semibold text-sm tracking-tight">Resume Optimizer</span>
          </button>
          <nav className="hidden md:flex items-center gap-1">
            {visibleLinks.map((l) => (
              <NavLink
                key={l.label}
                to={l.to}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive ? "bg-accent-light text-accent" : "text-muted hover:text-ink hover:bg-canvas"
                  }`
                }
              >
                {l.label}
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="hidden md:flex items-center gap-3">
          <button
            onClick={() => navigate("/profile")}
            className="flex items-center gap-2 text-sm text-muted hover:text-ink transition-colors"
          >
            <User size={15} />
            {user?.full_name || user?.email}
          </button>
          <Button_Logout onClick={logout} />
        </div>

        <button className="md:hidden text-ink" onClick={() => setOpen((o) => !o)} aria-label="Toggle menu">
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-line px-4 py-3 space-y-1">
          {visibleLinks.map((l) => (
            <NavLink
              key={l.label}
              to={l.to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `block px-3 py-2.5 rounded-lg text-sm font-medium ${
                  isActive ? "bg-accent-light text-accent" : "text-ink"
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
          <NavLink to="/profile" onClick={() => setOpen(false)} className="block px-3 py-2.5 rounded-lg text-sm font-medium text-ink">
            Profile
          </NavLink>
          <button
            onClick={logout}
            className="w-full text-left px-3 py-2.5 rounded-lg text-sm font-medium text-bad"
          >
            Log out
          </button>
        </div>
      )}
    </header>
  );
}

function Button_Logout({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg border border-line hover:border-ink/40 transition-colors"
    >
      <LogOut size={13} />
      Log out
    </button>
  );
}
