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



def annual_chart(data):
    """Render the saved annual counts; distinguish the incomplete final year."""
    counts = {int(row['year']): int(row['works']) for row in data['years']}
    first, last = min(counts), max(counts)
    years = list(range(first, last + 1))
    width, height = 900, 390
    left, right, top, bottom = 85, 35, 30, 65
    plot_width, plot_height = width - left - right, height - top - bottom
    step = 100000
    ceiling = max(step, ((max(counts.values()) + step - 1) // step) * step)
    bar_width = plot_width / len(years) * 0.75
    x = lambda year: left + (year - first + 0.5) / len(years) * plot_width
    y = lambda count: top + plot_height * (1 - count / ceiling)
    parts = ['<figure class="annual-chart" aria-labelledby="annual-chart-caption">',
        '<div class="annual-chart-scroll">',
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="annual-chart-title annual-chart-desc">',
        '<title id="annual-chart-title">arXiv works by first submission year</title>',
        f'<desc id="annual-chart-desc">Bar chart of annual work counts from {first} to {last}. Each work is counted once by first submission year. The hatched final bar denotes incomplete {last} data. Exact counts are available in the year selector and CSV download.</desc>',
        '<defs><pattern id="partial-year-hatch" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="white"/><path d="M-1 1L1-1M0 6L6 0M5 7L7 5" stroke="#325b79" stroke-width="1.5"/></pattern></defs>',
        '<text x="85" y="18" class="chart-axis-title">Works</text>']
    for tick in range(0, ceiling + 1, step):
        parts += [f'<line class="chart-grid" x1="{left}" y1="{y(tick):.2f}" x2="{width-right}" y2="{y(tick):.2f}"/>',
                  f'<text x="{left-12}" y="{y(tick)+5:.2f}" text-anchor="end">{tick:,}</text>']
    ticks = [first] + list(range(((first // 10) + 1) * 10, last, 10)) + [last]
    for year in ticks:
        parts.append(f'<text x="{x(year):.2f}" y="{height-bottom+27}" text-anchor="middle">{year}</text>')
    parts += [f'<text x="{left+plot_width/2}" y="{height-12}" text-anchor="middle" class="chart-axis-title">First submission year (UTC)</text>']
    for year in years:
        count = counts.get(year, 0)
        label = f'{year}: {count:,} works' + (' (partial year)' if year == last else '')
        parts.append(f'<rect class="chart-bar{" chart-bar-partial" if year == last else ""}" x="{x(year)-bar_width/2:.2f}" y="{y(count):.5f}" width="{bar_width:.2f}" height="{plot_height*count/ceiling:.5f}" data-year="{year}" data-count="{count}" data-label="{label}"><title>{label}</title></rect>')
    parts += ['</svg></div>',
        f'<figcaption id="annual-chart-caption">Annual counts from the loaded snapshot. Hatched bar: {last} through {str(data["summary"]["latest_submission"])[:10]}; not annualized.</figcaption>',
        f'<div class="chart-inspector" hidden><label for="arxiv-chart-year">Inspect year</label><input id="arxiv-chart-year" type="range" min="{first}" max="{last}" value="{last-1}" step="1"><output for="arxiv-chart-year" id="arxiv-chart-value" aria-live="polite"></output></div>',
        '<a class="text-link" href="/assets/arxiv/years.csv" download>Download annual counts (CSV)</a></figure>']
    return '\n'.join(parts)



def subject_group_chart(rows):
    """Horizontal bars share a zero-based scale; counts remain readable as text."""
    ordered = sorted(rows, key=lambda row: row['works'], reverse=True)
    maximum = max(row['works'] for row in ordered)
    ceiling = max(200000, ((maximum + 199999) // 200000) * 200000)
    parts = ['<figure class="subject-chart" aria-labelledby="subject-chart-caption">',
             '<div class="subject-chart-axis" aria-hidden="true"><span>Works</span><div>']
    for fraction in (0, .25, .5, .75, 1):
        parts.append(f'<span>{ceiling*fraction/1000000:g}M</span>')
    parts += ['</div><span></span></div><ol class="subject-chart-rows" aria-label="Works by subject group">']
    for row in ordered:
        name = html.escape(row['subject_group'])
        value = row['works']
        parts.append(f'<li><span class="subject-chart-label">{name}</span><span class="subject-chart-track" aria-hidden="true"><span class="subject-chart-bar" style="width:{100*value/ceiling:.5f}%"></span></span><span class="subject-chart-value">{value:,}<span class="sr-only"> works</span></span></li>')
    parts += ['</ol><figcaption id="subject-chart-caption">Distinct works within each subject group. Cross-listed works can occur in multiple groups; counts are not additive.</figcaption>',
              '<a class="text-link" href="/assets/arxiv/groups.csv" download>Download subject-group counts (CSV)</a></figure>']
    return '\n'.join(parts)


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
        f'<p><strong>{data["years"][-1]["year"]} is a partial year</strong> in this snapshot; the final month is also incomplete. Counts are not annualized; the hatched bar identifies the incomplete year.</p>',
        annual_chart(data),
        '</section>',
        '<section aria-labelledby="categories"><h2 id="categories">Subject groups and subcategories</h2><p>Group labels follow the <a href="https://arxiv.org/category_taxonomy">arXiv taxonomy</a>. Within a group, each work is counted once even when it has several subcategories. Works can appear in multiple groups, so group totals are not additive. Historical codes absent from the current taxonomy remain visible under “Legacy / unmapped.” Category order is preserved in the database, but is not treated here as a primary-category label.</p>',
        subject_group_chart(data['groups']),
        '<label class="category-filter" hidden>Find a category or subject <input type="search" id="arxiv-category-search" placeholder="Try cs.LG, astrophysics, or probability"></label><p id="arxiv-category-status" role="status" aria-live="polite"></p>']
    for group in data['groups']:
        rows = [r for r in data['categories'] if r['group'] == group['subject_group']]
        out += [f'<details class="category-group"><summary>{html.escape(group["subject_group"])} · {len(rows)} category codes</summary>', table(rows, 'category', 'Category code and name'), '</details>']
    multi = sum(r['works'] for r in data['category_counts'] if r['categories_per_work'] > 1)
    out += [f'<p>{multi:,} works ({multi/total:.1%}) carry more than one distinct category. Counts within individual category rows are distinct works; cross-listing makes category totals overlap.</p></section>',
        '<section aria-labelledby="downloads"><h2 id="downloads">Data and provenance</h2><p>Download the saved aggregates used on this page: <a href="/assets/arxiv/summary.json" download>statistics and SQL (JSON)</a>, <a href="/assets/arxiv/years.csv" download>annual counts</a>, <a href="/assets/arxiv/months.csv" download>monthly counts</a>, <a href="/assets/arxiv/categories.csv" download>category counts</a>, <a href="/assets/arxiv/groups.csv" download>group counts</a>, and <a href="/assets/arxiv/category_counts.csv" download>categories per work</a>.</p><p>The export includes ingestion checksums and timestamps. These are static database aggregates, not live arXiv statistics. Later snapshot loads may retain older papers absent from the new source; consult all ingestion runs in the JSON before comparing releases.</p></section>']
    summary, separator, statistics = ('\n'.join(out) + '\n').partition('</section>')
    (SITE / '_layout' / 'arxiv-summary.html').write_text(summary + separator + '\n')
    (SITE / '_layout' / 'arxiv-statistics.html').write_text(statistics.lstrip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-only', action='store_true')
    args = parser.parse_args()
    render(json.loads((ASSETS / 'summary.json').read_text()) if args.render_only else export())
