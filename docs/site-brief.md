# Project scope: Clean Air, a standalone website

Build an independent website called "Clean Air".

This brief replaces any earlier plan to fold the project into another site. Clean Air is standalone. Ignore any reference to beattheheat.asia or Common Shade.

Keep all the research, evidence-quality, livelihood, equity, infrastructure and intervention-assessment requirements in `docs/research-brief.md`. The research brief's line about not building a website is overridden by this document.

## Identity and purpose

- Site name: Clean Air
- Suggested descriptor: Air pollution, livelihoods and unequal protection.
- Homepage headline: "Shared air. Unequal protection."

Clean Air should help people understand how air pollution affects communities across India and assess what can be done, by whom, with what evidence and under which conditions.

Delhi/NCR is the anchor case, supported by contrasting Indian settings.

The site should be accessible to a general reader and rigorous enough for a senior philanthropic decision-maker assessing possible grants, partnerships and infrastructure investments.

Keep that decision-making audience implicit. The public-facing site should feel like an independent evidence resource, not a fundraising pitch.

## Repository and brand boundaries

- Inspect the current workspace and repository instructions first.
- If this is a dedicated Clean Air repository, build within it.
- If it contains another website, create an isolated Clean Air project directory without changing the existing application.
- Give Clean Air its own design system, navigation, metadata and assets.
- Do not inherit Common Shade branding, menus, analytics or deployment.
- Do not imply endorsement by Practical Action, any foundation or any organisation mentioned in the research.
- Do not assume a domain has been purchased or selected.
- Build and verify a local or preview version. Report deployment readiness.

## Primary navigation

1. The crisis
2. People and livelihoods
3. Places
4. What works
5. Organisations
6. Evidence

Provide a prominent secondary route: "Where support could make a difference".

This route should compare researched intervention and portfolio options, including evidence gaps, operating responsibilities, recurring costs, equity implications and conditions for success.

## Core user journey

Understand the problem →
Explore a community or place →
Trace health, income and care consequences →
Compare possible interventions →
Inspect evidence and delivery requirements →
Save or download a decision brief.

Example: Street vendors → Delhi/NCR → exposure and earnings constraints → possible protective arrangements → evidence, responsible actors, costs and unanswered questions.

Do not imply that selecting an intervention produces a personalised medical recommendation or a validated investment recommendation.

## Homepage requirements

Explain, in plain language:

- What the crisis is.
- Why its consequences are unequal.
- How health effects connect to work, income and care.
- What visitors can explore.
- How evidence and uncertainty are handled.

Include three main entry points:

- "Understand the impacts"
- "Explore interventions"
- "Examine the evidence"

Build the substantive research pages, working comparisons, organisation directory and downloadable outputs, not only a polished homepage.

## Success criterion

A visitor should leave able to explain both:

- "What is happening to people?"
- "What would a credible, equitable response require?"

## Build rules

- Generate site pages from the files in `/research` (Markdown and CSV), not from hand-written copy. Changing a rating in the evidence map should change the site.
- Every factual claim on the site must trace to a source register entry with a URL and date.
- Show the research cutoff date on the site.

Complete the research, website implementation, source verification, accessibility checks and functional testing specified in `docs/research-brief.md`.
