# Project Overview

This project is a Django-based API for an Angular application. It also utilizes the Django Admin for project management. This document provides essential information about the project for development and maintenance purposes.

## Core Technologies

*   **Language:** Python 3.12.3
*   **Framework:** Django 4.2.13
*   **AI:** OpenAI API (gpt-4o-mini) is used for the chat functionality.

## Key Architectural Patterns

### Conversational Authentication

For the primary chat interface, the application does not use a traditional username/password login. Instead, it employs a conversational authentication method:

1.  A user initiates a chat session without prior authentication.
2.  An AI assistant asks the user for their **passport number** and **last name**.
3.  The `employee/views.py:Chat.get_user` function validates these details against the `Employee` model in the database.
4.  Upon successful validation, a token from the frontend is saved to the employee's record, effectively "logging in" the user for that session.

### Token-Based API Authentication

For other protected API endpoints, the application uses token-based authentication.

*   **`expatcare.authentication.EmployeeTokenAuthentication`**: A custom authentication class that validates requests by checking for a valid token in the `Employee` model.
*   This is configured as the default authentication method in `expatcare/settings.py`.

## Dependencies

All Python dependencies are listed in the `requirements.txt` file. Key libraries include `Django`, `djangorestframework`, and `openai`.

## Development Environment

### Virtual Environment

This project uses a Python virtual environment located in the `venv/` directory. To activate it, run the following command:

```bash
source venv/bin/activate
```

### Running Tests

The project uses Django's built-in testing framework. To run the tests, use the following command:

```bash
python manage.py test
```

## Deployment

The application is served using **Apache**. After making changes to the code, you need to restart the Apache server for the updates to take effect in the live environment.

```bash
# Example command to restart Apache (the exact command may vary)
sudo systemctl restart apache2
```