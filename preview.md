+++
title = "Dataset preview"
+++

~~~
<header class="article-header wrap"><h1>OpenAlex metadata sample</h1><p class="lede">A static export of 80 works and linked metadata across 10 tables. This block sample illustrates the database structure and is not representative of OpenAlex coverage or research activity.</p><div class="preview-header-links"><a class="text-link" href="#sample">Browse the sample ↓</a><a class="text-link" href="#catalog">Explore all 50 tables ↓</a><a class="text-link" href="/assets/preview/dataset.json" download>Download the sample JSON ↓</a></div></header>
<section class="wrap preview-section" id="sample" aria-label="Dataset sample">
~~~

{{insert dataset-preview.html}}

~~~
<noscript><p class="callout">All sampled works are shown above. Enable JavaScript to search, sort, page through related tables, and inspect linked records. The complete sample is also available in the JSON download.</p></noscript>
</section>
<section class="wrap preview-catalog" id="catalog" aria-labelledby="catalog-title"><div class="section-heading"><div><h2 id="catalog-title">Table and column inventory</h2></div><a class="text-link" href="/schema/">Understand the join paths →</a></div><p class="catalog-intro">The inventory below comes from the local PostgreSQL catalog. Row totals are planner estimates captured at export, not exact counts or sample sizes. Open a table to inspect its columns.</p>
<label class="catalog-search-label" hidden>Find a table or column<input id="catalog-search" type="search" placeholder="Try works, affiliation, or country_code" autocomplete="off"></label><p id="catalog-count" class="sr-only" role="status" aria-live="polite"></p>
~~~

{{insert dataset-catalog.html}}

~~~
</section>
<section class="wrap preview-notes"><div><h2>Sampling and interpretation</h2></div><div><p>This is a static export, not a live database connection. Searches and sorting operate only on the downloaded sample. It is useful for understanding the data model, not estimating research trends or database coverage.</p><p>Missing titles, unresolved links, and uneven metadata are preserved. Full OpenAlex IDs remain in the downloads; the browser shortens them for readability. Author and source counts refer to their database records, not the number of rows in this sample.</p><a class="text-link" href="/queries/">SQL examples and interpretation →</a></div></section>
~~~
