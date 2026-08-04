# Story 01 — Secure Account Access

**Issue:** [#1](https://github.com/unvde/CP3407-Assessment/issues/1)

**Iteration:** 1 · **Estimate:** 2 development-days · **Status:** Done

## Delivered behaviour

- Registration requires email and rejects duplicate email case-insensitively.
- Successful registration signs the reader in.
- Login, logout and post-login redirects are controlled.
- Private book routes require authentication.
- Ordinary readers cannot enter staff moderation routes.

## Implementation and tests

- Implementation: `RegistrationForm`, `RegisterView`, `SafeLoginView`, `LoginRequiredMixin` and `StaffRequiredMixin`.
- Automated evidence: `RegistrationTests` and `AuthenticationTests` in `books/tests.py`.
- Security regression: normal users are not redirected into unauthorised staff pages; staff users may continue to moderation.

## Acceptance

All acceptance criteria are automated and included in the complete Django regression suite. The live application exposes Register, Log in and Log out flows and protects private navigation.
