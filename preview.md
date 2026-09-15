+++
title = "Dataset preview"
+++

~~~
<header class="article-header wrap"><p class="eyebrow">Inside the database</p><h1>A small window into<br>the scholarly record.</h1><p class="lede">Explore actual records from the loaded OpenAlex database. Follow a work to its authors, institutions, and topics—or inspect the tables that hold it all together.</p><div class="preview-header-links"><a class="text-link" href="#sample">Browse the sample ↓</a><a class="text-link" href="#catalog">Explore all 50 tables ↓</a><a class="text-link" href="/assets/preview/dataset.json" download>Download the sample JSON ↓</a></div></header>
<section class="wrap preview-section" id="sample" aria-label="Dataset sample">
~~~

{{insert dataset-preview.html}}

~~~
<noscript><p class="callout">All sampled works are shown above. Enable JavaScript to search, sort, page through related tables, and inspect linked records. The complete sample is also available in the JSON download.</p></noscript>
</section>
<section class="wrap preview-catalog" id="catalog" aria-labelledby="catalog-title"><div class="section-heading"><div><p class="eyebrow">The larger picture</p><h2 id="catalog-title">50 tables. One connected dataset.</h2></div><a class="text-link" href="/schema/">Understand the join paths →</a></div><p class="catalog-intro">The inventory below comes from the local PostgreSQL catalog. Row totals are planner estimates captured at export, not exact counts or sample sizes. Open a table to inspect its columns.</p>
<label class="catalog-search-label" hidden>Find a table or column<input id="catalog-search" type="search" placeholder="Try works, affiliation, or country_code" autocomplete="off"></label><p id="catalog-count" class="sr-only" role="status" aria-live="polite"></p>
~~~

{{insert dataset-catalog.html}}

~~~
</section>
<section class="wrap preview-notes"><div><p class="eyebrow">Read the sample in context</p><h2>Real records.<br>A deliberately small view.</h2></div><div><p>This is a static export, not a live database connection. Searches and sorting operate only on the downloaded sample. It is useful for understanding the data model, not estimating research trends or database coverage.</p><p>Missing titles, unresolved links, and uneven metadata are preserved. Full OpenAlex IDs remain in the downloads; the browser shortens them for readability. Author and source counts refer to their database records, not the number of rows in this sample.</p><a class="text-link" href="/queries/">Move from records to research questions →</a></div></section>
~~~
