+++
title = "The schema"
+++

~~~
<header class="article-header wrap"><h1>Keep the connections.<br>Make them queryable.</h1><p class="lede">Entities become tables. Nested arrays become relationships. The result is an explicit data model for moving between works, authors, institutions, and ideas.</p></header>
<div class="article-layout wrap"><aside class="article-nav" aria-label="On this page"><strong>In this guide</strong><a href="#model">The relational model</a><a href="#join">Join paths</a><a href="#identifiers">IDs &amp; nested values</a><a href="#source">One source of truth</a><a href="#limits">Model boundaries</a></aside><article class="article">
~~~

\label{model}
## A work at the center

The tables live in the PostgreSQL `openalex` schema. A main table stores each entity’s scalar fields; child tables retain repeated relationships. For example, a work with several authors and several topics has multiple authorship and topic rows, without repeating its title and publication date.

~~~
<div class="schema-map" role="img" aria-label="Works connect to authors through works_authorships, topics through works_topics, and other works through works_referenced_works."><div class="schema-node central">works<small>id · title · publication_year</small></div><span class="schema-arrow">→</span><div class="schema-node">works_authorships<small>work_id · author_id → authors</small></div><span class="schema-arrow">→</span><div class="schema-node">works_topics<small>work_id · topic_id → topics</small></div><span class="schema-arrow">→</span><div class="schema-node">works_referenced_works<small>work_id · referenced_work_id → works</small></div></div>
~~~

The model also includes sources, institutions, publishers, funders, awards, keywords, and the domain–field–subfield–topic hierarchy. [Browse real records and all 50 tables](/preview/) in the static dataset preview. Consult the [full database diagram](https://github.com/science-as-data/openalex/blob/main/datadump/db_schema.svg) and [generated schema SQL](https://github.com/science-as-data/openalex/blob/main/datadump/scripts/sql/01_create_schema.sql) for the complete inventory.

\label{join}
## Choose the relationship you need

| Research relationship | Join path |
| :--- | :--- |
| Work → author | `works.id → works_authorships.work_id`; then `author_id → authors.id` |
| Work → institution | `works.id → works_authorship_institutions.work_id`; then `institution_id → institutions.id` |
| Work → primary venue | `works.primary_location_source_id → sources.id` |
| Work → primary topic | `works.primary_topic_id → topics.id` |
| Work → all topics | `works.id → works_topics.work_id`; then `topic_id → topics.id` |
| Work → cited work | `works.id → works_referenced_works.work_id`; `referenced_work_id` identifies the cited work |
| Work → open access | `works.id → works_open_access.work_id` |

### Watch the unit of analysis

Joining authors and topics can multiply rows: three authors and four topics may yield twelve rows for the same work. Use `EXISTS` for membership filters, or deduplicate the relevant identifiers before counting. Use `COUNT(DISTINCT w.id)` when your intended unit is a work.

The following retrieves recent journal articles using a single primary venue per work:

```sql
SELECT w.id, w.title, w.publication_year,
       s.display_name AS journal
FROM openalex.works AS w
JOIN openalex.sources AS s
  ON s.id = w.primary_location_source_id
WHERE w.publication_year = 2024
  AND w.type = 'article'
  AND s.type = 'journal'
ORDER BY w.id
LIMIT 25;
```

\label{identifiers}
## Stable identifiers, flexible nested values

IDs are stored as full OpenAlex URLs, such as `https://openalex.org/W2741809807`. Join the stored IDs directly; do not strip the URL prefix on one side of a join.

Not every nested value needs a child table. Variable structures such as `abstract_inverted_index`, `apc_list`, institution `lineage`, and source `issn` remain `jsonb`. Use PostgreSQL’s JSON operators when you need them. Abstracts remain inverted indexes, not reconstructed prose.

\label{source}
## One schema definition drives the pipeline

`datadump/scripts/oa_schema.py` defines ordered table columns, SQL types, extractors, and post-load indexes. `flatten.py` reads it to write CSVs; `gen_sql.py` reads it to generate database SQL.

When extending the model, keep extractor keys exactly aligned with column names. A mismatched key can silently become `NULL`. Regenerate the committed files from `datadump/scripts/`:

```bash
python gen_sql.py schema > sql/01_create_schema.sql
python gen_sql.py indexes > sql/02_create_indexes.sql
```

Update `sql/03_add_foreign_keys.sql` and `datadump/db_schema.svg` by hand when relationships change, then run the integration smoke test described in [the protocol](/protocol/#verify).

\label{limits}
## Know the model’s boundaries

- The standard-format snapshot replaced work grants with the `awards` entity and `works_awards` links. `works_grants` is intentionally absent.
- Legacy concept ancestor, related-concept, and yearly-count child tables are omitted because their arrays are no longer populated in the targeted format. Use the topic hierarchy for current classification.
- Small flat lookup lists shipped in the snapshot are not loaded by this pipeline.
- Snapshot references can point to missing records. Inner joins omit these rows; use left joins when missingness matters to your study.
- The separately maintained foreign-key script uses `NOT VALID`, so it does not validate existing snapshot rows. Once added, such constraints still check new writes; they are not a guarantee of complete historical referential integrity.

~~~
<div class="next-page"><a href="/queries/">Next: research queries →</a><a href="https://github.com/science-as-data/openalex/blob/main/datadump/scripts/oa_schema.py">Read the schema definition ↗</a></div></article></div>
~~~
