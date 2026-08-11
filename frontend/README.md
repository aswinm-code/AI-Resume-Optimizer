# AI Resume Optimizer — Frontend

React + TypeScript + Vite frontend for a FastAPI-based AI resume optimizer.

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

Runs at `http://localhost:5173`. `/api/*` is proxied to `http://127.0.0.1:8000`
(your FastAPI server) via `vite.config.ts`.

**Direct-call alternative:** set `VITE_API_BASE_URL=http://localhost:8000` in
`.env` and add CORS to FastAPI for `http://localhost:5173`:

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Structure

Matches the spec: `api/`, `components/{layout,resume,job,analysis,common}/`,
`pages/`, `hooks/`, `types/`, `store/`. `store/AuthContext.tsx` holds the JWT
+ current user (kept minimal instead of a separate state library, since
there's a single global slice of state to manage). `hooks/useToast.tsx`
provides the success/error toasts used across all API operations.

## Flow

```
Landing → Login/Register → Dashboard
Dashboard: Upload Resume + Paste JD → Analyze / Optimize → Preview → Download
Analysis (nav item) → history of past analyses
```

## ⚠️ Backend schema assumptions — verify these

I only had your `/docs` endpoint list (paths + methods), not the actual
request/response bodies. Every call is centralized in `src/api/*.ts`, each
with a comment documenting the exact shape assumed. The ones most likely to
need adjustment:

| Endpoint | Assumed request | Assumed response |
|---|---|---|
| `POST /auth/login` | form-urlencoded `username`+`password` (OAuth2 standard) | `{ access_token, token_type }` |
| `POST /auth/register` | `{ email, password, full_name }` | `User` |
| `POST /resumes/upload` | multipart, field `"file"` | `{ id, filename, uploaded_at, size_bytes }` |
| `POST /job-descriptions` | `{ title, company, description }` | `JobDescription` |
| `POST /analysis` | `{ resume_id, job_description_id }` | `AnalysisResult` (see `src/types/index.ts`) |
| `POST /resume-optimizer` | `{ resume_id, job_description_id }` | full `OptimizedResume` object |
| `GET /export/docx\|pdf/{version_id}` | — | binary file |

**Two structural assumptions worth flagging specifically:**

1. Your API models a job description as a saved entity
   (`POST /job-descriptions` → id), but the UI spec treats it as free-typed
   text. I bridge this in `src/pages/Dashboard.tsx`'s `ensureJobDescription()`
   — it silently saves the pasted text as a job description on first
   Analyze/Optimize click, then reuses that id. If your `/analysis` or
   `/resume-optimizer` endpoints actually accept raw JD text directly, this
   extra step can be removed.
2. `AnalysisResult` and `OptimizedResume` field names (`overall_score`,
   `skills_score`, `professional_summary`, `experience[].bullets`, etc.) are
   taken directly from your spec doc's section 24 types. If your FastAPI
   response models use different field names, update `src/types/index.ts`
   and the corresponding function in `src/api/analysisApi.ts` /
   `optimizerApi.ts` — no component needs to change beyond that.

## Notes

- The JWT is stored in `localStorage` (`resume_optimizer_token`) and attached
  automatically via an Axios request interceptor — no component sends it
  manually. A 401 response clears it and redirects to `/login`.
- All loading/success/error states use the toast system + inline `loading`
  props on `<Button>` — no raw FastAPI error text is ever shown to the user.
