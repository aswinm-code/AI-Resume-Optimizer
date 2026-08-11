import React, { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, Button } from "@/components/common/ui";
import { useAuth } from "@/store/AuthContext";
import * as authApi from "@/api/authApi";
import { readError } from "@/api/client";
import { useToast } from "@/hooks/useToast";

export default function Profile() {
  const { user, setUser } = useAuth();
  const toast = useToast();
  const [fullName, setFullName] = useState(user?.full_name || "");
  const [saving, setSaving] = useState(false);

  const save = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await authApi.updateMe({ full_name: fullName });
      setUser(updated);
      toast.success("Profile updated.");
    } catch (err) {
      toast.error(readError(err));
    } finally {
      setSaving(false);
    }
  };

  return (
    <AppLayout>
      <div className="max-w-lg mx-auto">
        <h1 className="text-xl font-semibold mb-6">Profile</h1>
        <Card className="p-6">
          <form onSubmit={save} className="space-y-4">
            <div>
              <label className="text-xs font-medium text-muted block mb-1.5">Email</label>
              <input className="w-full rounded-lg border border-line px-3.5 py-2.5 text-sm bg-canvas text-muted" value={user?.email || ""} disabled />
            </div>
            <div>
              <label className="text-xs font-medium text-muted block mb-1.5">Full name</label>
              <input
                className="w-full rounded-lg border border-line px-3.5 py-2.5 text-sm focus:border-accent"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
            <Button type="submit" loading={saving}>
              Save changes
            </Button>
          </form>
        </Card>
      </div>
    </AppLayout>
  );
}
