# Story 07 — Search and Filtering

## Week 8 Day 5

Story 07 started on the independent `iteration-3` branch with test-driven
development. The acceptance suite was written before the implementation and
its first valid project-environment run produced 8 expected failures because
the list view did not yet process search or filter parameters and displayed no
controls.

## Acceptance Coverage

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| SEARCH-01 | Search by mixed-case title text | Matching personal title is returned without case sensitivity | `test_search_matches_title_case_insensitively` |
| SEARCH-02 | Search by mixed-case author text | All matching personal books are returned without case sensitivity | `test_search_matches_author_case_insensitively` |
| FILTER-01 | Select each defined reading status | Only personal books in the selected status are returned | `test_every_defined_status_can_filter_results` |
| FILTER-02 | Submit search and status together | Both constraints are applied to the same owner-scoped queryset | `test_search_and_status_filters_can_be_combined` |
| FILTER-03 | Another owner has a matching book | The other owner's book is never returned | `test_filtered_results_remain_owner_scoped` |
| FILTER-04 | Clear query and status | The full personal reading list is restored | `test_clearing_filters_restores_full_personal_list` |
| FILTER-05 | Submit an unknown status | The request remains safe and the invalid status is ignored | `test_unknown_status_is_ignored_safely` |
| UI-01 | Open the filtered list | Search, status, apply and clear controls are available and retain valid values | `test_page_displays_search_status_and_clear_controls` |

## Implementation Evidence

- Owner isolation remains the first query boundary through
  `OwnedBookQuerysetMixin`.
- Title and author search use a case-insensitive OR query.
- Status filtering accepts only values defined by `Book.ReadingStatus`.
- Search and status constraints compose on the same queryset.
- Invalid status values do not produce an error or bypass owner scope.
- The list page provides labelled search and status controls, applies both
  parameters together, preserves valid selections and offers a clear action.
- Filtered empty results are distinguished from a genuinely empty reading
  list.

## Verification

The targeted Story 07 suite passes all 8 acceptance tests. The completion gate
also passes:

- complete Django regression suite: 38 tests passed;
- Django system check: no issues; and
- migration drift check: no changes detected.

These results satisfy the Story 07 acceptance criteria and support moving its
implementation, interface, test and acceptance-review tasks to `done`.
