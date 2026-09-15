# Science as Data website

The organization website for [Science as Data](https://github.com/science-as-data), built with [Franklin.jl](https://franklinjl.org/). It documents OpenAlex, arXiv, CORE, Pre-registrations, and Data matching, with explicit status notes for planned work. This is a standalone repository, moved from `openalex/website/`.

The homepage introduces each project. `/arxiv/` presents exact snapshot statistics,
`/core/` documents the loaded dump and historical assessment, `/pre-registrations/`
covers source collection, and `/data-matching/` describes linkage routes and outcomes.
Existing OpenAlex pages and the static preview remain available. Builds use saved
assets and require no database or API access.

## Preview locally

Use Julia 1.12 (the committed manifest was resolved with Julia 1.12.6). From this directory:

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. -e 'using Franklin; serve()'
```

Open **http://localhost:8000**. Franklin rebuilds when source files change. Stop the server with Ctrl+C. The first run may take longer while Julia compiles dependencies.

## Build static files

From the repository root:

```bash
julia --project=. build.jl
```

The output is `__site/`. The default URL prefix is empty for organization-level hosting at `/`. To host under the website repository’s GitHub Pages path, build with:

```bash
FRANKLIN_PREPATH="website" julia --project=. build.jl
```

Upload the contents of `__site/` to your static host. A production build with a prefix must be served at that prefix; use `serve()` for the usual local preview. Building does not publish the website. See Franklin’s [deployment guide](https://franklinjl.org/workflow/deploy/) for hosting options. Pre-rendering and minification are disabled in accordance with the [Franklin project guidance](https://github.com/JuliaDocs/Franklin.jl).

## Publish

The public site is https://science-as-data.github.io/website/.
Pushing to `main` runs `.github/workflows/pages.yml`, which builds with Julia
1.12.6 and the `website` URL prefix, then deploys `__site/` to GitHub Pages.
You can also run **Publish website** manually from the repository’s Actions tab.
GitHub Pages uses **GitHub Actions** as its publishing source.

## Edit the site

- `index.md` and `_layout/organization.html`: organization homepage and project summaries.
- `openalex.md` and `_layout/landing.html`: OpenAlex overview and conceptual data illustration.
- `arxiv.md` and `_layout/arxiv-statistics.html`: arXiv schema, counts, and distributions.
- `core.md`: CORE data model, documented load totals, and dated sample estimates.
- `pre-registrations.md`: implemented collectors, fields, and coverage limitations.
- `data-matching.md`: linkage network, implemented/planned routes, and historical outcomes.
- The Overview tab links to the organization homepage; each research area has its own navigation entry.
- `protocol.md`, `schema.md`, `queries.md`, `preview.md`: Markdown documentation and dataset preview pages.
- `_layout/query-examples.html`: query tabs and SQL examples.
- `_layout/head.html`, `_layout/foot.html`: shared navigation and footer.
- `_css/site.css`, `_libs/site.js`: responsive styles and progressive enhancements (published as `css/` and `libs/`).
- `config.md`: site metadata, output container, ignored build inputs, and deployment prefix.

Assets and the JuliaMono heading font are served locally; body text uses system fonts. JuliaMono is distributed under the SIL Open Font License in `assets/fonts/JuliaMono-LICENSE.txt`. Copy buttons report clipboard failures and select the code for manual copying. Query tabs support arrow keys, Home, End, and URL fragments. Without JavaScript, all examples and navigation links remain visible.

Check desktop and mobile layouts, keyboard navigation, copy controls, and internal links after changes. Review SQL against `datadump/scripts/sql/01_create_schema.sql` in the OpenAlex repository; do not add automatically executed research queries to the build. Preserve the reference release label when updating snapshot figures. The main database smoke test is unnecessary for website-only edits.

## Static dataset preview

`/preview/` contains an actual, bounded export from the local PostgreSQL database: 80 works and linked metadata across 10 tables, plus the column inventory and planner row estimates for all 50 tables. Browser search, sorting, pagination, and work inspection run entirely on these static assets. The page never connects to PostgreSQL or calls the OpenAlex API. Without JavaScript, the work table, schema catalog, and downloads remain available.

The saved JSON includes the export timestamp, operator-supplied snapshot release label, exporter repository commit (historical exports refer to the OpenAlex repository; new exports identify the website repository), sampling SQL, and scope limitations. This block sample is not representative, and citation links are capped at 12 per work. Database row totals are estimates from `pg_class.reltuples`, not exact counts. CSV downloads include the entire exported table, regardless of the current browser filter; JSON preserves nulls and types.

To explicitly refresh the public metadata export (requires psycopg 3 and access to the loaded database), run from the repository root:

```bash
python scripts/export_preview.py --snapshot-release 2026-03-30
```

The script uses `OPENALEX_DSN`, or the default `dbname=openalex user=simone host=localhost` with `~/.pgpass`. Queries run in a read-only, repeatable-read transaction with statement and lock timeouts. It does not scan whole tables for exact counts. The default work sample uses `TABLESAMPLE SYSTEM (0.0001) REPEATABLE (20260910)`, sorts by ID, then limits to 80. The seed is repeatable for an unchanged physical table; preserving the export is necessary for reproducibility across reloads.

Generated artifacts are `assets/preview/dataset.json`, ten table CSVs, and `_layout/dataset-{preview,catalog}.html`. Commit these small, curated metadata exports together. Credentials, raw snapshot files, and Scopus data are excluded. To update the generated HTML after template changes without another database read:

```bash
python scripts/export_preview.py --render-only
```

The Franklin build uses the saved artifacts and never runs the exporter. The generator lives in `scripts/`, which is excluded from the published output.

## arXiv statistics

`assets/arxiv/summary.json` stores exact read-only database aggregates, SQL,
ingestion checksums, count units, and export timestamps. Annual and monthly
counts use first submission dates in UTC. Category groups count distinct works
within each group; cross-listing makes groups overlap. Historical category codes
absent from the saved official taxonomy are retained under “Legacy / unmapped.”

From this repository, explicitly refresh with psycopg 3 and database access:

```bash
python scripts/export_arxiv.py
# Or regenerate the HTML from saved aggregates without a database:
python scripts/export_arxiv.py --render-only
```

Set `ARXIV_DATABASE_URL` to override the local `arxiv` database connection.
The exporter rejects unfinished ingestion runs and checks aggregate totals.
Commit the JSON, CSVs, and generated layout together. `assets/arxiv/taxonomy.json`
records the source URL and retrieval date for saved taxonomy labels; review it
when refreshing. The website build never runs the exporter.

CORE and linkage figures are historical documentation summaries, not fresh
live-database counts. Keep assessment dates, sampling denominators, matching
units, and source-report links attached when editing them.

## Project scope review

Last reviewed against local checkouts: **2026-09-15**. Check the following sources
when updating the homepage, project pages, or linkage diagram:

| Project | Scope reflected on the website | Repository evidence |
|---|---|---|
| OpenAlex | API tools, PostgreSQL snapshot pipeline, publication-date audits, and the existing journal matcher | `openalex/README.md`, `quality/publication_dates/README.md`, `results_fulltext_decades_20260914.md` |
| arXiv | Loaded metadata snapshot, exact exported statistics, relational schema; OAI-PMH and bulk text workflows planned | `arxiv/kaggle/README.md`, `kaggle/sql/schema.sql`, `oai_pmh/README.md`, `s3/README.md` |
| CORE | Loaded 2024 dump, parsing/ingestion, completed baseline and API sizing, sampled drift assessment; field-fill outstanding | `core/docs/INGESTION.md`, `docs/COMPLETENESS_ASSESSMENT.md` |
| Pre-registrations | Five implemented collectors and platform-specific data representation; matching/EDA moved out | `study-preregistrations/README.md` and individual collector READMEs |
| Data matching | Cross-source linkage ownership; migrated registration matcher/training/EDA; journal matcher still in OpenAlex | `data-matching/README.md`, `preregistrations/README.md`, `preregistrations/EDA/REPORT.md` |

Repository evidence paths are relative to the named sibling checkout. General
OpenAlex–arXiv matching remains planned, while the OpenAlex date audit documents
nine bounded arXiv history checks. Keep that distinction in both project pages
and the linkage diagram. Do not infer a validated crosswalk from adapters or
rule-selected positive candidates. Review dates describe scope checks, not new
data collection or refreshed measurements.
