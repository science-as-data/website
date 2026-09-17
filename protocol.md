+++
title = "The protocol"
+++

~~~
<header class="article-header wrap"><h1>OpenAlex loading protocol</h1><p class="lede">Convert a specified OpenAlex snapshot into linked PostgreSQL tables. The protocol covers sample validation, storage requirements, record extraction, loading, and indexing.</p></header>
<div class="article-layout wrap"><aside class="article-nav" aria-label="On this page"><a class="project-identity" href="/openalex/" aria-label="OpenAlex section overview"><img src="/assets/openalex-mark.png" width="36" height="36" alt=""><span>OpenAlex</span></a><strong>In this protocol</strong><a href="#prepare">Before you begin</a><a href="#verify">Test a sample</a><a href="#download">01 · Download</a><a href="#flatten">02 · Flatten</a><a href="#load">03 · Load &amp; index</a><a href="#query">04 · Query</a><a href="#refresh">Refresh &amp; reproduce</a></aside><article class="article">
~~~

\label{prepare}
## Before you begin

The pipeline targets the **standard-format OpenAlex snapshot, reference release 2026-03-30**, and PostgreSQL 18. Its scripts reflect a Linux workstation with a dedicated SSD. Read the [repository’s setup instructions](https://github.com/science-as-data/openalex/blob/main/datadump/README.md) alongside this guide.

| Requirement | What to prepare |
| :--- | :--- |
| Software | Python 3, PostgreSQL 18 and `psql`, Bash, AWS CLI, `curl`, and gzip utilities |
| Storage | Approximately 712 GB for the compressed reference snapshot, an estimated 1.5–2 TB for tables and indexes, plus transient CSVs and working headroom |
| Access | A PostgreSQL administrator and `sudo` access for directory ownership, database setup, and load tuning |
| Credentials | The PostgreSQL role password in `~/.pgpass`; the public snapshot download needs no AWS account |

```bash
git clone https://github.com/science-as-data/openalex.git
cd openalex
python -m venv .venv
source .venv/bin/activate
pip install awscli
cd datadump/scripts
```

### Adapt the workstation settings

The defaults use role `simone`, database `openalex`, the SSD path `/media/simone/ssd2/openalex`, and PostgreSQL configuration under `/etc/postgresql/18/main/conf.d/`.

Inspect `00_setup_db.sql`, `set_password.sh`, and `run_all.sh` before a full run. **The tablespace path in `00_setup_db.sql` is hard-coded**: changing `OPENALEX_ROOT` alone does not relocate it. Keep the SQL tablespace path, directories, role, credentials, and connection settings consistent with your machine. `OPENALEX_SNAPSHOT`, `OPENALEX_CSV`, `JOBS`, and `PSQL` configure the individual processing scripts.

\label{verify}
## Test a sample first

The smoke test fetches one real S3 part-file per entity, then runs flattening, schema creation, bulk loading, and indexing. This catches column and type mismatches before a full load. A part-file can still be large; this is an integration check, not a tiny fixture.

```bash
# Run from datadump/scripts/ with PostgreSQL available.
# Choose an unused name: this database is dropped before and after the test.
sudo -u postgres env SMOKE_DB=openalex_protocol_smoke bash ./smoke_test.sh
```

Ensure the `postgres` user can traverse the repository directory. The test prints row counts and a success message; inspect both. Repeat it whenever `oa_schema.py` changes.

\label{download}
## 01 · Download the snapshot

`download.sh` syncs the public `s3://openalex/data/` tree. It excludes the separate legacy snapshot and can be rerun after an interrupted transfer.

```bash
# Begin with a few entities to inspect the files.
./download.sh topics sources institutions

# Download all supported entities when storage is ready.
./download.sh
```

Files retain their partitioned layout: `snapshot/data/<entity>/updated_date=YYYY-MM-DD/part_NNN.gz`. Each compressed line is one JSON record. Keep these source files if you want to repeat the load without downloading again.

\label{flatten}
## 02 · Flatten nested records

`oa_schema.py` defines both table columns and per-record extractors. `flatten.py` uses that definition to produce headerless, gzipped CSV shards. A work becomes one row in `works`, with separate rows for its authorships, topics, locations, and references.

```bash
# An inspection run: up to 100 records PER input part-file.
# Keep this scratch output separate from the production CSV directory.
python flatten.py topics --limit 100 --jobs 4 --csv /tmp/openalex-preview-csv
```

The full loader performs flattening for you. It processes independent input files in parallel and loads lookup entities before works. Read [the schema guide](/schema/) to understand the output.

\label{load}
## 03 · Load, index, and analyze

Once the machine-specific setup has been reviewed, configure the role password and run the driver:

```bash
./set_password.sh
./run_all.sh

# Alternative when the entire snapshot has already been downloaded:
./run_all.sh --skip-download
```

Use **one** driver command for the appropriate starting state. It prepares directories, creates the database and tablespace, applies temporary load tuning, and invokes `load.sh`.

The loader creates the schema, flattens and bulk-copies each entity, and removes its transient CSV shards after loading. It builds primary keys and indexes once the data is in place, then runs `VACUUM ANALYZE` so PostgreSQL can plan queries.

> **A full load replaces existing tables.** Generated schema SQL contains `DROP TABLE … CASCADE`. Use a dedicated database and preserve any research outputs separately. Named-entity loads skip schema creation and indexing; they are not an automatic deduplicating refresh.

The driver normally removes its tuning file after a successful load. After an interrupted run, inspect the configuration and use the supplied restoration script when the database is ready:

```bash
sudo ./restore_normal_config.sh
```

It restores normal database settings and re-enables the unattended-upgrade timers used by this workstation setup. Do not leave bulk-load tuning enabled for everyday use.

\label{query}
## 04 · Connect and ask questions

With the default role and database:

```bash
psql -U simone -h localhost -d openalex
```

```sql
SELECT display_name, works_count
FROM openalex.topics
ORDER BY works_count DESC
LIMIT 10;
```

Begin with small lookup tables. Use `EXPLAIN` to inspect a query plan before expensive joins over works and citation links. A small `LIMIT` does not necessarily make an aggregate cheap.

\label{refresh}
## Refresh and reproduce

The download sync is resumable; database loading is a **full-reload workflow**, not an incremental merge engine. Merged-ID deletions are not applied automatically. S3 sync by itself does not pin a historical release.

For a reproducible study, preserve the exact input file set and manifests, record the snapshot release and repository commit, and save your SQL, sampling rules, and exported results. Distinguish changes in research from changes in database coverage.

~~~
<div class="next-page"><a href="/schema/">Next: understand the schema →</a><a href="https://github.com/science-as-data/openalex/tree/main/datadump/scripts">Inspect the scripts ↗</a></div></article></div>
~~~
