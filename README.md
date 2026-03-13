# Online Course Management System (OCMS)
<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/30fcdebd-7642-4332-b02f-40ac3ea3b17e" />

## Project Overview

The **Online Course Management System (OCMS)** is a backend-driven Learning Management System (LMS) built using **Django and Django REST Framework**. The platform enables students to enroll in courses, instructors to manage course content, and administrators to monitor platform activity and analytics.

The system implements **JWT-based authentication**, ensuring secure access to APIs. To improve performance and scalability, **Redis caching** is used for frequently accessed public endpoints and analytics data.

The project is designed with a **modular Django architecture**, where each major feature of the system is implemented as a separate Django application.

---

# Key Features

## User Authentication and Authorization

The system supports secure authentication using **JSON Web Tokens (JWT)**.

Users are categorized into three roles:

* **Student** – Can browse courses, enroll, and track progress.
* **Instructor** – Can create and manage courses.
* **Admin** – Has complete access to platform analytics and management.

Authentication features include:

* User registration
* Login and JWT token generation
* Token refresh
* Logout functionality
* Role-based API access control

---

# Technology Stack

## Backend

* Python
* Django
* Django REST Framework

## Authentication

* JSON Web Tokens (JWT)
* Access tokens and refresh tokens

## Database

* PostgreSQL

## Caching Layer

* Redis

## Frontend

* HTML
* CSS
* JavaScript

## Version Control

* Git

## Repository Hosting

* GitHub

---

# System Architecture

The system follows a **three-layer architecture**:

User Interface (Frontend)
↓
Django REST API (Backend)
↓
PostgreSQL Database + Redis Cache

### Request Flow

1. Client sends request to API.
2. Django processes request through serializers and views.
3. PostgreSQL handles persistent data storage.
4. Redis caches frequently accessed endpoints.
5. Response is returned to the frontend.

---

# Django Project Structure

The OCMS system follows a **modular Django architecture**.

```
ocms/
│
├── accounts/        # User authentication and role management
├── courses/         # Course, category, modules, lectures
├── enrollments/     # Student enrollment and progress tracking
├── reviews/         # Course ratings and feedback
├── dashboard/       # Admin analytics and platform insights
│
├── manage.py
└── README.md
```

Each application contains the following files:

```
models.py
serializers.py
views.py
urls.py
admin.py
```

---

# Application Modules

## 1. Accounts App

Handles user management and authentication.

Features:

* Custom user model
* Role-based permissions
* JWT authentication
* User registration and login
* Token refresh
* User profile management

User roles include:

* Student
* Instructor
* Admin

---

## 2. Courses App

Manages the complete course structure.

Features:

* Course creation and management
* Category management
* Course modules
* Lecture organization
* Public course listing APIs
* Redis caching for course lists

Each course contains:

* Modules
* Lectures
* Instructor details
* Pricing and level information

---

## 3. Enrollments App

Handles course enrollment and progress tracking.

Features:

* Student enrollment
* Duplicate enrollment prevention
* Progress calculation
* Course completion status

This module links students to the courses they are enrolled in.

---

## 4. Reviews App

Handles course feedback and ratings.

Features:

* Students can review courses
* Rating system (1–5 stars)
* Review comments
* One review allowed per student per course
* Average rating calculation

---

## 5. Dashboard App

Provides administrative analytics.

Features include:

* Total users
* Total courses
* Total enrollments
* Most popular courses

Redis caching is used for analytics queries to improve performance.

---

# API Endpoints

## Authentication APIs

```
/api/auth/register/
/api/auth/login/
/api/auth/refresh/
/api/auth/logout/
/api/auth/profile/
```

---

## Course APIs

```
/api/courses/
/api/courses/{id}
/api/categories/
/api/instructor/courses/
```

---

## Enrollment APIs

```
/api/enroll/
/api/my-courses/
/api/course/{id}/progress
```

---

## Review APIs

```
/api/courses/{id}/reviews/
/api/reviews/my/
```

---

## Admin Analytics APIs

```
/api/admin/analytics/
/api/admin/top-courses/
```

---

# Database Design

The system uses **PostgreSQL** with a normalized relational schema.

## User Table

| Field      | Type             | Description                  |
| ---------- | ---------------- | ---------------------------- |
| id         | UUID / BIGSERIAL | Primary Key                  |
| email      | VARCHAR          | Unique login email           |
| password   | VARCHAR          | Hashed password              |
| full_name  | VARCHAR          | User full name               |
| role       | ENUM             | STUDENT / INSTRUCTOR / ADMIN |
| is_active  | BOOLEAN          | Account status               |
| created_at | TIMESTAMP        | Account creation time        |

Indexes:

* email
* role

---

## Category Table

| Field | Type    |
| ----- | ------- |
| id    | SERIAL  |
| name  | VARCHAR |
| slug  | VARCHAR |

---

## Course Table

| Field         | Type    |
| ------------- | ------- |
| id            | SERIAL  |
| title         | VARCHAR |
| description   | TEXT    |
| price         | DECIMAL |
| level         | ENUM    |
| instructor_id | FK      |
| category_id   | FK      |
| is_published  | BOOLEAN |

---

## Module Table

| Field     | Type    |
| --------- | ------- |
| id        | SERIAL  |
| course_id | FK      |
| title     | VARCHAR |
| order     | INTEGER |

Constraint:

```
UNIQUE(course_id, order)
```

---

## Lecture Table

| Field     | Type    |
| --------- | ------- |
| id        | SERIAL  |
| module_id | FK      |
| title     | VARCHAR |
| video_url | TEXT    |
| notes     | TEXT    |
| order     | INTEGER |
| duration  | INTEGER |

Constraint:

```
UNIQUE(module_id, order)
```

---

## Enrollment Table

| Field       | Type      |
| ----------- | --------- |
| id          | SERIAL    |
| student_id  | FK        |
| course_id   | FK        |
| status      | ENUM      |
| enrolled_at | TIMESTAMP |

Constraint:

```
UNIQUE(student_id, course_id)
```

---

## Lecture Progress Table

Tracks which lectures a student has completed.

| Field         | Type      |
| ------------- | --------- |
| id            | SERIAL    |
| enrollment_id | FK        |
| lecture_id    | FK        |
| completed     | BOOLEAN   |
| completed_at  | TIMESTAMP |

---

## Reviews Table

| Field      | Type    |
| ---------- | ------- |
| id         | SERIAL  |
| student_id | FK      |
| course_id  | FK      |
| rating     | INTEGER |
| comment    | TEXT    |

Constraint:

```
UNIQUE(student_id, course_id)
```

---

# Redis Caching Strategy

Redis is used to cache frequently accessed data such as:

* Public course listings
* Platform analytics
* Top courses

Example cache keys:

```
admin:users:count
admin:courses:count
admin:top:courses
admin:enrollments:count
```

Typical cache expiration time:

```
5 – 15 minutes
```

---

# Security Implementation

The platform uses **JWT authentication**.

Security features include:

* Stateless access tokens
* Refresh tokens
* Role validation in JWT claims
* Secure password hashing
* Protected API endpoints

Refresh token blacklisting can be implemented using Redis or a blacklist table.

---

# Scalability and Optimization

The OCMS backend is optimized for scalability through:

* Normalized database schema
* Indexed database queries
* Redis caching layer
* Stateless JWT authentication
* Modular Django architecture

This design supports scaling horizontally for larger user bases.

---

# Evaluation Criteria

The project implementation is evaluated based on:

| Component                        | Weight |
| -------------------------------- | ------ |
| API Design                       | 30%    |
| JWT Authentication & Permissions | 20%    |
| Redis Caching                    | 15%    |
| Database Design                  | 15%    |
| Code Structure & Quality         | 20%    |

---

# Author

**Ammu S**
B.Tech Computer Science Engineering
Lovely Professional University

---

# License

This project is created for **educational and academic purposes**.
