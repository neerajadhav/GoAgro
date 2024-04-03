
# GoAgro
A social media platform for agriculture sector 

## [Demo video](https://drive.google.com/file/d/1E-Zy4Zat2XYIHKrz0iaB9Ii77jSuSdsI/view?usp=sharing)

## Features 
 - Mobile first **Modern design**
 - Users can **create**, **delete**, **edit**, **like** posts and make **comments** on them
 - **Newspaper** section, where all **agriculture** and **farmers** related news is served from various trusted sources
 -  A **Marketplace** to make it easy for farmers to **find stores** located in their area
- Friend system, **send**, **accept** friend requests
- **Weather updates** for searched location
## Tech Stack

### FrontEnd
 - HTML5
 - CSS
 - JavaScript
 - Bootstrap 5
 - Jquery 

###  Backend

 - Django Python Web Framework
 - SQLite for Database
 - GitHub

## Getting started
###   Requirements
 - Python 3.6+
 - pip
 - virtualenv 

###  Installation
```bash
# Clone the repository
git clone https://github.com/neerajadhav/GoAgro.git

# Enter into the directory
cd GoAgro/

# Create virtual environment 
python -m venv .venv

# Activate virtual environment 
source .venv/bin/activate # for linux
source .venv/Source/activate # for windows

# Install the dependencies
pip install -r requirements.txt

# Check migrations.
python manage.py makemigrations

# Apply migrations.
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Set .env
cp .env.example .env
# set the values in .env file

#Starting the application
python manage.py runserver
```
