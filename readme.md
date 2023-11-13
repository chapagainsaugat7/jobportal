# Online Job Portal
For my BCA 6th-semester project, I developed an advanced "Online Job Portal" using Django. This platform facilitates job searches, allowing employers to post listings, questions for assessment, and shortlist candidates through the platform directly. And candidates can apply, give assessment, upload resume and track the status of job. It incorporates user-friendly interfaces, resume uploading, and search capabilities, contributing to a streamlined and efficient recruitment process.

# ⚪ Installation Guide

## Create Virtual Environment
```shell
    python venv env_name
```

## Activate Virtual Environment
```py
    env_name\Scripts\activate
```

## Install all required files
```shell
    pip install requirements.txt
    (sometimes with -r flag)
```
## Create migrations
```shell
    python manage.py makemigrations
    python manage.py migrate
```
If it is only creating migration for admin, you may use migration command with app name. (ie. employer, jobseeker)

## Run Development Server
```shell
    python manage.py runserver
```


##

Happy Coding 🤞