# Library Management Web Application

A web application for managing a local library's books, members, and transactions.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This Library Management Web Application is designed to simplify the tasks of librarians in tracking books, members, and transactions. The application provides a user-friendly interface for performing various operations related to library management.

## Features

- CRUD Operations for Books and Members
- Issuing and Returning Books
- Member Registration and Dismissal
- Book Search by Name and Author
- Rent Fee Calculation on Book Returns

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript/jQuery
- **Database**: SQLite (You can use other databases if needed)
- **Other Tools**: SQLAlchemy (for database ORM)

## Project Structure

The project is organized as follows:


- `app`: Contains the Flask backend code.
- `frontend`: Holds the HTML templates, CSS styles, and JavaScript for the front end.
- `venv`: Virtual environment for Python dependencies.
- `config.py`: Configuration settings for the application.
- `run.py`: Main entry point for the Flask application.

## Getting Started

## Backend Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd library_management
   
2. Install Flask and required dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install Flask
   pip install flask-sqlalchemy
   pip install flask-restful

3. Configure the database in config.py. By default, it uses SQLite.
4. Initialize and migrate the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade

5. Run the Flask application:

   ```bash
   python run.py

## Frontend Setup
Inside the frontend directory, create HTML templates, CSS styles, and JavaScript files for your front end.

Serve the front end templates using Flask routes as described in the backend setup section.

You can add your front-end logic, styles, and interactions in the respective files.

Usage
Access the web application by navigating to http://localhost:5000 in your web browser.
Use the application to manage books, members, and transactions as per the provided features.

### Screenshots
<img width="1440" alt="Screenshot 2023-09-25 at 00 51 56" src="https://github.com/NeemaRhonnahMkenda/Library-Management-System/assets/115183776/651fcb22-c991-4839-885a-165290b815d2">
<img width="1428" alt="Screenshot 2023-09-25 at 00 53 34" src="https://github.com/NeemaRhonnahMkenda/Library-Management-System/assets/115183776/f9e7ebf1-c5be-46fa-95d8-322550d1ccbd">






