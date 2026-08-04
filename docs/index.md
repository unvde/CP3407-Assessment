# Reading Compass — Project Evidence

Reading Compass is a deployed community book-discovery application. This site
is the canonical entry point for the current requirements, design,
implementation, testing and delivery evidence.

## Delivered outcome

- Live application: https://reading-compass.onrender.com/
- Source repository: https://github.com/unvde/CP3407-Assessment
- Three completed iterations covering the private shelf, shared catalogue,
  discovery, reviews, lists, recommendations, forums and moderation
- Automated model, service, view, permission, acceptance and system tests
- Render deployment with PostgreSQL, static-file handling and health checks

## Start with the current system

- [Feature traceability](traceability.md) links each delivered capability to
  implementation, automated tests and completion evidence.
- [Testing evidence](testing.md) explains the test code, data, test levels,
  acceptance coverage, CI checks and current result.
- [Architecture](design/architecture.md), [database design](design/database-design.md)
  and [interface design](design/interface-design.md) describe the current
  implementation.
- [Development tools](development-tools.md) explains the libraries, build
  tools, delivery platform and external services used by the project.

## Iteration summary

| Iteration | Product increment | Acceptance evidence |
| --- | --- | --- |
| Foundation | Secure account, shared catalogue import and private shelf | `week5/user-stories/` |
| Community | Category discovery, public reviews, lists and profiles | `week7/user-stories/` |
| Delivery | Forums, recommendations, moderation and production delivery | `week9/` |

## Repository organisation

The topic pages above are the current source of truth. Directories named by
week retain the practical work, planning snapshots, burndowns and iteration
reviews required to demonstrate the development process. They remain available
as chronological supporting evidence, but are intentionally placed after the
current-system pages in navigation.

The repository's Issues and Pull requests tabs retain GitHub's immutable audit
history. Feature names, code, tests and completion pages are used for current
traceability instead of GitHub record numbers.
