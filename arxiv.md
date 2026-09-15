+++
title = "arXiv: preprint metadata"
+++

~~~
<header class="article-header wrap"><p class="eyebrow">Project / arXiv</p><h1>arXiv metadata workflow</h1><p class="lede">A workflow for loading versioned Cornell arXiv metadata snapshots into PostgreSQL. The data model includes papers, author occurrences, categories, revisions, and provenance.</p></header>
<div class="article-layout wrap">
<nav class="article-nav" aria-label="arXiv project sections"><strong>arXiv</strong><a href="#outputs">Project outputs</a><a href="#workflow">The workflow</a><a href="#scope">Current scope</a><a href="https://github.com/science-as-data/arxiv">Repository ↗</a></nav>
<article class="article">
<h2 id="outputs">Project outputs</h2>
<p>The loader organizes papers, ordered author occurrences, categories, revisions, and provenance in a dedicated PostgreSQL database. A snapshot downloader and profiler support inspection and repeatable loading.</p>
<p><a href="https://github.com/science-as-data/arxiv/tree/main/kaggle">Explore the metadata tools and documentation ↗</a></p>
<h2 id="workflow">The workflow</h2>
<ol><li>Download and retain a versioned Cornell arXiv JSON snapshot from Kaggle.</li><li>Profile the source records before loading.</li><li>Load the metadata into PostgreSQL while preserving source text and provenance.</li><li>Verify the load with the project’s checks and integration tests.</li></ol>
<p><a href="https://github.com/science-as-data/arxiv/blob/main/kaggle/README.md">Follow the Kaggle workflow ↗</a></p>
<h2 id="scope">Current scope</h2>
<p>The available workflow covers metadata snapshots. Official OAI-PMH harvesting and bulk PDF and TeX/source archive workflows are planned. This website currently hosts an interactive data preview for OpenAlex; arXiv outputs are documented in the repository.</p>
<p>The code uses the MIT license. The Cornell dataset assigns CC0 to its metadata; individual articles retain their own licenses.</p>
<a class="next-page" href="/openalex/"><span>Explore another project</span><strong>OpenAlex →</strong></a>
</article></div>
~~~
