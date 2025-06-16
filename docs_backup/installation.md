<div class="pdf-header"></div>

# Installation Guide   

This guide will help you install and set up the **ioVote** project on your local machine.

## **Prerequisites**  
Before installation, make sure you have the following installed:  

✅ Python 3.10+  
✅ Git  
✅ Virtual environment (`venv`)  
✅ PostgreSQL (optional, for production setup)  


## **Installation Steps**  

 💡 **Step 1: Clone the Repository**
   
Run the following command to clone the project from GitHub:  

```sh
git clone https://github.com/Wolodmr/iovote.git
cd iovote
```



💡 **Step 2: Create a Virtual Environment**

🔹 Create a virtual environment to manage dependencies:


`python -m venv venv`


🔹 **Activate the virtual environment:**

- **Windows:** 

`venv\Scripts\activate`


- **Mac/Linux:**  

  `source venv/bin/activate`


💡 **Step 3: Install all required dependencies using `pip`:**

`pip install -r requirements.txt`


📌 This will install Django, required libraries, and other dependencies necessary for the project.

💡 **Step 4: Apply database migrations to set up the database schema:**

`python manage.py migrate`

📌 This step initializes all necessary database tables for user authentication, voting sessions, and results tracking.

💡 **Step 5: To access the admin panel, create a superuser by running:**

`python manage.py createsuperuser`

✏️ Follow the prompts to set up an admin username, email, and password.

💡 **Step 6: Start the Django development server:**

`python manage.py runserver`

🚀 Once the server starts, open your browser and visit:  

🔗 [http://127.0.0.1:8000](http://127.0.0.1:8000) 🎉  
