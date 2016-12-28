#DjangoHero : Django and Heroku for lazy humans
<img src="https://github.com/gutfeeling/djangohero/blob/master/logo/djangohero.png" alt="djangohero logo" width="200">

## Description

DjangoHero automates the process of starting a new Django project on Heroku. It sets everything up for you, 
so that you can start working on your project immediately without worrying about Heroku specific details.

## Example

To start a functional Heroku app called my_app running an empty Django project called my_django_project complete with a 
database, you need just one line.

```
djangohero deploy --app=my_app --database my_django_project
```

## Why?

Creating a Django app on Heroku usually requires the following steps:

1. Create a Django project using `django-admin startproject`.
2. Modify the Django project to conform to best practices outlined in 
   [Two Scoops of Django](https://www.twoscoopspress.com/products/two-scoops-of-django-1-8) or whatever 
   project structure suits your team best.
3. Create a settings file for Heroku and add Heroku specific database settings and static file settings.
4. For serving static files from Heroku, modify `wsgi.py` to use whitenoise.
5. Initialize a Git repository for the project.
6. Create the heroku app.
7. Add the app url to `ALLOWED_HOSTS` in the Django settings.
8. Set heroku config vars for `DJANGO_SETTINGS_MODULE` and `DJANGO_SECRET_KEY`. If you are using best practices for Django,
you'd need these.
9. Create `requirements.txt` containing required Python packages.
10. Create a `Procfile` containing information on the web process and `runtime.txt` containing information on the
preferred Python runtime.
11. Create a Heroku Postgres addon to set up a database.
12. Commit the changes to Git and push the changes to Heroku.
13. Scale the app.

I end up wasting a lot of time doing these things before I can actually start working on writing actual code. 
This is frustrating. This package solves the problem by automating the setup process. 

## Setup

Set it up like any other Python package. In particular, you can use the following steps.

###Git clone the project
```
git clone https://github.com/gutfeeling/djangohero.git
```
###Install with pip
```
pip install -e djangohero
```

## Usage

Installing djangohero will make the program `djangohero` available on your system. Here's how to use it.

### Syntax

```
djangohero deploy --app=<app_name> --region=<region> --database --database_type=<database_type> --python=<python_version> --container_name=<container_folder_name> <django_project_name>
```

### Explanation of options, flags and arguments

--app : name of the Heroku app; if absent, uses Heroku's imaginative app names

--region : [Geographical location of the app](https://devcenter.heroku.com/articles/regions)

--database : If this flag is present, a [database](https://devcenter.heroku.com/articles/heroku-postgresql) is created

--database_type : [name of the Heroku Postgres' plan tier](https://devcenter.heroku.com/articles/heroku-postgres-plans#plan-tiers)

--python : [Python runtime (either 2 or 3)](https://devcenter.heroku.com/articles/python-runtimes#supported-python-runtimes);
the default is Python 3

--container_name : Name of the container folder. If this option is absent, it uses the app name.

django_project_name : Name of the Django project

## Folder structure of the app

The created app uses the following folder structure for the Django project in accordance with 
[Two Scoops of Django](https://www.twoscoopspress.com/products/two-scoops-of-django-1-8) and 
Heroku's requirements. The folder structure can be 
changed without much trouble as well.
```
container_name
├── django_project_name
│   ├── django_project_name
│   │   ├── __init__.py
│   │   ├── settings
│   │   │   ├── __init__.py
│   │   │   ├── settings_base.py
│   │   │   └── settings_heroku.py
│   │   ├── urls.py
│   │   └── wsgi
│   │       ├── __init__.py
│   │       ├── wsgi_base.py
│   │       └── wsgi_heroku.py
│   └── manage.py
├── Procfile
├── requirements.txt
└── runtime.txt
```

### Compatibility
It should work on both Python 2 and 3.

### Requirements

You should have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed for this to work.

### Additional comments

There's another project called [heroku-django-template](https://github.com/heroku/heroku-django-template) that provides a 
Heroku template. It does not fit my use case as the template 
there does not conform to the best practices outlined in 
[Two Scoops of Django](https://www.twoscoopspress.com/products/two-scoops-of-django-1-8)
and it doesn't try to automate the other command line things. But it might fit yours, do check it out.

If you think similar stuff can be done for other languages that work on Heroku, we could create a unified project containing all the code. 
Drop me a line at dibyachakravorty@gmail.com

Finally, your contributions and suggestions to improve the process are most welcome. 



