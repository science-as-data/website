"""Export aggregate collection figures explicitly; website builds never query databases.

Run with --render-only to regenerate layouts from the saved public aggregates.
Optional connections: AEA_RCT_DSN, OSF_DSN, ASPREDICTED_DSN (never saved).
"""
import argparse
from datetime import date, datetime, timezone
import html
import json
import os
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
ASSET = SITE / 'assets/preregistrations/summary.json'
SPECS = (
    ('aea_rct', 'AEA RCT Registry', 'trials', 'first_registered_on',
     ('title', 'abstract', 'principal_investigators'), 'status'),
    ('osf', 'OSF Registries', 'registrations', 'date_registered',
     ('title', 'description', 'registration_supplement'), 'provider'),
    ('aspredicted', 'AsPredicted', 'aspredicted_registrations', 'created_date',
     ('title', 'hypothesis', 'analyses', 'sample_size'), 'source'),
)


def export():
    import psycopg
    from psycopg.rows import dict_row

    data = {'measured_at_utc': datetime.now(timezone.utc).isoformat(), 'collections': {}}
    for database, label, table, date_field, fields, group in SPECS:
        measures = ['count(*) AS stored_rows', 'count(DISTINCT id) AS distinct_ids',
                    'min(crawled_at) AS first_crawled_at', 'max(crawled_at) AS last_crawled_at']
        measures += [f"count(DISTINCT id) FILTER (WHERE nullif(btrim({field}), '') IS NOT NULL) AS with_{field}"
                     for field in (*fields, date_field)]
        queries = {
            'summary': f'SELECT {", ".join(measures)} FROM public.{table}',
            'groups': f'SELECT {group} AS label, count(*) AS stored_rows, count(DISTINCT id) AS distinct_ids '
                      f'FROM public.{table} GROUP BY 1 ORDER BY 2 DESC, 1',
            'dates': f'SELECT {date_field} AS source_date, count(*) AS stored_rows '
                     f'FROM public.{table} GROUP BY 1',
        }
        with psycopg.connect(os.environ.get(database.upper() + '_DSN',
                             f'host=localhost dbname={database} user=simone'),
                             connect_timeout=5, row_factory=dict_row) as conn:
            conn.execute('BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
            conn.execute("SET LOCAL statement_timeout = '30s'")
            conn.execute("SET LOCAL lock_timeout = '3s'")
            conn.execute("SET LOCAL TIME ZONE 'UTC'")
            summary = conn.execute(queries['summary']).fetchone()
            groups = conn.execute(queries['groups']).fetchall()
            dates = conn.execute(queries['dates']).fetchall()
        parsed, missing, invalid = [], 0, 0
        for item in dates:
            value = (item['source_date'] or '').strip()
            if not value:
                missing += item['stored_rows']
                continue
            try:
                # Older AEA records append a local time and EST/EDT suffix.
                # Compare source calendar dates without inventing UTC times.
                parsed.append(datetime.strptime(','.join(value.split(',', 2)[:2]), '%B %d, %Y').date()
                              if database == 'aea_rct' else date.fromisoformat(value[:10]))
            except ValueError:
                invalid += item['stored_rows']
        assert sum(row['stored_rows'] for row in groups) == summary['stored_rows']
        assert summary['distinct_ids'] <= summary['stored_rows']
        data['collections'][database] = {
            'label': label, 'database': database, 'table': 'public.' + table,
            'summary': summary, 'group_field': group, 'groups': groups,
            'dates': {'field': date_field, 'earliest': min(parsed) if parsed else None,
                      'latest': max(parsed) if parsed else None,
                      'missing_date_rows': missing, 'unparseable_date_rows': invalid},
            'queries': queries,
        }
    data['notes'] = [
        'Exact local database aggregates; not registry-wide totals or a fresh crawl.',
        'Each database is read in its own repeatable-read, read-only transaction.',
        'Distinct IDs are counted within platform, without cross-platform study deduplication.',
        'Field presence counts distinct IDs with a nonblank value in at least one stored observation; not a content-quality assessment.',
        'Registration/creation ranges use source calendar dates. AEA month-name dates are parsed before comparison, excluding optional time/zone suffixes after the second comma; ISO dates use their first ten characters.',
        'crawled_at is retrieval/upsert time, not registration time or a guaranteed collection-completion marker.',
        'OSF totals include all loaded providers. AsPredicted rows retain retrieval sources and archive snapshots separately.',
    ]
    ASSET.parent.mkdir(parents=True, exist_ok=True)
    ASSET.write_text(json.dumps(data, indent=2, default=str) + '\n')
    return json.loads(ASSET.read_text())


def render(data):
    collections = data['collections']
    measured = data['measured_at_utc'][:10]
    summary = ['<section class="snapshot-band project-summary"><div class="wrap">',
               '<h2>Collected registrations</h2><div class="dataset-metrics preregistration-metrics">']
    for key, *_ in SPECS:
        c = collections[key]
        summary.append(f'<div><strong>{c["summary"]["distinct_ids"]:,}</strong><span>{c["label"]} · distinct IDs</span></div>')
    summary.append(f'</div><p>Exact local database counts measured on {measured}. Records were retrieved in May 2026; '
                   'these are collection sizes, not current registry totals. <a href="#figures">Dates, counting units, and key figures</a>.</p></div></section>')
    (SITE / '_layout/preregistrations-summary.html').write_text('\n'.join(summary) + '\n')

    out = ['<section aria-labelledby="figures"><h2 id="figures">Key collection figures</h2>',
           '<p>Each platform uses its own identifiers and date fields. AsPredicted can retain several retrievals of one registration; '
           'distinct IDs count each registration once within that platform.</p>',
           '<div class="data-table-scroll"><table><thead><tr><th scope="col">Collection</th><th scope="col">Distinct IDs</th>'
           '<th scope="col">Stored rows</th><th scope="col">Registration / creation dates</th><th scope="col">Latest stored retrieval (UTC)</th>'
           '</tr></thead><tbody>']
    for key, *_ in SPECS:
        c = collections[key]
        s, d = c['summary'], c['dates']
        last = str(s['last_crawled_at'])[:10] if s['last_crawled_at'] else 'Unavailable'
        span = f'{d["earliest"]} to {d["latest"]}' if d['earliest'] else 'Unavailable'
        excluded = d['missing_date_rows'] + d['unparseable_date_rows']
        if excluded:
            span += f' ({excluded:,} rows without a parseable date)'
        out.append(f'<tr><th scope="row">{c["label"]}</th><td>{s["distinct_ids"]:,}</td><td>{s["stored_rows"]:,}</td>'
                   f'<td>{span}<br><code>{d["field"]}</code></td><td>{last}</td></tr>')
    out.append('</tbody></table></div>')
    a, o, p = [collections[k] for k in ('aea_rct', 'osf', 'aspredicted')]
    osf_providers = {row['label']: row['distinct_ids'] for row in o['groups']}
    out += [
        '<h3>AEA RCT Registry</h3>',
        '<p>The documented April 2026 Dataverse snapshot contained 11,746 source records; loading resolved three repeated IDs '
        'to 11,743 trial records. This source count and deduplication result are documented in the '
        '<a href="https://github.com/science-as-data/study-preregistrations/blob/main/aea-rct/CHANGELOG.md">collection report</a>.</p>',
        '<p>Recorded trial status: ' + '; '.join(f'{html.escape(row["label"] or "Unspecified")}: {row["distinct_ids"]:,}' for row in a['groups']) + '.</p>',
        '<h3>OSF Registries</h3>',
        f'<p>{len([r for r in o["groups"] if r["label"]])} named providers are represented. The OSF provider accounts for {osf_providers.get("osf", 0):,} registrations; '
        f'EGAP accounts for {osf_providers.get("egap", 0):,}. The headline count includes all loaded providers. '
        f'{o["summary"]["with_description"]:,} registrations have a nonblank description.</p>',
        '<h3>AsPredicted</h3>',
        f'<p>{p["summary"]["stored_rows"]:,} stored observations represent {p["summary"]["distinct_ids"]:,} distinct registration IDs. '
        f'The {p["summary"]["stored_rows"] - p["summary"]["distinct_ids"]:,} additional rows preserve repeated retrieval observations. '
        f'{p["summary"]["with_hypothesis"]:,} IDs have a nonblank hypothesis; {p["summary"]["with_analyses"]:,} have planned analyses; '
        f'{p["summary"]["with_sample_size"]:,} have a sample-size field.</p>',
        '<p>Field presence means a nonblank value in at least one stored observation; it does not establish the plan’s completeness or quality. '
        'Registration and creation dates are kept distinct from retrieval dates and study start dates.</p>',
        f'<p>Measured on {measured}. <a href="/assets/preregistrations/summary.json" download>Download aggregate counts, date ranges, SQL, and provenance (JSON)</a>. '
        'The website uses this saved export and makes no database queries.</p></section>',
    ]
    (SITE / '_layout/preregistrations-statistics.html').write_text('\n'.join(out) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-only', action='store_true')
    args = parser.parse_args()
    render(json.loads(ASSET.read_text()) if args.render_only else export())
