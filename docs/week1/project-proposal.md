# Reading Compass Project Proposal

## Problem

Readers often split book discovery, private tracking, reviews and discussion across unrelated services. Re-entered metadata becomes inconsistent, while privacy boundaries are easily blurred when personal notes and public opinions share a platform.

## Proposed solution

Reading Compass is a web application built around a shared book catalogue and an explicitly private personal shelf. It combines Open Library search/import, reading statuses and notes, category discovery, reviews, lists, profiles, recommendations and moderated book forums.

## Objectives

- Minimise manual book data entry through a reusable catalogue.
- Keep shelf state and notes private by default.
- Make public sharing intentional through reviews, public lists and profiles.
- Support community discovery through categories, traits, recommendations and forums.
- Enforce author, owner and staff permission boundaries.
- Deliver a tested Django application on Render.

## Technology

Django provides models, validation, authentication, templates and testing. Open Library supplies public catalogue metadata. SQLite supports local work; PostgreSQL, Gunicorn and WhiteNoise support the Render deployment. GitHub stores source, Issues, reviews and iteration evidence.

## Team

- Tianyang Zhang — lead developer and technical lead.
- Yuhao Guo — project coordination, requirements, documentation and QA.

## Success criteria

The project succeeds when all nine Stories pass focused and system tests, the deployed application supports the complete reader and moderator journeys, and each requirement is traceable to code, tests and acceptance evidence.
