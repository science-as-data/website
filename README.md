# Science as Data website

The organization website for [Science as Data](https://github.com/science-as-data), built with [Franklin.jl](https://franklinjl.org/). It showcases repository outcomes, covering arXiv, OpenAlex, and CORE, with preregistrations next in the queue. This is a standalone repository, moved from `openalex/website/`.

The homepage introduces the projects; `/openalex/` retains the original OpenAlex overview, and `/arxiv/` describes the metadata workflow and its current scope. `/core/` reserves space for CORE outcomes, pending project details. Existing `/protocol/`, `/schema/`, `/queries/`, and `/preview/` routes remain OpenAlex resources. Builds use saved assets and require no database access.

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

## Edit the site

- `index.md` and `_layout/organization.html`: organization homepage and project summaries.
- `openalex.md` and `_layout/landing.html`: OpenAlex overview and conceptual data illustration.
- `arxiv.md`: arXiv outcomes, workflow, and current scope.
- `core.md`: CORE project status; add verified outcomes when available.
- Keep preregistrations in the homepage queue until project material is ready.
- `protocol.md`, `schema.md`, `queries.md`, `preview.md`: Markdown documentation and dataset preview pages.
- `_layout/query-examples.html`: query tabs and SQL examples.
- `_layout/head.html`, `_layout/foot.html`: shared navigation and footer.
- `_css/site.css`, `_libs/site.js`: responsive styles and progressive enhancements (published as `css/` and `libs/`).
- `config.md`: site metadata, output container, ignored build inputs, and deployment prefix.

Assets and system fonts are served locally. Copy buttons report clipboard failures and select the code for manual copying. Query tabs support arrow keys, Home, End, and URL fragments. Without JavaScript, all examples and navigation links remain visible.

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
