# Reading Compass Interface Prototype

## Review the prototype

- **Interactive prototype:** [Reading Compass — Interface Prototype in
  Penpot](https://design.penpot.app/#/workspace?team-id=81f57451-85cc-819d-8008-6f857ab31971&file-id=3be9e5e1-190f-8090-8008-6f8638edd4d2&page-id=3be9e5e1-190f-8090-8008-6f8638edd4d3)
- **Offline overview:** [`prototype-overview.png`](prototype-overview.png)
- **Editable/importable sources:** [`prototype-assets/`](prototype-assets/)
- **Penpot import bundle:**
  [`reading-compass-penpot-import.zip`](reading-compass-penpot-import.zip)

The Penpot file contains ten 1440 × 900 boards, eight verified board-to-board
connections and three named flows: **Reader journey**, **Book discovery** and
**Staff moderation**. The PNG and SVG files in this repository ensure the
submission remains reviewable even if the external prototype requires sign-in.

## Purpose and tool choice

The interface prototype validates the complete reader and staff journeys before
implementation changes are made. It was created in **Penpot**, an online
interface-design and prototyping tool. This directly satisfies the rubric's
requirement that interface design use a prototyping tool, while the repository
evidence makes the design reproducible and auditable.

The source screens are stored in [`prototype-assets/`](prototype-assets/). Each
SVG is a 1440 × 900 editable board source. The companion
`prototype-manifest.json` records the screen purpose and required interaction
links so that the prototype can be reproduced and reviewed consistently.

![Prototype screen overview](prototype-overview.png)

## Scope and traceability

| Prototype screen | User stories demonstrated | Design reason |
| --- | --- | --- |
| Account access | Story 01 | Separates authenticated reader activity from public catalogue browsing and communicates the privacy boundary before sign-in. |
| Dashboard | Stories 03 and 08 | Prioritises the active book and explains why each recommendation was selected; every suggestion includes a persistent *Not interested* action. |
| Find a book | Story 02 | Uses one search field for title, author or ISBN and keeps the import action adjacent to normalised Open Library metadata. |
| My books | Story 03 | Keeps shelf content private, makes the four controlled statuses visible and supports text, status and category filters. |
| Private book detail | Story 03 | Groups reading status, progress and private notes while keeping these fields absent from community views. |
| Explore | Story 04 | Combines trait shortcuts, catalogue search, community ratings and local fallback content in one discovery entry point. |
| Community book | Stories 05, 06 and 07 | Brings together shared metadata, aggregate ratings, reviews, list actions and the book-specific forum without exposing private shelf data. |
| Lists and public profile | Story 06 | Shows only intentionally public lists and reviews and explicitly communicates that private data is excluded. |
| Forum | Story 07 | Keeps posts and threaded replies attached to one catalogue book and distinguishes read access from authenticated write access. |
| Moderation centre | Story 09 | Isolates staff-only catalogue refresh, category management and community-content moderation from the reader interface. |

## Primary prototype flow

1. Log in and arrive at the personalised dashboard.
2. Search Open Library and add a result to the private shelf.
3. Open the shelf entry, update progress and add a private note.
4. Explore the community catalogue and open a shared book page.
5. Rate or review the book, add it to a list, or enter its forum.
6. Follow the separate staff flow to the moderation centre.

The verified whole-board click sequence in Penpot is:

`Login → Dashboard → Find a book → My books → Private book → Explore → Community book → Lists/profile → Forum`

The moderation centre is a separate **Staff moderation** flow so staff-only
controls are never presented as part of the ordinary reader journey.

The exact board-to-board connections and trigger labels are recorded in
[`prototype-manifest.json`](prototype-assets/prototype-manifest.json).

## Visual and interaction decisions

- Deep forest navigation and warm paper surfaces give the product an editorial,
  reading-focused identity while maintaining clear contrast.
- Georgia headings distinguish book and discovery content; a system sans-serif
  keeps controls and supporting text legible.
- Green is reserved for primary actions and positive progress, gold for ratings
  and category traits, and red only for destructive moderation actions.
- Desktop boards use a consistent 1440 × 900 frame. Repeated navigation,
  buttons, fields, status chips and book cards form a small reusable component
  system.
- Private and public information are separated structurally, not only by colour.
  Every private screen labels its privacy boundary, and public profiles explicitly
  state what is excluded.
- Each primary action has a text label, status is communicated with words, and
  the layout preserves a visible reading order for keyboard and screen-reader
  implementation.

## Acceptance checks

- Every committed user story with a user-facing interface is represented.
- The primary happy path can be completed without a dead end.
- Public pages never display shelf status, progress or reading notes.
- Reader and staff navigation are visibly different.
- Search, empty/error, permission and destructive-confirmation states are
  retained as implementation requirements even when not all appear as separate
  prototype boards.
- Prototype decisions are traceable to the requirements backlog and can be
  compared with acceptance tests during iteration reviews.

## Rubric alignment

| Rubric expectation | Submission evidence |
| --- | --- |
| Interface design uses a prototyping tool | The linked Penpot file is the canonical interactive prototype. |
| Design covers all major components | Ten boards cover account access, private shelf, discovery, public community features and staff moderation. |
| Design is exemplary and justified | The screen traceability table and visual/interaction decisions explain why each component exists and how privacy, accessibility and task flow shaped it. |
| Design is documented on GitHub | This page, the overview PNG, individual PNG previews, editable SVG boards and JSON interaction manifest are committed together. |
| Prototype is assessable and reproducible | The live file is backed by offline assets and a downloadable Penpot import bundle. |
