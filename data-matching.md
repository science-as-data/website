+++
title = "Data matching: connecting research through OpenAlex"
+++

~~~
<section class="wrap matching-intro" aria-labelledby="project-title">
  <p class="project-identity"><span class="project-icon project-icon-data-matching" aria-hidden="true"><img src="/assets/data-matching-mark.svg" width="36" height="36" alt=""></span><span>Data matching</span></p>
  <h1 id="project-title">Connecting research through OpenAlex</h1>
  <p class="hero-description">A paper’s metadata, full text, source files, and registered study plan often live in separate collections. Data matching brings these otherwise disconnected sources into a common research network, with OpenAlex as the central point of connection.</p>
  <p class="hero-description">CORE contributes additional full text through its dump and API. arXiv connects curated paper sources and version metadata. Pre-registration links connect study plans to the papers that may report them. Each connection adds evidence to the same research context.</p>
</section>

<section class="wrap matching-network-section" aria-labelledby="network">
  <h2 id="network">The network of sources</h2>
  <figure class="source-network-figure" aria-describedby="source-network-caption">
    <div class="source-network" role="group" aria-label="Source network centred on OpenAlex; select a source to read about its connection">
      <a class="source-network-node source-network-hub" href="#openalex-hub">
        <span class="source-network-kicker">Central point of connection</span>
        <span class="source-network-name">OpenAlex</span>
        <span>Shared work identifiers</span>
        <span>Works · authors · institutions<br>Topics · citation relationships</span>
        <span class="source-network-action">Connect the evidence ↗</span>
      </a>
      <a class="source-network-node source-network-core" href="#core-link">
        <span class="source-network-name"><img src="/assets/core-mark.svg" width="30" height="30" alt="">CORE</span>
        <span class="source-network-detail"><strong>CORE dump</strong><span>Stored full text and metadata</span></span>
        <span class="source-network-detail"><strong>CORE API</strong><span>Targeted retrieval and enrichment</span></span>
        <span class="source-network-action">Read the full-text connection ↗</span>
      </a>
      <div class="source-network-edge source-network-edge-core" aria-hidden="true"><span>Full text</span></div>
      <div class="source-network-edge source-network-edge-arxiv" aria-hidden="true"><span>Text +<br>metadata</span></div>
      <a class="source-network-node source-network-arxiv" href="#arxiv-link">
        <span class="source-network-name"><img src="/assets/arxiv-mark.jpg" width="30" height="30" alt="">arXiv</span>
        <span class="source-network-detail"><strong>Curated bulk sources</strong><span>TeX · BibTeX · bibliographies</span></span>
        <span class="source-network-detail"><strong>Kaggle metadata</strong><span>Paper IDs · authors · versions</span></span>
        <span class="source-network-action">Read the arXiv connection ↗</span>
      </a>
      <div class="source-network-edge source-network-edge-plans" aria-hidden="true"><span>Study plans ↔ papers</span></div>
      <a class="source-network-node source-network-plans" href="#preregistration-link">
        <span class="source-network-name"><img src="/assets/preregistrations-mark.svg" width="30" height="30" alt="">Pre-registrations</span>
        <span class="source-network-platforms"><span>AEA RCT Registry</span><span>OSF Registries</span><span>AsPredicted</span></span>
        <span>Hypotheses · study designs · planned analyses · registration dates</span>
        <span class="source-network-action">Read the study-plan connection ↗</span>
      </a>
    </div>
    <figcaption id="source-network-caption">Select a source to follow its connection. The lines show the integration model around OpenAlex; source identifiers, versions, and linkage evidence remain attached to each record. Implementation notes are provided below.</figcaption>
  </figure>
</section>

<nav class="project-sections wrap" aria-label="Data matching sections"><strong>Follow the connections</strong><a href="#openalex-hub">OpenAlex as the hub</a><a href="#core-link">CORE full text</a><a href="#arxiv-link">arXiv sources and metadata</a><a href="#preregistration-link">Registered study plans</a><a href="#methods">Linkage evidence</a><a href="#ownership">Tools and development</a></nav>
<div class="wrap project-details"><article class="article">

<section aria-labelledby="openalex-hub">
  <h2 id="openalex-hub">OpenAlex provides a common reference</h2>
  <p>The central node gives the network a shared way to refer to scholarly works and their relationships. Connecting source records to an OpenAlex work makes it possible to move between a paper’s bibliographic context, available text, arXiv history, and associated study plans.</p>
  <p>The connections preserve the identity of each source. A CORE record keeps its CORE identifier; an arXiv observation keeps its paper ID and version evidence; a registration keeps its platform identifier. OpenAlex work IDs provide a common reference for joining these records in the research dataset.</p>
  <p><a href="/openalex/">Explore the OpenAlex database</a> · <a href="/schema/">OpenAlex entities and relationships</a></p>
</section>

<section aria-labelledby="core-link">
  <span id="routes"></span>
  <h2 id="core-link">CORE brings more full text into reach</h2>
  <p>The CORE branch extends the text available for works represented in OpenAlex. The <strong>CORE dump</strong> provides a substantial local collection of metadata and extracted full text. The <strong>CORE API</strong> complements that snapshot with targeted lookups and retrieval of additional text where available.</p>
  <p>Matching a CORE record to an OpenAlex work connects its stored text to the work’s authors, topics, and citation context. DOI and other identifiers support this connection; titles, authors, and publication details provide additional evidence when identifiers are missing or inconsistent. Dump records and API responses retain their own provenance and retrieval dates.</p>
  <p>This makes the CORE branch useful for reading and analysing papers beyond the bibliographic record: locating a registration identifier in a methods section, examining how a study is described, or recovering evidence needed to resolve a reference.</p>
  <p><a href="/core/">CORE dump, API assessment, and stored full text</a></p>
</section>

<section aria-labelledby="arxiv-link">
  <h2 id="arxiv-link">arXiv connects paper sources with their histories</h2>
  <p>The arXiv branch combines curated bulk full text with the metadata distributed through Kaggle. Within the arXiv PostgreSQL database, source observations, TeX and BibTeX files, and rendered bibliography material are connected to paper metadata by arXiv ID.</p>
  <p>Linking that arXiv identity to an OpenAlex work extends the connection into the wider literature. DOI and arXiv identifiers, repository locations, and bibliographic evidence help establish which records refer to the same work. Preprint and journal manifestations retain their version and source information.</p>
  <p>The resulting connection lets a researcher move from an OpenAlex work to the arXiv text and bibliography behind it, or from an arXiv paper to its broader bibliographic context. Submission histories and source-version evidence remain available for studies of how papers and citations develop over time.</p>
  <p><a href="/arxiv/">arXiv curation and the connected database structure</a></p>
</section>

<section aria-labelledby="preregistration-link">
  <h2 id="preregistration-link">Pre-registrations connect plans to papers</h2>
  <p>AEA RCT Registry, OSF Registries, and AsPredicted contribute an earlier stage of the research process: recorded hypotheses, study designs, and planned analyses. Connecting these records to papers represented in OpenAlex brings study plans into the same network as publication metadata and full text.</p>
  <p>Registration identifiers and URLs mentioned in papers provide direct linkage evidence. Titles, investigator names, and study descriptions help identify further candidate papers. Text supplied through CORE or arXiv can provide the context needed to interpret a reference to a registration.</p>
  <p>A registration–paper link represents a relationship between a plan and a publication. One plan may lead to several papers, and one paper may draw on several registrations. Preserving those relationships supports comparisons between what researchers planned and what they subsequently reported.</p>
  <p><a href="/pre-registrations/">The registration collections and their fields</a></p>
</section>

<section aria-labelledby="methods">
  <h2 id="methods">Keep the evidence behind each connection</h2>
  <p>Matching starts with identifiers and source-specific metadata, then brings in bibliographic and textual evidence where needed. Each proposed connection retains the source records, the identifiers compared, the method used, and the evidence supporting the relationship. Ambiguous candidates and unresolved records remain distinguishable.</p>
  <p>Paper identity, version relationships, and links from registrations to publications are recorded as different relationships. A citation to a registration needs enough context to establish how that plan relates to the paper. A missing match may reflect missing identifiers, unavailable text, or incomplete retrieval.</p>
  <p id="achieved">These connections support a research path across the network: begin with a study plan, find a related OpenAlex work, retrieve text through CORE or arXiv, and inspect the reported study alongside its original plan. The value comes from bringing those complementary records into conversation while preserving their origins.</p>
</section>

<section aria-labelledby="ownership">
  <h2 id="ownership">Tools and development</h2>
  <p>Source projects curate their own data; <a href="https://github.com/science-as-data/data-matching">data-matching</a> develops the connections between them. The pre-registration workflow includes input adapters, publication searches, candidate linkage, and persistence. The CORE dump and API tools and the arXiv source database provide complementary assets for extending the network.</p>
  <p>The diagram describes the integration model. General CORE–OpenAlex and arXiv–OpenAlex crosswalks remain integration work to develop and document. The existing OpenAlex date audit provides bounded arXiv linkage examples. Implementation details and historical experiments remain available in the repositories.</p>
  <p><a href="https://github.com/science-as-data/data-matching/tree/main/preregistrations/matching">Pre-registration linkage tools</a> · <a href="https://github.com/science-as-data/data-matching/tree/main/preregistrations/EDA">Analyses of connected records</a> · <a href="https://github.com/science-as-data/openalex/tree/main/matching">Journal crosswalk work</a></p>
</section>
</article></div>
~~~
