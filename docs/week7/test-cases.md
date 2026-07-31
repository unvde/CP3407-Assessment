# Week 7 Test Cases

## Summary

Practical 7 requires at least five user stories, three cases per story and 15
automated tests. This focused suite documents **7 user stories and 30
automated tests**. Each case protects a distinct user-visible rule, risk or
boundary; tests that repeated the same behaviour at another layer were removed.

## US7-01 — Access an Account

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| ACC-01 | Register with valid details | Account is created, signed in and redirected | `RegistrationTests.test_registration_creates_and_logs_in_user` |
| ACC-02 | Reuse an email with different case | Registration is rejected | `RegistrationTests.test_registration_rejects_duplicate_email` |
| ACC-03 | Register without email | Required-field error; no account | `RegistrationTests.test_registration_requires_email` |
| ACC-04 | Submit different passwords | Mismatch error; no account | `RegistrationTests.test_registration_rejects_mismatched_passwords` |
| ACC-05 | Log in with valid credentials | Personal list opens | `AuthenticationTests.test_valid_login` |
| ACC-06 | Log in with invalid credentials | Error is shown and access is denied | `AuthenticationTests.test_invalid_login` |
| ACC-07 | Submit logout | Session ends and login page opens | `AuthenticationTests.test_logout` |

## US7-02 — View a Private Reading List

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| LIST-01 | Anonymous visitor opens private book routes | Every route redirects to login | `AuthenticationTests.test_private_book_routes_require_login` |
| LIST-02 | Two readers own books | List shows only the signed-in reader's book | `BookManagementTests.test_list_contains_only_current_users_books` |
| LIST-03 | Reader opens another reader's detail | Response is 404; private data is hidden | `BookManagementTests.test_cannot_view_another_users_book` |

## US7-03 — Add Valid Book Information

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| ADD-01 | Validate page count `0` | Model rejects the non-positive total | `BookModelTests.test_total_pages_must_be_positive` |
| ADD-02 | Create a book without explicit status | Status defaults to Want to Read | `BookModelTests.test_default_status_is_want_to_read` |
| ADD-03 | Enter surrounding whitespace | Title and author are trimmed | `BookFormTests.test_form_trims_title_and_author` |
| ADD-04 | Submit an unknown status | Form rejects the invalid choice | `BookFormTests.test_form_rejects_unknown_status` |
| ADD-05 | Submit a valid book | Book is assigned to the signed-in reader | `BookManagementTests.test_create_book_assigns_authenticated_owner` |

## US7-04 — Maintain My Books

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| EDIT-01 | Change own book's reading status | Change persists and detail page opens | `BookManagementTests.test_update_book` |
| EDIT-02 | Delete own book | Book is removed and list opens | `BookManagementTests.test_delete_book` |
| EDIT-03 | Attempt to edit another reader's book | Response is 404 and their book is unchanged | `BookManagementTests.test_cannot_edit_another_users_book` |
| EDIT-04 | Delete the account owning a book | Related book is removed by cascade | `BookModelTests.test_deleting_owner_cascades_to_books` |

## US7-05 — Update Reading Progress

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| PROG-01 | Read page 100 of a 400-page book | Progress is calculated as 25% | `ReadingProgressTests.test_progress_percentage_is_calculated` |
| PROG-02 | Record progress without total pages | Percentage is unavailable rather than invented | `ReadingProgressTests.test_percentage_is_unavailable_without_total_pages` |
| PROG-03 | Set current page above known total | Model rejects the out-of-range value | `ReadingProgressTests.test_current_page_cannot_exceed_total_pages` |
| PROG-04 | Submit a valid current-page update | New page persists and detail page opens | `ReadingProgressTests.test_update_saves_valid_current_page` |

## US7-06 — View My Reading Dashboard

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| DASH-01 | Anonymous visitor opens dashboard | Redirect to login with dashboard as destination | `ReadingDashboardTests.test_dashboard_requires_login` |
| DASH-02 | Reader has active and inactive books | Only Currently Reading books appear | `ReadingDashboardTests.test_dashboard_contains_only_currently_reading_books` |
| DASH-03 | Another reader has an active book | Their book is not exposed | `ReadingDashboardTests.test_dashboard_does_not_reveal_other_users_books` |

## US7-07 — Manage a Reading Target

| ID | Scenario | Expected result | Automated test |
|---|---|---|---|
| PLAN-01 | Add a future target | Target persists | `ReadingPlanTests.test_reader_can_add_future_target` |
| PLAN-02 | Add a new past target | Form rejects it and saves no target | `ReadingPlanTests.test_new_past_target_is_rejected` |
| PLAN-03 | Clear an existing target | Optional target is removed | `ReadingPlanTests.test_reader_can_remove_target` |
| PLAN-04 | Attempt to change another reader's target | Response is 404 and their data is unchanged | `ReadingPlanTests.test_reader_cannot_change_another_users_target` |

## Coverage Check

| User story | Cases |
|---|---:|
| US7-01 Account access | 7 |
| US7-02 Private list | 3 |
| US7-03 Add book information | 5 |
| US7-04 Maintain books | 4 |
| US7-05 Reading progress | 4 |
| US7-06 Dashboard | 3 |
| US7-07 Reading target | 4 |
| **Total** | **30** |

Every selected story has at least three distinct automated cases. All named
methods are implemented in `books/tests.py`.
