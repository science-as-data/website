"""Explicit read-only arXiv statistics export; never run during site builds.

Usage: python scripts/export_arxiv.py [--render-only]
Set ARXIV_DATABASE_URL for refreshes. Taxonomy labels are saved in assets/arxiv/.
"""
import argparse
import csv
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
ASSETS = SITE / 'assets' / 'arxiv'
TABLES = ('papers', 'paper_authors', 'paper_categories', 'paper_versions',
          'raw_records', 'duplicate_records', 'ingestion_runs')
QUERIES = {
    'runs': 'SELECT run_id, dataset_version, snapshot_sha256, status, records_loaded, finished_at FROM arxiv.ingestion_runs ORDER BY run_id',
    'summary': '''SELECT count(*) AS works, count(*) FILTER (WHERE first_submitted_at IS NULL) AS missing_first_submission,
        min(first_submitted_at) AS earliest_submission, max(first_submitted_at) AS latest_submission,
        count(*) FILTER (WHERE doi IS NOT NULL AND btrim(doi) <> '') AS with_doi,
        count(*) FILTER (WHERE abstract IS NOT NULL AND btrim(abstract) <> '') AS with_abstract,
        min(update_date) AS earliest_update, max(update_date) AS latest_update FROM arxiv.papers''',
    'years': "SELECT extract(year FROM first_submitted_at AT TIME ZONE 'UTC')::int AS year, count(*) AS works FROM arxiv.papers WHERE first_submitted_at IS NOT NULL GROUP BY 1 ORDER BY 1",
    'months': "SELECT to_char(first_submitted_at AT TIME ZONE 'UTC', 'YYYY-MM') AS month, count(*) AS works FROM arxiv.papers WHERE first_submitted_at IS NOT NULL GROUP BY 1 ORDER BY 1",
    'categories': 'SELECT category, count(DISTINCT arxiv_id) AS works FROM arxiv.paper_categories GROUP BY category ORDER BY works DESC, category',
    'category_counts': 'SELECT n AS categories_per_work, count(*) AS works FROM (SELECT p.arxiv_id, count(DISTINCT c.category) AS n FROM arxiv.papers p LEFT JOIN arxiv.paper_categories c USING (arxiv_id) GROUP BY p.arxiv_id) x GROUP BY n ORDER BY n',
}


def export():
    import psycopg
    from psycopg.rows import dict_row
    taxonomy = json.loads((ASSETS / 'taxonomy.json').read_text())
    with psycopg.connect(os.environ.get('ARXIV_DATABASE_URL', 'host=localhost dbname=arxiv user=simone'), row_factory=dict_row) as conn:
        conn.execute('BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
        conn.execute("SET LOCAL statement_timeout = '240s'")
        conn.execute("SET LOCAL lock_timeout = '5s'")
        conn.execute("SET LOCAL TIME ZONE 'UTC'")
        data = {name: conn.execute(query).fetchall() for name, query in QUERIES.items()}
        if not data['runs'] or any(r['status'] != 'complete' for r in data['runs']):
            raise RuntimeError('Expected completed ingestion runs; refusing partial statistics')
        data['table_counts'] = {name: conn.execute(f'SELECT count(*) AS n FROM arxiv.{name}').fetchone()['n'] for name in TABLES}
        data['summary'] = data['summary'][0]
        mapped = []
        for row in data['categories']:
            label = taxonomy['categories'].get(row['category'], {})
            row.update(group=label.get('group', 'Legacy / unmapped'), name=label.get('name', 'Historical code; retained as supplied'))
            mapped.append((row['category'], row['group']))
        # Distinct works within each group prevent double-counting subcategories.
        group_query = '''WITH taxonomy AS (SELECT * FROM unnest(%s::text[], %s::text[]) AS t(category, subject_group))
            SELECT t.subject_group, count(DISTINCT c.arxiv_id) AS works
            FROM arxiv.paper_categories c JOIN taxonomy t USING(category) GROUP BY 1 ORDER BY works DESC'''
        data['groups'] = conn.execute(group_query, ([x[0] for x in mapped], [x[1] for x in mapped])).fetchall()
        data['provenance'] = dict(exported_at_utc=datetime.now(timezone.utc).isoformat(), database='arxiv', schema='arxiv',
            count_basis='Exact counts after duplicate resolution, from a read-only repeatable-read transaction.',
            date_basis='Earliest available version number (first_submitted_at), grouped in UTC; not journal publication or metadata update dates.',
            taxonomy_source=taxonomy['source'], taxonomy_retrieved_at=taxonomy['retrieved_at'], queries=QUERIES, group_query=group_query)
    total = data['summary']['works']
    assert sum(r['works'] for r in data['years']) + data['summary']['missing_first_submission'] == total
    assert sum(r['works'] for r in data['months']) == sum(r['works'] for r in data['years'])
    assert sum(r['works'] for r in data['category_counts']) == total
    (ASSETS / 'summary.json').write_text(json.dumps(data, indent=2, default=str) + '\n')
    for name in ('years', 'months', 'categories', 'groups', 'category_counts'):
        with (ASSETS / f'{name}.csv').open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(data[name][0])); w.writeheader(); w.writerows(data[name])
    return data


def table(rows, key, label):
    maximum = max(r['works'] for r in rows)
    parts = [f'<div class="data-table-scroll"><table class="distribution"><thead><tr><th scope="col">{label}</th><th scope="col">Works</th><th scope="col">Relative count</th></tr></thead><tbody>']
    for r in rows:
        text = html.escape(str(r[key]))
        if key == 'category':
            text += ' · ' + html.escape(r['name'])
        parts.append(f'<tr><th scope="row">{text}</th><td>{r["works"]:,}</td><td><span class="count-bar" style="width:{100*r["works"]/maximum:.2f}%" aria-hidden="true"></span></td></tr>')
    return ''.join(parts) + '</tbody></table></div>'


def render(data):
    s = data['summary']; counts = data['table_counts']; total = s['works']
    metric = lambda value, label: f'<div><strong>{value}</strong><span>{label}</span></div>'
    out = ['<section aria-labelledby="arxiv-counts"><h2 id="arxiv-counts">The loaded dataset</h2><div class="dataset-metrics">',
        metric(f'{total:,}', 'unique works'), metric(f'{counts["paper_versions"]:,}', 'version records'),
        metric(f'{counts["paper_authors"]:,}', 'author occurrences'), metric(str(len(data['categories'])), 'observed category codes'), '</div>',
        f'<p>Snapshot version {data["runs"][-1]["dataset_version"]}. Counts measured on {data["provenance"]["exported_at_utc"][:10]} after duplicate resolution. {data["runs"][-1]["records_loaded"]:,} source records were consumed by the latest run; {counts["duplicate_records"]:,} repeated-ID events are retained for audit.</p>',
        f'<p>{s["with_abstract"]:,} works have a nonblank abstract; {s["with_doi"]:,} ({s["with_doi"]/total:.1%}) have a nonblank DOI field. DOI text is preserved as supplied and is not necessarily one normalized identifier.</p></section>',
        '<section aria-labelledby="time"><h2 id="time">Works over time</h2>',
        f'<p>First submission timestamps span {str(s["earliest_submission"])[:10]} to {str(s["latest_submission"])[:10]}. Each work appears once, using the timestamp of its earliest available version number, in UTC. These are submission dates, not journal publication dates or metadata updates. {s["missing_first_submission"]:,} works lack this date.</p>',
        f'<p><strong>{data["years"][-1]["year"]} is a partial year</strong> in this snapshot; the final month is also incomplete. Bar lengths show counts, without annualizing partial periods.</p>',
        table(data['years'], 'year', 'First submission year'),
        '<details><summary>Monthly distribution — all observed months</summary>', table(data['months'], 'month', 'First submission month'), '</details></section>',
        '<section aria-labelledby="categories"><h2 id="categories">Subject groups and subcategories</h2><p>Group labels follow the <a href="https://arxiv.org/category_taxonomy">arXiv taxonomy</a>. Within a group, each work is counted once even when it has several subcategories. Works can appear in multiple groups, so group totals are not additive. Historical codes absent from the current taxonomy remain visible under “Legacy / unmapped.” Category order is preserved in the database, but is not treated here as a primary-category label.</p>',
        table(data['groups'], 'subject_group', 'Subject group'),
        '<label class="category-filter" hidden>Find a category or subject <input type="search" id="arxiv-category-search" placeholder="Try cs.LG, astrophysics, or probability"></label><p id="arxiv-category-status" role="status" aria-live="polite"></p>']
    for group in data['groups']:
        rows = [r for r in data['categories'] if r['group'] == group['subject_group']]
        out += [f'<details class="category-group"><summary>{html.escape(group["subject_group"])} · {len(rows)} category codes</summary>', table(rows, 'category', 'Category code and name'), '</details>']
    multi = sum(r['works'] for r in data['category_counts'] if r['categories_per_work'] > 1)
    out += [f'<p>{multi:,} works ({multi/total:.1%}) carry more than one distinct category. Counts within individual category rows are distinct works; cross-listing makes category totals overlap.</p></section>',
        '<section aria-labelledby="downloads"><h2 id="downloads">Data and provenance</h2><p>Download the saved aggregates used on this page: <a href="/assets/arxiv/summary.json" download>statistics and SQL (JSON)</a>, <a href="/assets/arxiv/years.csv" download>annual counts</a>, <a href="/assets/arxiv/months.csv" download>monthly counts</a>, <a href="/assets/arxiv/categories.csv" download>category counts</a>, <a href="/assets/arxiv/groups.csv" download>group counts</a>, and <a href="/assets/arxiv/category_counts.csv" download>categories per work</a>.</p><p>The export includes ingestion checksums and timestamps. These are static database aggregates, not live arXiv statistics. Later snapshot loads may retain older papers absent from the new source; consult all ingestion runs in the JSON before comparing releases.</p></section>']
    (SITE / '_layout' / 'arxiv-statistics.html').write_text('\n'.join(out) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-only', action='store_true')
    args = parser.parse_args()
    render(json.loads((ASSETS / 'summary.json').read_text()) if args.render_only else export())
