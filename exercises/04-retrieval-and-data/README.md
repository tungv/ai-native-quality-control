# Lab 04 — Test retrieval and data correctness

**Status:** Uses the optional PostgreSQL/pgvector SQL lab. Connecting the Go API or assistant to that database is an extension. **Prerequisites:** Lab 03, basic SQL, and the database setup in the README. **Outcome:** Reproducible retrieval checks with explicit relevance labels and data boundaries.

## Brief

An assistant can produce a plausible answer from the wrong retrieved products. Separate three questions: which rows may be retrieved, how eligible rows rank, and whether the answer uses the retrieved evidence correctly.

## Tasks

1. Read the database schema, seed data, and vector definitions. Run the host-side Docker commands in the [database guide](../../db/README.md): `docker compose up -d --wait db`, then `docker compose exec -T db psql -U learner -d playground -v ON_ERROR_STOP=1 -f /lab/tests.sql`. These commands use the database container directly and require no local Make or PostgreSQL client. Record the database and extension versions used.
2. Identify which starter embeddings are synthetic and explain why their behavior cannot establish the quality of a production embedding model.
3. Write a small relevance table for selected synthetic queries: eligible products, relevant products, and the reason for each label. Choose `k` before measuring results. Define any missing eligibility requirement explicitly before implementing it.
4. Add or improve SQL assertions for a documented data invariant and one retrieval boundary. Examples to investigate include result limits, empty candidate sets, tied distances, and filtering before ranking; select cases supported by the actual schema.
5. Report Recall@k as relevant retrieved items divided by all labelled relevant items. Report Precision@k using an explicit denominator policy when fewer than `k` rows are returned. Treat queries with no relevant items separately instead of dividing by zero.
6. Introduce one reversible local seed/query defect, prove that an assertion or metric catches it, and restore the baseline. Explain whether the problem is eligibility, ranking, or stale data.
7. Inspect a query plan. State the dataset size and whether the query uses exact or approximate retrieval. Do not infer production performance from a tiny seed corpus.

## Evidence and completion

Submit labels, SQL/test changes, the baseline and defect results, metric formulas, and a short conclusion. State explicitly whether this was a standalone database test or a test of a connected application.

**Cleanup:** Restore altered fixtures and run `docker compose down` from a host terminal following the documented workflow. Delete only the disposable lab data you created.

**Stretch:** Connect the API or assistant to this database. Add a documented isolation rule, a changed-product reindex scenario, and an application-level regression that proves the correct retrieved evidence reaches the response. These features are new implementation work, not assumptions about the starter.
