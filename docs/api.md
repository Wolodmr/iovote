<div class="pdf-header"></div>

# API & Forms

The *Vote Cast* project uses Django's built-in forms for handling user input but does not currently expose a public API.

## Forms Overview
Django forms validate and process user input securely. The key forms include:

### **Authentication Forms**
- **LoginForm** – User login validation.
- **SignupForm** – Registers new users with secure credentials.

### **Voting Forms**
- **VoteForm** – Ensures one vote per session.
- **OptionForm** – Manages voting options (admin use).

### **Admin Forms**
- **SessionForm** – Manages voting sessions.
- **ResultForm** – Handles voting results.

## API-Like Behavior & Future Enhancements
While *Vote Cast* lacks an API, Django's class-based views and forms provide structured interactions. Potential future additions:
- **User Authentication API** – Token-based login.
- **Voting API** – Cast votes via API.
- **Results API** – Retrieve results in JSON.

Currently, all interactions are web-based using Django forms.
