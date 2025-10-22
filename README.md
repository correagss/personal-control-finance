# PERSONAL FINANCE CONTROL 📊

A Full-Stack web application for personal finance management, allowing users to register, log in, and manage their income and expense transactions.

**Access the live application:** [**https://[https://personal-finance-app-8tkn.onrender.com]**](https://[URL OF YOUR APP ON RENDER])

---

![Login Screen of the App](https://via.placeholder.com/800x450.png/1e1e1e/00aaff?text=Screenshot+of+Login+Screen)
*Login screen with a dark theme.*

![Dashboard Screen](https://via.placeholder.com/800x450.png/1e1e1e/00aaff?text=Screenshot+of+Dashboard)
*Main dashboard showing the current balance, form, and transaction list.*

---

## 🚀 About The Project

This project was developed as a complete solution for personal finance management. The application supports multiple user registrations, ensuring that each user's data remains private and secure. The interface, built with React, is reactive and modern, providing a fluid user experience for adding, viewing, editing, and deleting transactions.

## ✨ Features

*   **Secure Authentication:** Complete registration and login system with password hashing (Argon2) and JWT-based authentication.
*   **Data Privacy:** Each user only has access to their own financial transactions.
*   **Full CRUD:** Functionality to Create, Read, Update, and Delete transactions.
*   **Interactive Dashboard:** Real-time balance view and a transaction list with visual indicators for income (green) and expenses (red).
*   **Modern Design:** A dark-themed interface with a responsive layout, focused on user experience.

## 🛠️ Tech Stack

This project is a monorepo that integrates a Python backend with a React frontend.

#### **Backend (API)**
*   **Python 3.12**
*   **FastAPI:** For building the RESTful API.
*   **SQLAlchemy:** As the ORM for database interaction.
*   **PostgreSQL (Neon):** Cloud-based relational database.
*   **Passlib & Python-JOSE:** For password hashing and JWT management.
*   **Uvicorn:** As the ASGI server.

#### **Frontend**
*   **React.js 18**
*   **Vite:** As the development environment and build tool.
*   **React Router:** For route and navigation management.
*   **JavaScript (ES6+)**
*   **CSS3:** For component-based styling.

#### **Deployment**
*   **Render:** For hosting the Web Service (Backend) and the Static Site (Frontend).
*   **Git & GitHub:** For version control and CI/CD.

---

## ⚙️ Running The Project Locally

Follow the steps below to set up and run the application in your development environment.

### Prerequisites
*   **Python** (version 3.8 or higher)
*   **Node.js** and **npm**

### Backend

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/personal-control-finance.git
    cd personal-control-finance
    ```
2.  **Create and activate the virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/Scripts/activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start the backend server:**
    ```bash
    uvicorn app.main:app --reload --reload-dir app
    ```
    The backend will be running at `http://127.0.0.1:8000`.

### Frontend

1.  **Navigate to the frontend folder:**
    ```bash
    cd frontend
    ```
2.  **Install JavaScript dependencies:**
    ```bash
    npm install
    ```
3.  **Create a `.env` file** in the `frontend` folder with the following content:
    ```    VITE_API_URL=http://127.0.0.1:8000
    ```
4.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`.

---

## Author

**Gabriel Corrêa**

*   **GitHub:** [@correagss](https://github.com/correagss)
*   **LinkedIn:** [www.linkedin.com/in/gabrielcorreasv]