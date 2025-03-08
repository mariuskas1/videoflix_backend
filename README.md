# Videoflix

## Description
Videoflix is a Django REST Framework (DRF) video streaming platform, with built-in user authentication.


---

## Tech Stack
- **Python**: 3.x
- **Django**: 5.1.6
- **Django REST Framework**: 3.15.2
- **Django Redis**: 5.4.0
- **Django RQ**: 2.5.1
- **RQ**: 1.10.0
- **CORS Headers**: 4.7.0
- **SQLParse**: 0.5.3
- **ASGIRef**: 3.8.1
- **Redis**: 3.5.3
- **Database**: PostgreSQL

---

## Installation

### Clone the Repository
```sh
git clone https://github.com/mariuskas1/videoflix_backend.git
cd videoflix_backend
```
### Create a Virtual Environment
```sh
python -m venv env
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```
### Install Dependencies
```sh
pip install -r requirements.txt
```
### Apply Migrations
```sh
python manage.py migrate
```
### Start the Development Server
```sh
python manage.py runserver
```
The API will be available at http://127.0.0.1:8000/

## API Endpoints

### Authentication & User Management

- **POST** `/registration/` - Register a new user  
- **POST** `/login/` - Log in and obtain an authentication token  
- **POST** `/token/validate/` - Validate authentication token  
- **GET** `/activate/<uidb64>/<token>/` - Activate a user account via email verification  
- **POST** `/password-reset/` - Request a password reset link  
- **POST** `/pw-reset-confirm/<uidb64>/<token>/` - Reset the password  
- **POST** `/check-email/` - Check if an email is registered  


### Video Management

- **GET** `/videos/` - Retrieve all videos  
- **POST** `/videos/` - Create a new video  
- **GET** `/videos/{id}/` - Retrieve a specific video  
- **PUT** `/videos/{id}/` - Update a video  
- **PATCH** `/videos/{id}/` - Partially update a video  
- **DELETE** `/videos/{id}/` - Delete a video  


