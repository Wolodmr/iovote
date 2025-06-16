<div class="pdf-header"></div>

# Project Structure

The *ioVote* project is structured into multiple Django apps, each responsible for specific functionality. Below is an overview of the key apps and their roles.

## Main Apps

### 1. `main`
- Handles the homepage and general static pages.
- Manages site-wide settings.

### 2. `users`
- Manages authentication (signup, login, logout).
- Stores user profiles and permissions.

### 3. `voting_sessions`
- Core functionality for creating and managing voting sessions.
- Stores voting options and tracks votes.

### 4. `results`
- Processes and displays voting results.
- Future integration with Dash for visual analytics.

## Additional Components

### - `templates/`
Contains HTML templates for frontend rendering.

### - `static/`
Includes CSS, JavaScript, and image assets.

### - `media/`
Holds user-uploaded files (if applicable).

### - `config/`
Global project settings and configurations.

This modular structure ensures maintainability and scalability for future enhancements.
