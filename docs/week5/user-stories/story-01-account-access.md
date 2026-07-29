# Story 01 — User Account Access

## User Story

As a new reader, I want to create and access a personal account so that my
reading information can be securely saved.

**Estimate:** 2 days  
**Iteration:** 1  
**Status:** done

## Completed Behaviour

- A reader can register with username, email and password.
- Email addresses are required and duplicates are rejected
  case-insensitively.
- A successful registration signs the reader in and opens their book list.
- Existing readers can log in and log out.
- Private book routes redirect unauthenticated visitors to login.

## Acceptance Evidence

Automated tests cover successful registration, duplicate-email rejection,
valid and invalid login, logout and authentication protection. The shared base
template changes its navigation according to authentication state.

## Main Implementation

- `RegistrationForm` validates registration data.
- `RegisterView` creates and signs in the user.
- Django authentication views provide login and logout.
- `LoginRequiredMixin` protects private book workflows.
