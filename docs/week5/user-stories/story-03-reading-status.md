# Story 03 — Reading Status Management

## User Story

As a reader, I want to assign a status to each book so that I can understand its
position in my reading workflow.

**Estimate:** 2 days  
**Iteration:** 1  
**Status:** done

## Completed Behaviour

Each book accepts exactly one of four controlled statuses:

- Want to Read
- Currently Reading
- Paused
- Completed

The Add and Edit forms provide a status selector and plain-language guidance.
The list and detail pages display readable status labels with distinct visual
treatments. A reader can change a book's status through the edit workflow.

## Acceptance Evidence

Automated tests verify the exact status values, the form guidance and status
updates. The Iteration 1 usability review accepted the status guidance and
shared add/edit workflow.

## Main Implementation

- `Book.ReadingStatus` is the single source of allowed values and labels.
- `BookForm` exposes the model choice field and its help text.
- Templates use `get_status_display` for readable labels.
- CSS status classes provide visual differentiation.
