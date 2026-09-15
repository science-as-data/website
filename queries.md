+++
title = "Research queries"
+++

~~~
<header class="article-header wrap"><p class="eyebrow">03 / Research queries</p><h1>SQL examples and analytical choices</h1><p class="lede">Copy a query, adapt the sample, and run it against your local database. These examples use the repository’s actual schema; they do not execute in your browser.</p></header>
<div class="article-layout wrap"><aside class="article-nav" aria-label="On this page"><strong>Query notebook</strong><a href="#examples">Explore the examples</a><a href="#practice">Research practice</a><a href="#crosswalk">Add Scopus disciplines</a><a href="#faq">Common questions</a></aside><article class="article">
~~~

\label{examples}
## Example queries

Choose a starting point. All examples use completed publication years, explicit joins, and a stated unit of analysis. Runtime depends on hardware, indexes, and the query plan; aggregations over works may scan a substantial portion of the database.

{{insert query-examples.html}}

\label{practice}
## Make the analysis reproducible

Before exporting results, record the snapshot release, repository revision, exact SQL, and inclusion rules. Inspect coverage by publication year, language, and source type rather than treating the database as a complete census of science.

- **Define your denominator.** Articles, all work types, and journal-only records are different populations.
- **Respect multiplicity.** Count works distinctly after joins to authors, affiliations, or multiple topics. Fractional counting may be more appropriate for some questions.
- **Treat missingness explicitly.** Missing affiliations and unresolved citation targets are not evidence of no collaboration or no citations.
- **Separate publication time from observation time.** Citations and open-access status reflect the snapshot, not necessarily the year of publication. The [publication-date audit](/openalex/#quality) also distinguishes journal events, preprint histories, partial dates, and unresolved evidence.
- **Inspect performance first.** `EXPLAIN` estimates a plan; `EXPLAIN ANALYZE` actually runs the query. Start with smaller cohorts where possible.

\label{crosswalk}
## Add Scopus disciplines

The OpenAlex repository’s `matching/` tools build an OpenAlex–Scopus journal crosswalk using ISSNs, normalized titles, and scored candidate pairs. It is an extension under development, with ambiguous pairs routed to review.

Source coverage is time-dependent: when sampling works, join publication year to the Scopus coverage interval. Keep all ASJC discipline assignments; choosing the first code discards information. The [matching guide](https://github.com/science-as-data/openalex/blob/main/matching/README.md) documents source-list loading, optional API enrichment, review, and evaluation. The organization’s broader linkage scope and other implemented routes are documented under [Data matching](/data-matching/).

\label{faq}
## Common questions

~~~
<details><summary>Do I need to load the full snapshot to get started?</summary><p>No. Use the repository’s <a href="https://github.com/science-as-data/openalex/tree/main/api">API tools and examples</a> for lookups and exploratory work. The snapshot protocol is useful for broad, repeated analyses across the record. The smoke test validates a sample of the loading pipeline.</p></details>
<details><summary>Can I run these SQL queries on the OpenAlex API?</summary><p>No. They target the PostgreSQL schema created by this repository. The OpenAlex API has its own filters and pagination, documented in the <a href="https://github.com/science-as-data/openalex/blob/main/api/api-reference.md">API reference</a>.</p></details>
<details><summary>Are the displayed numbers live results?</summary><p>No. The OpenAlex overview reports the repository’s documented reference snapshot measurements and storage estimate. The examples here provide SQL and interpretation, without fabricated output or browser access to a database.</p></details>
<details><summary>How should I acknowledge the tools and data?</summary><p>Identify OpenAlex as the data source and record the snapshot release. Link to <a href="https://github.com/science-as-data/openalex">this repository</a> and the commit used to build your database. Include your study’s SQL and sampling decisions so others can reproduce the analysis.</p></details>
<div class="next-page"><a href="/protocol/">Build your research database →</a><a href="https://github.com/science-as-data/openalex">Explore the repository ↗</a></div></article></div>
~~~
