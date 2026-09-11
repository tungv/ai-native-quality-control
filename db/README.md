# PostgreSQL / pgvector starter

Prerequisite: Docker with Compose v2 (`docker compose`); no local Make, PostgreSQL, or SQL client is required. Run these from a host terminal in the repository root, outside the `lab` shell:

```sh
docker compose up -d --wait db
docker compose exec -T db psql -U learner -d playground -v ON_ERROR_STOP=1 -f /lab/tests.sql
```

The first command waits for database readiness. The second runs the SQL assertions and exits nonzero on failure. `db/` is mounted read-only at `/lab`, so SQL test edits are visible immediately. The test prints its checks to the terminal; save the command, output, revision, and interpretation in your evidence record.

For interactive inspection:

```sh
docker compose exec db psql -U learner -d playground
```

Type `\q` to leave psql. Stop and remove services when finished:

```sh
docker compose down
```

The database container has no published port and uses disposable memory-backed storage. `docker compose down` removes it; the next start seeds from `seed.sql`. A container restart also loses this database. After changing seed data, run `docker compose up -d --force-recreate --wait db` to seed a fresh instance. Never point these scripts at a real database.

If Make is installed on the host, `make db-test` and `make db-down` remain shortcuts. Do not run them inside the offline lab container: it has no Docker socket and cannot manage the database service.

The API keeps its own in-memory catalog; it does not connect here yet. This standalone lab teaches database constraints, deterministic ranking, and the need to scope retrieval. The credentials in Compose are public, local fixture values. There are no secrets or customer records.

`products.embedding` has three hand-authored dimensions. The query uses cosine **distance** (`<=>`, smaller is nearer), filters `tenant_id` and stock, then orders by distance and SKU for ties. The SQL checks exact result IDs, empty scope, a deliberately unscoped leakage control, negative prices, zero vectors, and dimensionality. Every check raises an error on failure; the test transaction rolls back.

Tenant filtering here is a query requirement, not authentication or database-enforced isolation: the local training user can query all rows. A later security lab should introduce a server-verified identity and role-based or row-level policies, then test attempted bypasses.

No approximate index is needed for four rows. Extend with a larger labeled corpus to compare exact vs HNSW recall and latency; do not infer semantic quality from these synthetic vectors. See the [pgvector reference](https://github.com/pgvector/pgvector) for operators, constraints, and indexing.
