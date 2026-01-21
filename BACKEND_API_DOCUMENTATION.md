# Backend API Documentation

This document provides a comprehensive overview of the backend APIs available for the mobile app, including Authentication, User Management, Wellness features, Community interactions, and the Chatbot.

## Table of Contents
1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Wellness & Mood](#wellness--mood)
4. [Activity Lounge](#activity-lounge)
5. [Chatbot & AI](#chatbot--ai)
6. [Journaling](#journaling)
7. [Community & Messaging](#community--messaging)
8. [Todos](#todos)
9. [Utilities](#utilities)

---

## Authentication

### Sign Up
Registers a new user.
- **Endpoint:** `/api/signup/`
- **Method:** `POST`
- **Request Body:**
    - `firstName` (string, required)
    - `lastName` (string, required)
    - `username` (string, required)
    - `email` (string, required)
    - `password` (string, required)
- **Response:**
    - **Success (201):** `{ "message": "User signed up successfully." }`
    - **Error (400):** `{ "errors": { "field": ["error message"] } }`

### Login
Authenticates a user and starts a session.
- **Endpoint:** `/api/login/`
- **Method:** `POST`
- **Request Body:**
    - `email` (string, required)
    - `password` (string, required)
- **Response:**
    - **Success (200):** `{ "message": "Login successful" }`
    - **Error (401):** `{ "error": "Invalid credentials" }`

### Get Token (JWT)
Obtain a JWT access and refresh token.
- **Endpoint:** `/api/token/`
- **Method:** `POST`
- **Request Body:**
    - `username` (string, required)
    - `password` (string, required)
- **Response:** `{ "refresh": "...", "access": "..." }`

### Refresh Token
Refresh an expired access token.
- **Endpoint:** `/api/token/refresh/`
- **Method:** `POST`
- **Request Body:**
    - `refresh` (string, required)
- **Response:** `{ "access": "..." }`

### Logout
Logs out the user.
- **Endpoint:** `/api/logout/`
- **Method:** `POST`
- **Response:** `{ "message": "Logout successful" }`

### Password Reset
- **Endpoint:** `/api/password_reset/`
- **Includes:** Endpoints for requesting reset, confirming token, etc. (Django Rest Password Reset standard endpoints)

### Send Verification Email
- **Endpoint:** `/api/send-verification-email/`
- **Method:** `POST` (Implied)
- **Request Body:** `{ "email": "user@example.com" }`

### Verify Code
- **Endpoint:** `/api/verification/`
- **Method:** `POST`
- **Request Body:**
    - `email` (string)
    - `code` (string)

---

## User Management

### Get User Data
Retrieve current authenticated user's data.
- **Endpoint:** `/api/user/`
- **Method:** `GET`

### Get User Username
- **Endpoint:** `/api/get-user-username/`
- **Method:** `GET`

### Get User Info Dashboard
- **Endpoint:** `/api/user-info-dashboard/`
- **Method:** `GET`

### User Settings
Get or update user settings (notifications, themes, visibility).
- **Endpoint:** `/api/settings/`
- **Method:** `GET`, `POST`
- **Request Body (POST):**
    - `email_notifications` (boolean)
    - `push_notifications` (boolean)
    - `sms_notifications` (boolean)
    - `profile_visibility` ("public" | "private")
    - `search_visibility` ("public" | "private")
    - `current_theme` ("light" | "dark")

### Delete Account
Permanently delete the authenticated user's account.
- **Endpoint:** `/api/delete-account/`
- **Method:** `DELETE`

### Profiles
- **Get Profile:** `GET /api/profiles/<str:username>/`
- **Update Profile:** `PUT /api/profiles/<str:username>/update/`
  - **Fields:** `firstName`, `lastName`, `username`, `email`, `whyHere`

---

## Wellness & Mood

### Mood Entries
Track daily mood ratings.
- **Endpoint:** `/api/mood-entries/`
- **Method:** `GET` (List), `POST` (Create)
- **Request Body (Create):**
    - `date` (date string, YYYY-MM-DD)
    - `mood_rating` (integer)
    - `notes` (string, optional)
- **Response:** List of mood entry objects or created object.

### Mood Entry Detail
- **Endpoint:** `/api/mood-entries/<int:pk>/`
- **Method:** `GET`, `PUT`, `DELETE`

### Mood Assessment
Comprehensive wellness assessment.
- **Endpoint:** `/api/mood-assessment/`
- **Method:** `POST`
- **Request Body:**
    - `happiness` (integer)
    - `anxiety` (string)
    - `energy` (string)
    - `sleep_quality` (integer)
    - `appetite` (integer)
    - `physical_health` (integer)
    - `concentration` (integer)
    - `social_connections` (integer)
    - `stress_level` (integer)

### Detect Mood (AI)
Detect mood from an uploaded image using AWS Rekognition.
- **Endpoint:** `/api/detect-mood/`
- **Method:** `POST`
- **Body:** Form Data
    - `image` (File)
- **Response:** `{ "mood": "HAPPY", "message": "...", "details": [...] }`

---

## Activity Lounge

These endpoints expose the curated content used in the Activity Lounge (movies, games, exercises, and sounds) so web and mobile clients can fetch the same data.

> Auth: Public read-only (no authentication required).

### Movies
- **Endpoint:** `/api/activity/movies/`
- **Method:** `GET`
- **Query Params (optional):**
    - `mood` (string) – filter by mood tag, e.g. `?mood=anxious`.
- **Response (example item):**
    - `id` (int)
    - `title` (string)
    - `description` (string)
    - `image_url` (string)
    - `external_url` (string)
    - `moods` (string, comma-separated tags – e.g. "anxious,low")

### Games
- **Endpoint:** `/api/activity/games/`
- **Method:** `GET`
- **Query Params (optional):**
    - `mood` (string) – filter by mood or category tag.
- **Response (example item):**
    - `id` (int)
    - `title` (string)
    - `description` (string)
    - `image_url` (string)
    - `play_url` (string)
    - `moods` (string, comma-separated tags)

### Exercises
- **Endpoint:** `/api/activity/exercises/`
- **Method:** `GET`
- **Query Params (optional):**
    - `mood` (string) – filter by mood tag.
- **Response (example item):**
    - `id` (int)
    - `name` (string)
    - `exercise_type` (string)
    - `reason` (string)
    - `gif_url` (string)
    - `moods` (string, comma-separated tags)

### Sounds
- **Endpoint:** `/api/activity/sounds/`
- **Method:** `GET`
- **Query Params (optional):**
    - `mood` (string) – filter by mood tag.
- **Response (example item):**
    - `id` (int)
    - `name` (string)
    - `category` (string)
    - `duration` (string)
    - `audio_url` (string)
    - `image_url` (string)
    - `moods` (string, comma-separated tags)

---

## Chatbot & AI

### Enhanced Chat
Main AI chat endpoint with context and history.
- **Endpoint:** `/api/chat/enhanced/`
- **Method:** `POST`
- **Auth:** Requires JWT – send `Authorization: Bearer <access_token>` header.
- **Request Body:**
    - `message` (string, required)
    - `thread_id` (integer, optional) - ID of existing thread to continue.
    - `thread_title` (string, optional) - Title for new thread.
- **Response:**
    - `response` (string) - AI response text.
    - `conversation_id` (int) - ID of this specific message exchange.
    - `thread_id` (int) - ID of the thread.
    - `intent` (string) - Detected intent (e.g., 'anxiety', 'greeting').

### Chat Threads
Manage conversation threads.
- **List/Create Threads:** `GET`, `POST` `/api/chat/threads/`
- **Thread Detail:** `GET` `/api/chat/threads/<int:thread_id>/`
- **Thread Messages:** `GET` `/api/chat/threads/<int:thread_id>/messages/` - Get history for a specific thread.

### Chat History Management
- **Full History:** `GET /api/chat/history/`
- **Delete All History:** `DELETE /api/chat/history/delete/`
- **Delete Conversation:** `DELETE /api/chat/history/<int:conversation_id>/delete/`
- **Get Log:** `GET /api/chat/history/log/`

### Chat Analytics
Get insights into conversation topics and sentiment.
- **Endpoint:** `/api/chat/analytics/`
- **Method:** `GET`

### Bot Settings
Configure the bot (e.g., name).
- **Endpoint:** `/api/bot-settings/`
- **Method:** `GET`, `PUT`
- **Body (PUT):**
    - `bot_name` (string)

---

## Journaling

### Journal Entries
Manage personal journal entries.
- **Endpoint:** `/api/journal-entries/`
- **Method:** `GET` (List all for user), `POST` (Create new)
- **Request Body (POST):**
    - `title` (string)
    - `content` (string)
    - `background_color` (string, hex code, e.g., "#ffffff")
- **Response:** JSON list or single entry object.

### Journal Detail
- **Endpoint:** `/api/journal-entries/<int:pk>/`
- **Method:** `GET`, `PUT`, `DELETE`

### Create Blog
Create a public blog post (Review process).
- **Endpoint:** `/api/create-blog/`
- **Method:** `POST` (Form Data)
    - `title`
    - `content`
    - `image` (file)
    - `fullname`
    - `email`

### Post List (Public)
- **Endpoint:** `/api/posts/`
- **Method:** `GET`

---

## Community & Messaging

### Communities
List and manage communities.
- **Endpoint:** `/api/communities/`
- **Method:** `GET`, `POST`... (ViewSet)
- **Fields:** `name`, `description`.

### Community Messages
Get or post messages to a specific community.
- **Endpoint:** `/api/community/<int:community_id>/messages/`
- **Method:** `GET`, `POST`
- **Request Body (POST):**
    - `content` (string)
    - `user` (id)
    - `community` (id)

### Message Management
- **Detail:** `GET /api/message/<int:pk>/`
- **Edit:** `PUT /api/message/<int:pk>/edit/`
- **Delete:** `DELETE /api/message/<int:pk>/delete/`
- **Get Sender:** `GET /api/messages/<int:message_id>/sender/`
- **Report Message:** `POST /api/report-message/<int:message_id>/`

---

## Todos

### Todo List
- **Endpoint:** `/api/todos/`
- **Method:** `GET` (List), `POST` (Create)
- **Request Body (POST):**
    - `text` (string)
    - `deadline` (date, YYYY-MM-DD)
- **Note:** Creating a todo automatically assigns it to the authenticated user.

### Todo Detail
- **Endpoint:** `/api/todos/<int:pk>/`
- **Method:** `GET`, `PUT`, `DELETE`

### Complete Todo
Mark a todo as completed.
- **Endpoint:** `/api/todos/<int:todo_id>/complete/`
- **Method:** `PUT`

---

## Utilities

### Contact Form
Send a contact message to the team.
- **Endpoint:** `/api/contact/`
- **Method:** `POST`
- **Body:** `name`, `email`, `phone`, `company`, `service_interest`, `message`.

### Book a Professional / Submit Booking Form
Used after a successful payment (e.g. Paystack) to send booking details to the Serenimind team and a confirmation email to the user.
- **Endpoint:** `/api/submit-form/`
- **Method:** `POST`
- **Body (JSON):**
    - `date` (string, e.g. `"2024-10-01"`)
    - `time` (string, e.g. `"15:30"`)
    - `reason` (string)
    - `phoneNumber` (string)
    - `email` (string)
    - `language` (string)
    - `plan` (string – e.g. selected plan name)
    - `anonymous` (boolean)
    - `paymentReference` (string – reference from payment gateway)
- **Response:** `{ "message": "Form submitted successfully." }`

### Send Email (Generic)
- **Endpoint:** `/api/send-email/`
- **Method:** `POST`
- **Body:** `user_name`, `user_email`, `message`.

### Subscribe Newsletter
- **Endpoint:** `/api/subscribe-newsletter/`
- **Method:** `POST`
- **Body:** `user_email`.

### Open Library Proxy
Search for books via Open Library.
- **Endpoint:** `/api/open-library-proxy/`
- **Method:** `GET`
- **Query Params:** `q` (query), `limit` (default 20).
