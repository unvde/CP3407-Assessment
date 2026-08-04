# Requirements Backlog

The backlog contains nine committed User Stories. Priorities use the course scale: 50 is essential, followed by 40, 30, 20 and 10. Estimates are development-days and each iteration is limited to seven days.

| No. | User Story | Priority | Estimate | Iteration | Status |
| ---: | --- | ---: | ---: | ---: | --- |
| 01 | As a reader, I want secure account access so that private reading data is protected. | 50 | 2 | 1 | Done |
| 02 | As a reader, I want to search Open Library and import a shared catalogue record so that I avoid repeated data entry. | 50 | 3 | 1 | Done |
| 03 | As a reader, I want a private shelf with controlled statuses and notes so that I can manage reading privately. | 50 | 2 | 1 | Done |
| 04 | As a reader, I want category and trait discovery so that I can find books by interest. | 40 | 3 | 2 | Done |
| 05 | As a community member, I want to rate and review books publicly so that I can share useful opinions. | 40 | 2 | 2 | Done |
| 06 | As a reader, I want public or private lists and a public profile so that sharing remains intentional. | 40 | 2 | 2 | Done |
| 07 | As a community member, I want forums with posts and threaded replies so that discussion stays attached to a book. | 30 | 3 | 3 | Done |
| 08 | As a reader, I want personalised recommendations with a Not interested action so that discovery improves. | 30 | 2 | 3 | Done |
| 09 | As a staff member, I want moderation and dependable production delivery so that public content and deployment remain safe. | 30 | 2 | 3 | Done |

## Acceptance summary

### Story 01 — Secure Account Access

- Email is required and duplicate email is rejected.
- Valid users can log in and log out.
- Private routes require authentication.
- Staff-only routes reject ordinary users.

### Story 02 — Shared Catalogue Search and Import

- Title, author and ISBN searches return normalised Open Library results.
- Signed import tokens reject tampering.
- Duplicate imports reuse catalogue and shelf records.
- API failure produces a controlled fallback.

### Story 03 — Personal Shelf and Reading Statuses

- Shelf records are private and owner-scoped.
- Status is limited to Want to Read, Currently Reading, Paused or Completed.
- Owners can update status and maintain private notes.
- Private data is absent from public pages.

### Story 04 — Category and Trait Discovery

- API subjects and user categories are normalised and reused.
- Trait discovery supports pagination.
- Aliases resolve consistently.
- API timeout falls back to local catalogue content.

### Story 05 — Public Ratings and Reviews

- Rating is limited to 1–5 and review content is not blank.
- A reader has at most one review per catalogue book.
- Reviews and aggregate ratings are public.
- Author and staff permissions are enforced.

### Story 06 — Custom Lists and Public Profiles

- Owners can create lists and add or remove books.
- Only owners may edit or delete a list.
- Private lists are absent from community search and profiles.
- Public profiles show only intentionally public material.

### Story 07 — Forums and Threaded Replies

- A catalogue book has at most one forum.
- Anonymous visitors can read but cannot write.
- Authors can edit their own posts and replies only.
- Staff can remove forums, posts and replies.

### Story 08 — Personalised Recommendations

- Category matches are ranked and owned books are excluded.
- External results may fill a sparse local result.
- Not interested persists and removes the suggestion.
- External timeout leaves a usable local result or empty state.

### Story 09 — Moderation and Production Delivery

- Moderation routes require staff permission.
- Staff can manage categories, refresh metadata and moderate public content.
- Render configuration covers database, static files, HTTPS and health checks.
- System, migration and deployment checks pass.

## Planning result

Each iteration totals seven development-days. The order establishes privacy and catalogue foundations first, adds public discovery second, and introduces higher-risk community moderation and production delivery last.
