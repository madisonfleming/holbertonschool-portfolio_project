
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Testing Guide ---------------------------- 🗺️ `/my_little_bookworm/tests`

- Jump back to [Application Setup Guide](my_little_bookworm/README.md) ------------- ⬅️ `/my_little_bookworm` 
---

# Testing Guide

Our backend unit and API tests are written with Python's `unittest` framework. Tests are grouped by the app module they exercise.

> ℹ️ `unittest` is native to Python - no need to install it.


## Table of Contents

- [What makes a good test?](/my_little_bookworm/tests/README.md#what-makes-a-good-test)
- [Run all tests locally](/my_little_bookworm/tests/README.md#run-all-tests-locally)

## What makes a good test?

A good test should:
- be independent of other tests (so one test failure doesn't break other tests)
- have clear boundaries (aka clear start & stop points)
- use mocks & stubs to isolate the test within the chosen boundaries
- have specific, well-chosen assertions, which provide meaningful information about the application
- be tested to ensure that it fails when it's supposed to (ie make a breaking change in your app code & re-run your test - does it fail when you're expecting it to?)


## Run all tests locally

```bash
# Ensure that you're in the correct directory
cd my_little_bookworm

# Ensure that you're in a virtual env
source venv/bin/activate

# Run all of the tests in the part 4 project
python3 -m unittest
```