# Story 07 — Forums and Threaded Replies

**Issue:** [#7](https://github.com/unvde/CP3407-Assessment/issues/7)

**Iteration:** 3 · **Estimate:** 3 development-days · **Status:** Done

## Delivered behaviour

- Each catalogue book has at most one forum.
- Anonymous visitors can read forums; authenticated readers create posts and replies.
- Post and reply authors may edit their own contributions only.
- Forum creators may edit forum details; staff may remove forums and any public contribution.
- Replies retain author and edited-state information beneath their parent post.

## Evidence

- Implementation: `Forum`, `ForumPost`, `ForumReply` and their permission mixins/views.
- Tests: `ForumPermissionTests` and `ForumReplyPermissionTests` in `books/test_community.py`.
- Live proof: catalogue pages link to forums containing posts, reply counts and threaded replies.
