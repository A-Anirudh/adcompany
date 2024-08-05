# Django User Authentication API

This is a Django project that provides user registration and login functionality using Django Rest Framework (DRF) and PostgreSQL as the database.

## Features

- User registration with email, first name, last name, and password
- User login with email and password
- Custom user model
- API endpoints for registration and login

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL
- Virtualenv (optional, but recommended)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/A-Anirudh/adcompany.git
   cd adcompany
   ```
   Create virtual environment and install the required dependencies
   Linux:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Windows:
   ```bash
   python -m venv venv
   venv/Scripts/Activate
   ```

   install the dependencies by running the following command
   ```bash
   pip install -r requirements.txt
   ```

   Ensure postgreSQL is installed with required setup. Contact owner of this repo for details.

   ```bash

   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

   python manage.py runserver
   ```


   Login route -> /api/login
   
   Registration route -> /api/register

   
   
