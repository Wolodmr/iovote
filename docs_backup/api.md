# API & Forms

The *Vote Cast* project primarily relies on Django's built-in form handling and does not expose a public API. However, it utilizes Django forms and views effectively for handling user input and interactions.

## 1. Forms in *Vote Cast*
Django forms are used to validate and process user inputs securely. Below are the key forms implemented:

### **1.1 User Authentication Forms**
- **LoginForm** – Handles user login with validation.
- **SignupForm** – Manages new user registration with validation for unique usernames and secure passwords.

### **1.2 Voting Forms**
- **VoteForm** – Captures user votes, ensuring one vote per session.
- **OptionForm** – Used by admins to create or update voting options.

### **1.3 Admin Management Forms**
- **SessionForm** – Enables admins to create and manage voting sessions.
- **ResultForm** – Allows for the management of voting results.

## 2. API-Like Behavior (If Extended in the Future)
Currently, *Vote Cast* does not include a REST API, but Django’s built-in **class-based views (CBVs)** and **Django Forms** serve as an efficient way to handle user interactions.

### **Possible Future API Enhancements**
If an API is added in the future, it might include:
- **User Authentication API** (Token-based authentication for external apps)
- **Voting API** (Allow users to cast votes via API calls)
- **Results API** (Retrieve results in JSON format)

For now, all interactions happen through Django views and forms within the web interface.
