# Final Demonstration Checklist

## Access and deployment

- [x] Open https://reading-compass.onrender.com/ over HTTPS.
- [x] Confirm `/health/` responds successfully.
- [x] Confirm demo catalogue, lists, profiles, reviews and forums are present.
- [x] Keep staff credentials private and provide instructor access out of band.

## Reader journey

- [x] Register or log in.
- [x] Search Open Library and import a book.
- [x] Change shelf status and add a private note.
- [x] Browse a trait, publish a review and create a public/private list.
- [x] Open a public profile and verify private lists are absent.
- [x] Review recommendations and dismiss one.
- [x] Open a forum, create a post and add a threaded reply.

## Permission demonstration

- [x] Anonymous visitors can read public pages but cannot write.
- [x] One reader cannot change another reader's shelf, list, review, post or reply.
- [x] Ordinary readers cannot open moderation pages.
- [x] Staff can moderate public content and manage shared categories.

## Verification

- [x] Django system check passes.
- [x] No migration drift exists.
- [x] Complete automated regression passes.
- [x] Documentation links every Story to implementation and tests.
