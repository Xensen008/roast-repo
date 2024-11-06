# Code Critic: Your AI-Powered Code Roaster and README Generator

Code Critic is a cutting-edge tool designed to analyze your code, provide insightful (and sometimes cheeky) feedback, and automatically generate comprehensive README files.  It leverages the power of Gemini AI to deliver accurate and engaging code analysis, helping you improve code quality and documentation simultaneously.

## Key Features

* **AI-Powered Code Analysis:**  Code Critic uses Gemini AI to analyze your codebase, identifying potential issues, suggesting improvements, and even offering witty "roasts" about your coding style.

* **README Generation:**  Say goodbye to tedious README writing! Code Critic automatically generates detailed and well-structured README files based on your code, saving you time and effort but u have to bear with the roast.

* **Support for Multiple Languages:**  Code Critic supports a variety of programming languages, ensuring compatibility with your projects.

* **Clear and Concise Reporting:**  Receive clear and concise reports outlining the analysis results and generated README content.

## Project Architecture

Code Critic follows a client-server architecture with a clear separation between the frontend and backend.

* **Frontend (React):**  The frontend is built using React and provides a user-friendly interface for interacting with the tool.  Users can upload their code, configure analysis settings, and view the generated README.
* **Backend (FastAPI):** The backend is powered by FastAPI and handles the core logic, including code analysis using Gemini AI, README generation, and communication with the frontend.


## Installation & Setup

### Frontend

1. Navigate to the `frontend` directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

### Backend

1. Navigate to the `backend` directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the backend server: `uvicorn main:app --reload`

## Environment Variables

The following environment variables are required for the backend:

* `GEMINI_API_KEY`: Your Gemini API key.


## Usage Guide

1. **Upload Code:**  Use the frontend interface to upload your code files.
2. **Configure Analysis:** Select the desired roasting level and any other analysis options.
3. **Generate README:** Click the "Generate README" button.
4. **Review and Copy:** Review the generated README and download it to your project.


## Technologies Used

* [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
* [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
* [![Gemini](https://img.shields.io/badge/Gemini-FF69B4?style=for-the-badge&logo=Gemini)](https://google.ai/gemini)
* [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)


