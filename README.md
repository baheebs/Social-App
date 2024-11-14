# Project Setup Instructions

Welcome to our Django REST Framework project! Follow these steps to set up the project on your local machine:

## Prerequisites

- **Python**: Version 3.8 or above.
- **MySQL**: Installed locally.
- **Git**: For cloning the repository.

## Setup Steps

1. **Activate Your Environment**:

   - If you already have a Python environment set up, activate it:
     ```bash
     <your-env-name>\Scripts\activate
     ```

2. **Clone Repository**:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**:
   Create a database locally and configure the database and other values in the `.env` file. The `.env` file holds all the environment-specific variables.

5. **Apply Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run Server**:

   ```bash
   python manage.py runserver
   ```

   Access the project at [http://127.0.0.1:8000](http://127.0.0.1:8000).

   For swagger at  [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger/)

7. **Test APIs**:

   - Use Postman or Swagger to test the APIs.
   - Ensure the Postman collection and Swagger documentation are included in the deliverables.

## APIs Overview

1. **User Signup**: `/api/signup/` (POST) - Register with `name`, `email`, `mobile`, `username`, `password`.

2. **Create Post**: `/api/posts/` (POST) - Add `title`, `description`, `tags`, `date`.

3. **Publish/Un-publish Post**: `/api/posts/<post_id>/publish/` (UPDATE).

4. **List Posts**: `/api/posts/` (GET) - View posts by others with like count.

5. **Like/Un-like Post**: `/api/posts/<post_id>/like/` (POST).

If you encounter any issues during the setup process, please reach out to the project maintainers or consult the project documentation for further guidance.
