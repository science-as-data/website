+++
title = "arXiv: curated full text and PostgreSQL database"
+++

~~~
<section class="hero wrap project-hero" aria-labelledby="project-title">
  <div class="hero-copy">
    <p class="project-identity"><span class="project-icon project-icon-arxiv" aria-hidden="true"><img src="/assets/arxiv-mark.jpg" width="36" height="36" alt=""></span><span>arXiv</span></p>
    <h1 id="project-title">From bulk sources to a research database</h1>
    <p class="hero-description">At the centre of this project is a PostgreSQL database built from arXiv bulk source files. It brings paper texts and bibliography evidence into a relational structure connected to the Cornell metadata dump distributed through Kaggle.</p>
    <p class="hero-description">The essential work is curation: unpacking heterogeneous archives, parsing TeX and BibTeX files, preserving rendered bibliography text, and recording where each observation came from.</p>
    <p class="hero-description">Researchers can move from a paper’s metadata to its stored source files, inspect its bibliography, and trace the processing decisions behind the data.</p>
    <div class="hero-actions"><a class="button" href="#database">Explore the relational structure <span aria-hidden="true">↗</span></a><a class="text-link" href="#curation">TeX and bibliography curation <span aria-hidden="true">↗</span></a></div>
  </div>
  <figure class="transformation process-figure" aria-labelledby="process-title">
    <figcaption class="figure-topline" id="process-title">THE DATABASE IS THE RESEARCH ASSET</figcaption>
    <div class="process-input"><h2>Bulk paper sources</h2><p>Nested archives · TeX / LaTeX</p><p>BibTeX · rendered .bbl bibliographies</p></div>
    <div class="transform-connector"><span class="connector-line" aria-hidden="true"></span><span>CURATE → PARSE → VERIFY</span><span class="process-arrow" aria-hidden="true">↓</span></div>
    <div class="arxiv-database-hub"><h2>PostgreSQL · arxiv</h2><p>Source observations → file inventory → stored text</p><p>Archive provenance · parser builds · verification</p></div>
    <div class="arxiv-metadata-join"><span aria-hidden="true">↕</span><p><strong>Connected by arXiv ID</strong><br>Kaggle metadata: papers, authors, categories, versions</p></div>
    <p class="figure-note">One database, two connected schemas. Multiple source observations can belong to the same paper.</p>
  </figure>
</section>
<section class="section wrap project-workflow" aria-labelledby="workflow-title">
  <div class="section-heading"><h2 id="workflow-title">Making bulk sources usable</h2></div>
  <div class="workflow-grid">
    <a class="workflow-step" href="#bulk"><span class="step-index">01 <span aria-hidden="true">↗</span></span><h3>Acquire and identify</h3><p>Pin the source release, verify downloaded bytes, and retain archive provenance.</p></a>
    <a class="workflow-step" href="#curation"><span class="step-index">02 <span aria-hidden="true">↗</span></span><h3>Curate and parse</h3><p>Recover paper files, preserve TeX and bibliography text, and record exceptions.</p></a>
    <a class="workflow-step" href="#database"><span class="step-index">03 <span aria-hidden="true">↗</span></span><h3>Load and connect</h3><p>Store source observations and text; join them to the Kaggle catalogue by arXiv ID.</p></a>
    <a class="workflow-step" href="#references"><span class="step-index">04 <span aria-hidden="true">↗</span></span><h3>Verify and investigate</h3><p>Check counts and content hashes, then inspect the evidence for text and citation analysis.</p></a>
  </div>
</section>
<nav class="project-sections wrap" aria-label="arXiv project sections"><strong>In this section</strong><a href="#bulk">Bulk data asset</a><a href="#curation">TeX and BibTeX curation</a><a href="#database">Relational structure</a><a href="#references">Bibliography evidence</a><a href="#arxiv-counts">Metadata coverage</a><a href="#time">Works over time</a><a href="#categories">Subjects and categories</a><a href="#downloads">Download statistics</a><a href="#scope">Scope and interpretation</a><a href="https://github.com/science-as-data/arxiv">Repository ↗</a></nav>
<div class="wrap project-details"><article class="article">

<section aria-labelledby="bulk">
  <h2 id="bulk">A database built from difficult bulk data</h2>
  <p>The bulk collection contains the material from which papers and their bibliographies are produced. It is also difficult to manage: a downloaded archive can contain thousands of compressed paper bundles, each with its own file layout, encodings, macros, bibliography files, and figures. Downloading the collection is only the beginning of making it usable for research.</p>
  <p>The database organizes this material into identifiable source observations, file inventories, and stored text. Resumable loading handles large batches; hashes identify repeated content; independent verification checks that records and text survive the transformation. Each source observation remains connected to the archive and parser configuration that produced its stored representation.</p>
  <p>The implemented source-tar workflow has been exercised on <a href="https://huggingface.co/datasets/TIGER-Lab/arxiv-latex-5T">TIGER-Lab source archives</a>. <a href="https://info.arxiv.org/help/bulk_data_s3.html">arXiv’s official bulk service</a> provides source archives separately. The <a href="https://huggingface.co/datasets/scholarweave/arxiv-latex">Scholarweave collection</a> provides processed, bundled LaTeX in Parquet; this requires a separate ingestion adapter and is not interchangeable with original source-file bytes.</p>
  <div class="callout"><strong>Documented validation · 17 September 2026.</strong> Three early-2000 source archives were loaded and independently verified: 7,329 paper-source records, including 7,094 with parsed text, and 9,438 distinct stored text contents. All 7,329 IDs joined to the metadata catalogue. This bounded validation establishes the pipeline’s operation; corpus-wide text and bibliography coverage require separate measurement.</div>
</section>

<section aria-labelledby="curation">
  <h2 id="curation">Curation and parsing of TeX and BibTeX</h2>
  <p>The contribution is the conversion of heterogeneous files into research observations that can be inspected and reproduced. The parser reads nested paper bundles, normalizes legacy identifiers such as <code>astro-ph0001001</code> to <code>astro-ph/0001001</code>, inventories their contents, and records the outcome for each paper.</p>
  <div class="arxiv-curation-grid">
    <div><h3>Preserve the paper’s text</h3><p>Retain TeX/LaTeX files and supporting text with original paths, archive order, byte sizes, and hashes. Keep decoding choices explicit, including a reversible fallback for non-UTF-8 text. Repeated filenames remain separate file occurrences.</p></div>
    <div><h3>Recover bibliography evidence</h3><p>Preserve <code>.bib</code> entries, rendered <code>.bbl</code> bibliography text, and references embedded in TeX through <code>\bibitem</code> or <code>thebibliography</code>. These complementary forms retain citation keys, bibliographic fields, and the wording available in the paper’s sources.</p></div>
    <div><h3>Make exceptions visible</h3><p>Distinguish parsed papers, PDF-only submissions, unsupported formats, bundles without usable text, and errors. Record warnings and omissions alongside successful results so a failed extraction cannot silently become an empty bibliography.</p></div>
    <div><h3>Verify what was stored</h3><p>Fingerprint the parser and its settings; reconcile batch totals and record digests; reconstruct stored text bytes to check their hashes. Retain source observations separately even when their identical text is stored only once.</p></div>
  </div>
  <p>The default policy retains all parsed text, including TeX, BibTeX, bibliography, and style files. An explicit bibliography-only policy retains selected text while keeping an inventory and hashes for omitted text files. Binary figures and PDFs are inventoried; their payloads are not stored in these text tables. Source parsing does not execute TeX or compile articles.</p>
</section>

<section aria-labelledby="database">
  <h2 id="database">Relational schematic: bulk sources and metadata</h2>
  <p>The <code>arxiv</code> PostgreSQL database contains two schemas: <code>arxiv_source</code> holds the curated bulk-source material; <code>arxiv</code> holds the Kaggle metadata catalogue. A work, a source observation, a file occurrence, and a distinct text content have separate identities. This preserves multiple observations of a paper while avoiding duplicate storage of identical text.</p>
  <figure class="arxiv-relational-figure" aria-labelledby="arxiv-schema-caption">
    <div class="arxiv-schema-heading"><strong>PostgreSQL database: <code>arxiv</code></strong><span><code>arxiv_source</code> · bulk sources ↔ <code>arxiv</code> · Kaggle metadata</span></div>
    <div class="arxiv-diagram-scroll" tabindex="0" role="region" aria-label="Relational diagram; scroll horizontally on small screens">
      <img src="/assets/arxiv/relational-structure.svg" width="1100" height="740" alt="Bulk-source batches contain paper records, which own source-file occurrences linked to deduplicated text. Paper records join by arXiv ID to the Kaggle papers table, whose children hold authors, categories, versions, and raw metadata. Solid lines denote foreign keys; the dashed metadata connection is an optional exact-ID join.">
    </div>
    <figcaption id="arxiv-schema-caption">The core relationships across both schemas. Solid lines show foreign keys and cardinalities; the dashed connection matches source observations to metadata by <code>arxiv_id</code>. <a href="/assets/arxiv/relational-structure.svg">Open the overview diagram</a>.</figcaption>
  </figure>
  <details class="arxiv-complete-schema"><summary>Complete relational schematic · all 19 tables, provenance, verification, and the joining view</summary>
    <p>Follow a stored TeX or BibTeX file through its source record, parser batch, and archive provenance, or across to the paper’s metadata. Solid arrows point from a foreign key to its referenced table. The dashed line is the optional arXiv-ID match; dotted lines show the view’s inputs. Composite foreign keys are labelled together.</p>
    <figure class="arxiv-relational-figure">
      <div class="arxiv-diagram-scroll arxiv-complete-scroll" tabindex="0" role="region" aria-label="Complete relational schematic; scroll horizontally to inspect all tables">
        <img src="/assets/arxiv/relational-structure-complete.svg" alt="Complete arxiv database schematic with all twelve arxiv_source tables, all seven arxiv metadata tables, their foreign keys, and the papers_with_sources left-join view. Source observations connect to metadata by arxiv_id; archive provenance, parsing, content storage, verification, and local-copy lifecycle are shown.">
      </div>
      <figcaption><a href="/assets/arxiv/relational-structure-complete.svg">Open the complete schematic at full size</a> · <a href="/assets/arxiv/relational-structure-complete.svg" download>Download SVG</a> · <a href="/assets/arxiv/relational-structure-complete.dot" download>Diagram source (Graphviz)</a>. Keys and relationships follow the implemented SQL definitions; cleanup tables are schema provisions, with automated deletion disabled.</figcaption>
    </figure>
  </details>
  <p>The view <code>arxiv_source.papers_with_sources</code> uses a left join on <code>arxiv_id</code>. There is deliberately no mandatory foreign key from source records to the catalogue: unknown or unmatched IDs remain available, with <code>metadata_matched = false</code>. A source version is recorded only with explicit evidence; the metadata version history does not identify the version of an unlabelled source file.</p>
  <h3>Bulk-source tables · <code>arxiv_source</code></h3>
  <div class="data-table-scroll"><table class="arxiv-schema-table"><thead><tr><th scope="col">Table</th><th scope="col">Row identity</th><th scope="col">What it connects and preserves</th></tr></thead><tbody>
    <tr><th scope="row"><code>paper_records</code></th><td><code>record_id</code>; unique batch + record number</td><td>One source occurrence, linked to its batch: arXiv ID, evidenced version, archive member, status, hashes, and diagnostics.</td></tr>
    <tr><th scope="row"><code>source_files</code></th><td><code>record_id + file_number</code></td><td>One file occurrence: path, order, kind, retention decision, decoding, bibliography markers, and a stored or omitted text hash.</td></tr>
    <tr><th scope="row"><code>text_contents</code></th><td><code>content_sha256</code></td><td>One distinct source-text byte sequence, shared by matching file occurrences; checked byte length and reversible decoding.</td></tr>
    <tr><th scope="row"><code>ingestion_batches</code></th><td><code>batch_id</code>; unique input hash + parser fingerprint</td><td>Input and parsed-output artifacts, parser build, expected totals, resumable checkpoints, and loading/verification state.</td></tr>
    <tr><th scope="row"><code>parser_builds</code></th><td><code>parser_fingerprint</code></td><td>Parser code hash, configuration, and text-retention policy.</td></tr>
    <tr><th scope="row"><code>source_snapshots</code></th><td><code>snapshot_id</code></td><td>Provider, repository, pinned revision, and saved manifest.</td></tr>
    <tr><th scope="row"><code>artifacts</code></th><td><code>artifact_sha256</code></td><td>Identity, size, and kind of downloaded or generated bytes.</td></tr>
    <tr><th scope="row"><code>snapshot_files</code></th><td><code>snapshot_id + remote_path</code></td><td>Provider snapshot file linked to its artifact hash and upstream checksum claims.</td></tr>
    <tr><th scope="row"><code>verification_receipts</code></th><td><code>verification_id</code></td><td>Independent batch checks: totals, record digests, stored contents, and metadata join coverage.</td></tr>
    <tr><th scope="row"><code>record_resolutions</code></th><td><code>record_id</code></td><td>Explicit resolution of an unusable record, with a reason or a link to a reprocessed replacement.</td></tr>
    <tr><th scope="row"><code>local_copies</code></th><td><code>copy_id</code></td><td>Artifact linked to a local copy and, where available, the provider snapshot file.</td></tr>
    <tr><th scope="row"><code>cleanup_receipts</code></th><td><code>copy_id</code></td><td>Schema provision linking a copy to verification and backup evidence. Automated deletion is not enabled.</td></tr>
  </tbody></table></div>
  <details class="arxiv-metadata-tables"><summary>Metadata tables · arxiv · seven tables connected to the bulk-source records</summary>
    <div class="data-table-scroll"><table class="arxiv-schema-table"><thead><tr><th scope="col">Table</th><th scope="col">Row identity</th><th scope="col">What it preserves</th></tr></thead><tbody>
      <tr><th scope="row"><code>papers</code></th><td><code>arxiv_id</code></td><td>Title, abstract, original author string, DOI, journal reference, license, metadata update date, and derived first/latest submission dates.</td></tr>
      <tr><th scope="row"><code>paper_authors</code></th><td><code>arxiv_id + author_position</code></td><td>Ordered author names, including suffixes. Occurrences do not identify unique researchers.</td></tr>
      <tr><th scope="row"><code>paper_categories</code></th><td><code>arxiv_id + category_position</code></td><td>Subject codes and source order, including cross-listings.</td></tr>
      <tr><th scope="row"><code>paper_versions</code></th><td><code>arxiv_id + version</code></td><td>Version numbers and timezone-aware submission timestamps.</td></tr>
      <tr><th scope="row"><code>raw_records</code></th><td><code>arxiv_id</code></td><td>Selected source JSON values as JSONB and their ingestion run.</td></tr>
      <tr><th scope="row"><code>duplicate_records</code></th><td><code>ingestion_run_id + source_record_number</code></td><td>Repeated-ID observations, previous and incoming objects, and selection decisions.</td></tr>
      <tr><th scope="row"><code>ingestion_runs</code></th><td><code>run_id</code></td><td>Dataset version, checksum, manifest, progress, timestamps, and completion status.</td></tr>
    </tbody></table></div>
    <p>Metadata child tables use foreign keys to <code>papers</code>; load provenance uses <code>ingestion_runs</code>. Repeated IDs are resolved using the newest metadata update date, then the later file position for ties. Text IDs preserve legacy forms such as <code>hep-th/9901001</code>.</p>
  </details>
  <p><a href="https://github.com/science-as-data/arxiv/tree/main/huggingface">Bulk-source workflow</a> · <a href="https://github.com/science-as-data/arxiv/blob/main/kaggle/sql/schema.sql">Metadata schema</a> · <a href="https://github.com/science-as-data/arxiv/blob/main/kaggle/sql/examples.sql">Metadata query examples</a></p>
</section>

<section aria-labelledby="references">
  <h2 id="references">From bibliography evidence to citation analysis</h2>
  <p>Keeping the full source text and bibliography material in PostgreSQL makes citation analysis inspectable. A researcher can select papers by metadata, retrieve their TeX and BibTeX files, inspect rendered bibliography text, and return to the original evidence when an extraction or match is uncertain.</p>
  <p>The file forms answer different questions. A <code>.bib</code> file can contain entries never used by the paper. A supplied <code>.bbl</code> or inline TeX bibliography records a rendered reference list, while citation commands show where keys occur in the text. Reconstructing citations requires interpreting these together, including file dependencies and macros.</p>
  <p>The implemented bulk parser preserves these materials and detects bibliography markers. Structured reference occurrences, in-text citation mentions, and resolved target works require a further extraction and linkage layer; marker counts alone are not citation edges. Cross-source resolution belongs to <a href="/data-matching/">Data matching</a>, with OpenAlex as the central hub for connecting work identifiers while retaining the original bibliography evidence.</p>
</section>
~~~

{{insert arxiv-summary.html}}

{{insert arxiv-statistics.html}}

~~~
<section aria-labelledby="scope">
  <h2 id="scope">Scope and interpretation</h2>
  <p>Metadata coverage, usable source-text coverage, and validated bibliography coverage have different denominators. The statistics above describe the Kaggle metadata catalogue. They do not establish that every catalogued work has a parsed full text or complete reference list. Source-tar validation is dated separately; mirror completeness and equivalence to the official bulk collection remain unestablished.</p>
  <p>Submission timestamps must be distinguished from public announcement or release times. Metadata histories do not reconstruct earlier titles, author lists, or bibliographies, and <code>update_date</code> records metadata changes. Temporal citation studies must establish which source version is observed and when candidate papers became available.</p>
  <p>A general OpenAlex–arXiv crosswalk remains planned in <a href="/data-matching/">Data matching</a>. The <a href="/openalex/#quality">OpenAlex date audit</a> separately checked nine sampled arXiv histories. OAI-PMH synchronization remains planned. Dataset and article reuse conditions are recorded separately: code is MIT-licensed; individual papers retain their own licenses.</p>
</section>
</article></div>
~~~
