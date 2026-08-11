import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { FileText } from "lucide-react";
import { Button } from "@/components/common/ui";
import { useAuth } from "@/store/AuthContext";
import { readError } from "@/api/client";

interface FormValues {
  email: string;
  password: string;
}

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>();

  const onSubmit = async (values: FormValues) => {
    setServerError(null);
    try {
      await login({
        username: values.email,
        password: values.password,
      });
      navigate("/dashboard");
    } catch (err) {
      setServerError(readError(err, "Invalid email or password."));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6 bg-canvas">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-9 h-9 rounded-lg bg-accent flex items-center justify-center mx-auto mb-3">
            <FileText size={18} className="text-white" />
          </div>
          <h1 className="text-xl font-semibold">Welcome back</h1>
          <p className="text-sm text-muted mt-1">Log in to continue optimizing your resume.</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="bg-surface border border-line rounded-xl shadow-card p-6 space-y-4">
          <div>
            <label className="text-xs font-medium text-muted block mb-1.5">Email</label>
            <input
              type="email"
              className="w-full rounded-lg border border-line px-3.5 py-2.5 text-sm focus:border-accent"
              placeholder="you@example.com"
              {...register("email", { required: "Email is required" })}
            />
            {errors.email && <p className="text-xs text-bad mt-1">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-xs font-medium text-muted block mb-1.5">Password</label>
            <input
              type="password"
              className="w-full rounded-lg border border-line px-3.5 py-2.5 text-sm focus:border-accent"
              placeholder="••••••••"
              {...register("password", { required: "Password is required" })}
            />
            {errors.password && <p className="text-xs text-bad mt-1">{errors.password.message}</p>}
          </div>
          {serverError && <p className="text-sm text-bad">{serverError}</p>}
          <Button type="submit" className="w-full" loading={isSubmitting}>
            Login
          </Button>
        </form>

        <p className="text-center text-sm text-muted mt-5">
          No account?{" "}
          <Link to="/register" className="text-accent font-medium">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}
