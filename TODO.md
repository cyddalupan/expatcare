Overall Goal: Build a comprehensive test suite for this Django project, which serves as an API for an Angular application and is managed via the Django Admin. The primary objective is to achieve at least 80% test coverage. This will ensure all existing API endpoints and admin functionalities are working as expected, prevent future regressions, and enable safe code refactoring. All tests will use the `setUpTestData` method for efficient and consistent test data creation.

---

### Phase 0: Setup and Initial Analysis

- [x] **Install Coverage.py**: Add `coverage` to `requirements.txt` to enable test coverage measurement.
- [x] **Install Dependencies**: Run `pip install -r requirements.txt` to install the newly added `coverage` package.
- [x] **Analyze Firebase Usage**: Search the codebase for imports of `firebase_utils` to determine if it is actively used or can be removed.
- The search for `firebase_utils` only returned a match in the `TODO.md` file, indicating that the `firebase` app and `firebase_utils.py` file are not being used and can be removed.
- [x] **Establish Initial Coverage Baseline**: Run `coverage run manage.py test` to execute the existing test suite under coverage monitoring.
- [x] **Generate Baseline Report**: Run `coverage report` to view the initial coverage percentage before new tests are added.

### Phase 1: App-by-App Testing

---

#### App: `advance` (Blueprint)

- [x] **Create Test Files**: Create `advance/test_admin.py`, `advance/test_views.py`, and `advance/test_models.py`.
- [x] **Setup Admin Test Case**: In `advance/test_admin.py`, create a `TestCase` with a `setUpTestData` class method to create a reusable superuser and any other required baseline data.
- [x] **Test `Setting` Admin List View**: Verify the admin list view for `Setting` loads (200 OK).
- [x] **Test `Setting` CRUD**: Write individual tests for creating, updating, and deleting a `Setting` object through the admin interface.
- [x] **Test `Setting` Admin Search & Filter**: Write tests to use the `search_fields` (`name`) and `list_filter` (`value_type`) and confirm they work.
- [x] **Test `AICategory` Admin List View**: Verify the admin list view for `AICategory` loads (200 OK).
- [x] **Test `AICategory` CRUD**: Write individual tests for creating, updating, and deleting an `AICategory` object.
- [x] **Test `AICategory` Custom Form**: Write a test to specifically validate the usage of `AICategoryForm` in the admin.
- [x] **Test `SettingViewSet` API (Full CRUD)**: Write tests for `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` on the `/settings/` endpoint.
- [x] **Test `SettingViewSet` Permissions**: Ensure unauthenticated requests to `/settings/` are rejected with a `401` or `403` error.
- [x] **Test `advance` Model Logic**: Review models for custom methods and write specific tests for them.

---

### Phase 2: Investigation and Testing of Remaining Apps

The same detailed investigation and testing process will be applied to the following apps.

- [x] **Investigate and Test `cases` App**: Apply the full testing blueprint (Admin, API, Models) to the `cases` app.
- [x] **Investigate and Test `chats` App**: Apply the full testing blueprint (Admin, API, Models) to the `chats` app.
- [x] **Refactor `ChatHistoryView` Authentication**: Refactor the `ChatHistoryView` to use a secure token-based authentication method instead of passing the token in the URL.
- [x] **Investigate and Test `employee` App**: Apply the full testing blueprint (Admin, API, Models) to the `employee` app.
- [ ] **Investigate and Test `fra` App**: Apply the full testing blueprint (Admin, API, Models) to the `fra` app.
- [ ] **Investigate and Test `reviewhub` App**: Apply the full testing blueprint (Admin, API, Models) to the `reviewhub` app.
- [ ] **Investigate and Test `statement_of_facts` App**: Apply the full testing blueprint (Admin, API, Models) to the `statement_of_facts` app.
- [ ] **Investigate and Test `support` App**: Apply the full testing blueprint (Admin, API, Models) to the `support` app.