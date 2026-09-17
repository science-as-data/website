+++
title = "Pre-registrations: collection and data"
+++

~~~
<section class="hero wrap project-hero" aria-labelledby="project-title">
  <div class="hero-copy">
    <p class="project-identity"><span class="project-icon project-icon-pre-registrations" aria-hidden="true"><img src="/assets/preregistrations-mark.svg" width="36" height="36" alt=""></span><span>Pre-registrations</span></p>
    <h1 id="project-title">Registered study plans for research</h1>
    <p class="hero-description">Three collections bring together registered study plans from the AEA RCT Registry, OSF Registries, and AsPredicted.</p>
    <p class="hero-description">Each collector extracts platform-specific fields and preserves identifiers, dates, and retrieval provenance. Outputs include JSON or JSONL, with CSV and PostgreSQL available for selected workflows.</p>
    <p class="hero-description">The records support analysis of study plans and provide inputs for publication linkage. Field definitions and coverage remain specific to each platform.</p>
    <div class="hero-actions"><a class="button" href="#figures">Key collection figures <span aria-hidden="true">↗</span></a><a class="text-link" href="#platforms">Platforms and fields <span aria-hidden="true">↗</span></a></div>
  </div>
  <figure class="transformation process-figure" aria-labelledby="process-title">
    <figcaption class="figure-topline" id="process-title">FROM SOURCE RECORDS TO RESEARCH DATA</figcaption>
    <div class="process-input"><h2>Input: Registry records</h2><p>APIs · web pages · PDFs · snapshots</p><p>Study details · registry IDs · dates</p></div>
    <div class="transform-connector"><span class="connector-line" aria-hidden="true"></span><span>RETRIEVE → EXTRACT → PRESERVE</span><span class="process-arrow" aria-hidden="true">↓</span></div>
    <div class="process-outputs" aria-label="Outputs"><div class="process-output"><h3>Study fields</h3><p>Plans and registry metadata</p></div><div class="process-output"><h3>Identifiers</h3><p>Platform-specific record IDs</p></div><div class="process-output"><h3>Dates</h3><p>Distinct event timestamps</p></div><div class="process-output"><h3>Provenance</h3><p>Source and retrieval evidence</p></div></div>
    <p class="figure-note">Outputs: JSON/JSONL; CSV and PostgreSQL for selected workflows. No shared normalized database spans all collectors.</p>
  </figure>
</section>
~~~

{{insert preregistrations-summary.html}}

~~~
<section class="section wrap project-workflow" aria-labelledby="workflow-title"><div class="section-heading"><h2 id="workflow-title">Data processing workflow</h2></div><div class="workflow-grid"><a class="workflow-step" href="#platforms"><span class="step-index">01 <span aria-hidden="true">↗</span></span><h3>Define scope</h3><p>Select supported platforms, queries, and provider filters.</p></a>
<a class="workflow-step" href="#platforms"><span class="step-index">02 <span aria-hidden="true">↗</span></span><h3>Retrieve</h3><p>Use each collector’s supported API, page, PDF, or snapshot input.</p></a>
<a class="workflow-step" href="#representation"><span class="step-index">03 <span aria-hidden="true">↗</span></span><h3>Extract and store</h3><p>Retain platform field meanings, identifiers, and retrieval provenance.</p></a>
<a class="workflow-step" href="#limits"><span class="step-index">04 <span aria-hidden="true">↗</span></span><h3>Assess eligibility</h3><p>Check record type, registration timing, and access restrictions.</p></a></div></section>
<nav class="project-sections wrap" aria-label="Pre-registration project sections"><strong>In this section</strong><a href="#figures">Key figures</a><a href="#completed">Completed work</a><a href="#platforms">Platforms and fields</a><a href="#representation">Data representation</a><a href="#limits">Coverage and interpretation</a><a href="/data-matching/">Linking to papers</a><a href="https://github.com/science-as-data/study-preregistrations">Repository ↗</a></nav>
<div class="wrap project-details"><article class="article">
~~~

{{insert preregistrations-statistics.html}}

~~~

<section aria-labelledby="completed"><h2 id="completed">Completed work</h2><p>The three collections have dedicated command-line tools, parsers, file exports, PostgreSQL storage, and offline fixture tests. AEA RCT uses Dataverse snapshot input; OSF uses public registration records; AsPredicted supports live and archived pages, with a separate path for newer PDF records.</p><p>The databases retain platform-specific fields and identities: <code>aea_rct.trials</code>, <code>osf.registrations</code>, and <code>aspredicted.aspredicted_registrations</code> name each database and its collection table. AsPredicted distinguishes retrieval sources and archive timestamps. File outputs are JSON or JSONL, with CSV available in some workflows.</p><p>Historical matching experiments used 11,746 AEA source records and 25,436 AsPredicted observations. Those input counts differ from the distinct registration counts above. Publication-linkage results and dependent analyses are documented in <a href="/data-matching/">Data matching</a>.</p></section>
<section aria-labelledby="platforms"><h2 id="platforms">Platforms and key fields</h2><div class="data-table-scroll"><table><thead><tr><th scope="col">Collector</th><th scope="col">Key data features</th><th scope="col">Method</th></tr></thead><tbody>
<tr><th scope="row"><a class="registry-table-label" href="https://github.com/science-as-data/study-preregistrations/tree/main/aspredicted"><img src="/assets/aspredicted-mark.svg" width="32" height="32" alt=""><span>AsPredicted</span></a></th><td>ID, title, authors, hypotheses, dependent variables, conditions, planned analyses, outlier handling, sample-size plan, creation date, and retrieval provenance.</td><td>Live HTML/PDF and Wayback retrieval; optional PostgreSQL.</td></tr>
<tr><th scope="row"><a class="registry-table-label" href="https://github.com/science-as-data/study-preregistrations/tree/main/osf"><img src="/assets/osf-mark.ico" width="32" height="32" alt=""><span>OSF Registries</span></a></th><td>GUID, title, description, registration template, provider, tags, registration and modification dates, embargo and withdrawal flags.</td><td>Public JSON:API feed with downstream provider filtering, optional raw payload, and PostgreSQL.</td></tr>
<tr><th scope="row"><a class="registry-table-label" href="https://github.com/science-as-data/study-preregistrations/tree/main/aea-rct"><img class="registry-seal" src="/assets/aea-mark.png" width="32" height="32" alt=""><span>AEA RCT Registry</span></a></th><td>Trial ID, title, abstract, investigators, status, registration/update dates, intervention dates, countries, keywords, and JEL codes.</td><td>Dataverse JSON snapshots; tolerant parsing of historical field names and optional PostgreSQL.</td></tr>
</tbody></table></div></section>
<section aria-labelledby="representation"><h2 id="representation">Identifiers, dates, and provenance</h2><p>Each platform keeps its own identifiers and field meanings. A registration date, a study start date, an archive capture date, and a last-update timestamp describe different events. Missing fields and restricted records must remain distinguishable from observed empty content.</p><p>AsPredicted records retain retrieval source and archive timestamps where relevant. Other collectors can preserve raw API values for fields beyond their standard output. AEA’s parser accepts both older and newer field spellings. Consult each collector’s README for output and raw-payload options.</p></section>
<section aria-labelledby="limits"><h2 id="limits">Coverage and interpretation</h2><p>The current website scope is AEA RCT, OSF, and AsPredicted. Counts describe the locally collected records and retain their retrieval dates. They do not establish complete or current registry coverage, and IDs are not deduplicated across platforms.</p><p>OSF’s collection spans several providers, including EGAP; filter by provider for a narrower sampling frame. Embargo and withdrawal flags affect interpretation and access. For every platform, compare registration timing with study and data-collection dates before treating a plan as prospective. A failed or unavailable fetch is not evidence that a registration does not exist.</p><p><a href="https://github.com/science-as-data/study-preregistrations">Collection documentation and platform scope</a> · <a href="/data-matching/">Connecting study plans and papers</a></p></section>
</article></div>
~~~
