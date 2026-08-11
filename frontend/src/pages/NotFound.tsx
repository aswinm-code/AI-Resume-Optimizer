import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/common/ui";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center bg-canvas">
      <p className="text-5xl font-bold text-ink mb-2">404</p>
      <p className="text-sm text-muted mb-6">This page doesn't exist.</p>
      <Link to="/dashboard">
        <Button>Back to Dashboard</Button>
      </Link>
    </div>
  );
}
