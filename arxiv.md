+++
title = "arXiv: data and PostgreSQL database"
+++

~~~
<section class="hero wrap project-hero" aria-labelledby="project-title">
  <div class="hero-copy">
    <p class="project-identity"><span class="project-icon project-icon-arxiv" aria-hidden="true"><img src="/assets/arxiv-mark.jpg" width="36" height="36" alt=""></span><span>arXiv</span></p>
    <h1 id="project-title">arXiv data for research</h1>
    <p class="hero-description">The Cornell arXiv snapshot contains paper metadata, author names, subject categories, and submission versions.</p>
    <p class="hero-description">The pipeline resolves repeated identifiers and loads the records into linked PostgreSQL tables. Source values, version timestamps, and ingestion records remain available for inspection.</p>
    <p class="hero-description">The database supports selection by subject and submission date, analysis of revision timing, and reproducible counts. Bulk PDF and source-file workflows remain planned.</p>
    <div class="hero-actions"><a class="button" href="#database">Database structure <span aria-hidden="true">↗</span></a><a class="text-link" href="#time">Submission statistics <span aria-hidden="true">↗</span></a></div>
  </div>
  <figure class="transformation process-figure" aria-labelledby="process-title">
    <figcaption class="figure-topline" id="process-title">FROM SOURCE RECORDS TO RESEARCH DATA</figcaption>
    <div class="process-input"><h2>Input: arXiv metadata snapshot</h2><p>arxiv_id · title · abstract</p><p>authors · categories · versions</p></div>
    <div class="transform-connector"><span class="connector-line" aria-hidden="true"></span><span>RESOLVE IDS → LOAD → INDEX</span><span class="process-arrow" aria-hidden="true">↓</span></div>
    <div class="process-outputs" aria-label="Outputs"><div class="process-output"><h3>papers</h3><p>One record per arXiv ID</p></div><div class="process-output"><h3>paper_authors</h3><p>Ordered author names</p></div><div class="process-output"><h3>paper_categories</h3><p>Subject assignments</p></div><div class="process-output"><h3>paper_versions</h3><p>Submission timestamps</p></div></div>
    <p class="figure-note">Relationships use arXiv IDs. Author occurrences do not identify unique researchers.</p>
  </figure>
</section>
<div class="snapshot-band project-summary"><div class="wrap">
~~~

{{insert arxiv-summary.html}}

~~~
</div></div>
<section class="section wrap project-workflow" aria-labelledby="workflow-title"><div class="section-heading"><h2 id="workflow-title">Data processing workflow</h2></div><div class="workflow-grid"><a class="workflow-step" href="#downloads"><span class="step-index">01 <span aria-hidden="true">↗</span></span><h3>Read snapshot</h3><p>Read metadata and record the dataset version and checksum.</p></a>
<a class="workflow-step" href="#database"><span class="step-index">02 <span aria-hidden="true">↗</span></span><h3>Resolve duplicates</h3><p>Retain repeated-ID events and apply the documented selection rule.</p></a>
<a class="workflow-step" href="#database"><span class="step-index">03 <span aria-hidden="true">↗</span></span><h3>Load tables</h3><p>Separate authors, categories, and versions into linked tables.</p></a>
<a class="workflow-step" href="#time"><span class="step-index">04 <span aria-hidden="true">↗</span></span><h3>Analyze</h3><p>Select records and aggregate by submission date or category.</p></a></div></section>
<nav class="project-sections wrap" aria-label="arXiv project sections"><strong>In this section</strong><a href="#arxiv-counts">Dataset size</a><a href="#time">Works over time</a><a href="#categories">Subjects and categories</a><a href="#database">Database structure</a><a href="#downloads">Download statistics</a><a href="#scope">Scope and interpretation</a><a href="https://github.com/science-as-data/arxiv">Repository ↗</a></nav>
<div class="wrap project-details"><article class="article">

~~~

{{insert arxiv-statistics.html}}

~~~
<section aria-labelledby="database"><h2 id="database">Database structure</h2><p>The dedicated <code>arxiv</code> PostgreSQL database uses the <code>arxiv</code> schema. A text <code>arxiv_id</code> connects a paper to its ordered authors, categories, versions, and retained source object. Text IDs preserve legacy identifiers such as <code>hep-th/9901001</code>.</p>
<div class="data-table-scroll"><table class="arxiv-schema-table"><thead><tr><th scope="col">Table</th><th scope="col">Unit and key</th><th scope="col">What it preserves</th></tr></thead><tbody>
<tr><th scope="row"><code>papers</code></th><td>One work · arxiv_id</td><td>Title, abstract, original author string, DOI, journal reference, license, metadata update and submission dates.</td></tr>
<tr><th scope="row"><code>paper_authors</code></th><td>Author occurrence · arxiv_id + author_position</td><td>Ordered name components, including suffixes. These are occurrences, not disambiguated people.</td></tr>
<tr><th scope="row"><code>paper_categories</code></th><td>Assignment · arxiv_id + category_position</td><td>Every supplied subject code and its source position, including cross-listings.</td></tr>
<tr><th scope="row"><code>paper_versions</code></th><td>Version · arxiv_id + version</td><td>Integer version number and timezone-aware submission timestamp.</td></tr>
<tr><th scope="row"><code>raw_records</code></th><td>Source object · arxiv_id</td><td>Selected JSON values as JSONB and the ingestion run that supplied them.</td></tr>
<tr><th scope="row"><code>duplicate_records</code></th><td>Repeat event · ingestion_run_id + source_record_number</td><td>Previous and incoming objects, plus the selection decision.</td></tr>
<tr><th scope="row"><code>ingestion_runs</code></th><td>Load · run_id</td><td>Dataset version, checksum, source manifest, progress, timestamps, and completion status.</td></tr>
</tbody></table></div>
<p>Foreign keys enforce links to papers and ingestion runs. Indexes support metadata-update and first-submission filters, DOI lookup, and category-to-paper joins. The loader commits batches with resumable checkpoints. Repeated IDs are resolved using the newest metadata update date, then the later file position for ties.</p>
<p><a href="https://github.com/science-as-data/arxiv/blob/main/kaggle/sql/schema.sql">Read the schema</a> · <a href="https://github.com/science-as-data/arxiv/blob/main/kaggle/sql/examples.sql">Query examples</a> · <a href="https://github.com/science-as-data/arxiv/blob/main/kaggle/README.md">Loading and verification</a></p></section>
<section aria-labelledby="scope"><h2 id="scope">Scope and interpretation</h2><p>This is a metadata snapshot. Text preserves Unicode, LaTeX, and line breaks. The source does not supply a citation graph or disambiguated affiliations. Version timestamps do not reconstruct past titles, abstracts, or author lists, and <code>update_date</code> records metadata changes.</p><p>OAI-PMH synchronization and bulk PDF and TeX/source workflows remain planned in the arXiv repository. A general OpenAlex–arXiv matcher belongs to <a href="/data-matching/">Data matching</a> and remains planned. The <a href="/openalex/#quality">OpenAlex date audit</a> has separately checked arXiv histories for nine sampled works; that limited exercise is not a database-wide crosswalk. Source JSON bytes remain in the original snapshot; JSONB retains values but changes whitespace and key ordering.</p><p>Code is MIT-licensed. The Cornell dataset assigns CC0 to its metadata; individual articles retain their own licenses.</p></section>
</article></div>
~~~
