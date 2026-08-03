# Mock Object Research

## Purpose

A mock object replaces a collaborator with a controlled test double. It is most
useful when a test depends on time, a network service, email, file storage or
another slow or non-deterministic boundary. Mocks are not a substitute for
testing Django models, queries and views against the test database.

## Test-Double Vocabulary

- **Stub:** returns a prepared value.
- **Spy:** records how it was called.
- **Mock:** combines controlled behaviour with interaction expectations.
- **Fake:** provides a lightweight working implementation, such as Django's
  in-memory test email backend.

## Reading Compass Decision

Iteration 3 search, notes and review persistence should primarily use Django
database and request tests. Those behaviours depend on real query construction,
relationships, validation and permissions, so replacing them with mocks would
hide important failures.

Time is a suitable boundary to mock. `BookForm` reads
`books.forms.timezone.localdate`; the suite patches that name to a fixed course
day and verifies that a preceding target is rejected. The test also asserts the
collaborator was called, demonstrating both stub and spy behaviour without
depending on the machine clock.

```python
@patch("books.forms.timezone.localdate", return_value=date.max)
def test_target_validation_uses_mocked_course_day(self, mocked_localdate):
    target = (date.max - timedelta(days=1)).isoformat()
    form = BookForm(instance=self.book, data=self.book_data(target))
    self.assertFalse(form.is_valid())
    mocked_localdate.assert_called_once_with()
```

The patch targets the name used by the code under test, not the original
library definition. This avoids leaking a global time change into unrelated
tests.

## Iteration 3 Guidance

- Use real Django requests and database objects for owner isolation.
- Mock an external service only after an integration boundary is introduced.
- Assert outcomes first; assert calls only when the collaboration is itself a
  requirement.
- Keep return values realistic and add at least one non-mocked integration test
  for every external boundary.
