# Backend: Running Alembic migrations inside the container

Use the backend container to generate and apply Alembic migrations against the project's database.

Replace `resume_optimizer_backend` with your container name if different.

Generate an autogenerate migration (creates a new revision file):

```bash
docker exec resume_optimizer_backend alembic revision --autogenerate -m "describe changes"
```

Apply all pending migrations (upgrade to head):

```bash
docker exec resume_optimizer_backend alembic upgrade head
```

Quick check of tables using a Python one-liner (uses the project's DB engine):

```bash
docker exec resume_optimizer_backend python -c "from app.core.database import engine; import sqlalchemy as sa; ins=sa.inspect(engine); print(sorted(ins.get_table_names()))"
```

Notes:
- Alembic reads the DB URL from the app config (`settings.DATABASE_URL`), which is usually set from the container environment.
- Prefer creating new revisions instead of editing applied historical migrations when working with an existing database.
- If `psql` is not installed in the container, use the Python snippet above or connect externally with your DB client.
