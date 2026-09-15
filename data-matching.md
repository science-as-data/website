+++
title = "Data matching"
+++

~~~
<header class="article-header wrap"><p class="eyebrow">Research area / Data matching</p><h1>Data matching</h1><p class="lede">Methods for linking records across scholarly data sources. Current documentation concerns journal matching between OpenAlex and Scopus.</p></header>
<div class="article-layout wrap">
<aside class="article-nav" aria-label="On this page"><strong>Data matching</strong><a href="#scope">Current scope</a><a href="#method">Matching method</a><a href="#interpretation">Interpretation</a><a href="#materials">Materials</a></aside>
<article class="article">
<h2 id="scope">Current scope</h2>
<p>The <a href="https://github.com/science-as-data/data-matching">Data matching repository</a> provides a dedicated home for this research area. It currently contains scope documentation. The existing journal crosswalk workflow remains under development in the OpenAlex repository. Its unit of matching is the journal or source record; this page does not document matching individual articles, authors, or institutions.</p>
<h2 id="method">Matching method</h2>
<p>The workflow uses ISSNs, normalized journal titles, and scored candidate pairs. Ambiguous pairs are routed to review. The repository guide covers source-list loading, optional API enrichment, review, and evaluation.</p>
<h2 id="interpretation">Interpretation and limitations</h2>
<p>Source coverage is time-dependent. When using the crosswalk to select works, publication years must be compared with Scopus coverage intervals. Journals can have multiple ASJC discipline assignments; retaining only the first assignment discards information.</p>
<p>A candidate match requires evaluation before it is used in an analysis. This page reports no matching accuracy estimate or validated crosswalk release.</p>
<h2 id="materials">Code and documentation</h2>
<ul><li><a href="https://github.com/science-as-data/data-matching">Data matching repository and scope</a></li><li><a href="https://github.com/science-as-data/openalex/tree/main/matching">Journal matching source code</a></li><li><a href="https://github.com/science-as-data/openalex/blob/main/matching/README.md">Workflow, review, and evaluation guide</a></li><li><a href="/queries/#crosswalk">Using Scopus disciplines in OpenAlex analyses</a></li></ul>
</article></div>
~~~
