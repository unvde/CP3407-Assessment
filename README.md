# CP3407

## Reading Compass

Reading Compass is a web-based reading planning and reflection platform. It helps readers organise books they intend to read, set achievable reading plans, record progress, and reflect on completed books.

The project will be developed iteratively as part of the CP3407 Advanced Software Engineering assessment.

## Project Objectives

- Help users organise books they want to read.
- Allow users to create manageable reading plans.
- Provide a simple way to record reading progress.
- Encourage reflection through reading notes and completion reviews.
- Apply agile software engineering practices throughout development.
- Deliver a usable and tested web application over multiple iterations.

## Target Users

Reading Compass is intended for students and casual readers who want a straightforward way to organise their reading and maintain consistent reading habits.

## Proposed Features

- User registration and authentication
- Personal reading list
- Reading status management
- Reading plan creation
- Progress updates
- Reading notes
- Completion reviews
- Personal reading dashboard
- Search and filtering

These ideas have been reviewed through target-user interviews and converted into a formal requirements backlog.

## Technology Stack

The initial proposed technology stack is:

- Backend: Python and Django
- Frontend: HTML, CSS and JavaScript
- Database: SQLite during development
- Version Control: Git and GitHub
- Testing: Django testing framework

The technology stack may be adjusted as the project requirements become clearer.

## Team

### Tianyang Zhang

**Roles:** Lead Developer and Technical Lead

Responsibilities:

- Lead application development
- Make technical and architectural decisions
- Implement core application features
- Maintain code quality
- Support testing and deployment

### Yuhao Guo

**Roles:** Project Coordinator and Requirements, Documentation and QA Lead

Responsibilities:

- Coordinate project activities and iteration documentation
- Assist with requirements collection and user-story preparation
- Maintain project documentation
- Prepare acceptance criteria and test cases
- Conduct quality-assurance and usability checks
- Track progress against iteration goals

## Project Documentation

### Week 1 - Project Initiation

- [Project Proposal](docs/week1/project-proposal.md)
- [Initial Backlog Ideas](docs/week1/initial-backlog.md)

### Week 2 - Requirements Analysis

- [Target-User Interview Findings](docs/week2/interview-findings.md)
- [Requirements Backlog](docs/week2/requirements-backlog.md)
- [Practical 2 Report](docs/week2/practical-report.md)

### Week 3 - Iteration 1

- [Iteration Plan](docs/week3/iteration-plan.md)
- [Iteration 1 Project Board](docs/week3/project-board.md)
- [Iteration 1 Burndown](docs/week3/burndown.md)

### Week 4 - Execution and Tracking

- [Task Breakdown](docs/week4/task-breakdown.md)
- [Task Tracking](docs/week4/task-tracking.md)
- [Class Diagram](docs/week4/class-diagram.md)
- [Sequence Diagram](docs/week4/sequence-diagram.md)
- [Practical 4 Report](docs/week4/practical-report.md)

### Week 5 - Iteration 1 Review

- [Published GitHub Pages Site](https://unvde.github.io/CP3407-Assessment/)
- [Iteration 1 Review and Actual Velocity](docs/week5/iteration-review.md)
- [SRP and DRY Review](docs/week5/srp-dry-review.md)
- [Task and Story Tracking](docs/week5/task-tracking.md)
- [Practical 5 Report](docs/week5/practical-report.md)
- [Completed User Story Documentation](docs/week5/user-stories/README.md)

### Week 6 - Iteration 2 Planning

- [Iteration 2 GitHub Project](https://github.com/users/unvde/projects/3)
- [Practical 6 Report](docs/week6/practical-report.md)
- [Iteration 1 Burndown Graph](docs/week6/iteration-1-burndown.svg)

### Week 7 - Test-Driven Development

- [Test Plan](docs/week7/test-plan.md)
- [Test Cases](docs/week7/test-cases.md)
- [Practical 7 Report](docs/week7/practical-report.md)

Additional weekly documentation covering design, iterations, testing and development tools will be added as the project progresses.

## Project Status

**Current stage:** Iteration 1 is complete. Iteration 2 Stories 04–06 have been
implemented against the adjusted 7-day capacity, pass acceptance testing, and
are ready for pull-request review.

## Local Development

### Requirements

- Python 3.12 or later
- pip

### Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Configure local environment variables:

   ```bash
   export DJANGO_SECRET_KEY="replace-with-a-long-random-value"
   export DJANGO_DEBUG=True
   export DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
   ```

4. Prepare the database:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open `http://127.0.0.1:8000/`.

### Tests

Run the automated test suite with:

```bash
python manage.py test
```
