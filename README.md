#DjangoHero
<img src="https://github.com/gutfeeling/djangohero/blob/master/logo/djangohero.png" alt="djangohero logo" width="200">

## Description

DjangoHero is the fastest way to set up a Django project on the cloud (using Heroku). Starting a Django project using DjangoHero will 

1. Set up the Django project with a folder structure that follows best practices.
2. Make the Django project live on the cloud (Heroku) immediately.
3. Provision a database on the cloud (Heroku postgres) and connect your appication to it.

Best part : all of this happens with a single command under a minute without any input from your side. This is as good as plug and play gets.

## Example

To start a Heroku app called `my_app` running an empty Django project called `my_django_project`, complete with a 
database, we need to run the following command. Try it out, it works like a charm.

```
djangohero deploy --app=my_app --database my_django_project
```

## Why is this useful?

Creating a Django app on Heroku usually requires the following steps (you don't have to read all of them, just notice how many there are):

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

These boring steps have to be repeated for every project before we can get it to go live on the cloud. This package solves the problem by automating the setup process and making the application live on the cloud from birth. 

## Installation

The following steps are recommended.

###Git clone this repo
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
djangohero deploy --app=<app_name> --region=<region> --scale=<scale> --database --database_type=<database_type> --python=<python_version> --container_name=<container_folder_name> <django_project_name>
```

### Explanation of options, flags and arguments

**--app** : Name of the Heroku app; defaults to Heroku's imaginative app names.

**--region** : [Geographical location of the app](https://devcenter.heroku.com/articles/regions); defaults to us.

**--scale** : [Scale of the dynos](https://devcenter.heroku.com/articles/scaling); defaults to 1.

**--database** : If this flag is present, a [database](https://devcenter.heroku.com/articles/heroku-postgresql) is created.

**--database_type** : [Name of the Heroku Postgres' plan tier](https://devcenter.heroku.com/articles/heroku-postgres-plans#plan-tiers); defaults to hobby-dev.

**--python** : [Python runtime (either 2 or 3)](https://devcenter.heroku.com/articles/python-runtimes#supported-python-runtimes);
defaults to Python 3.

**--container_name** : Name of the container folder; defaults to app name.

**django_project_name** : Name of the Django project.

## Folder structure of the app

The created app uses the following folder structure for the Django project in accordance with 
[Two Scoops of Django](https://www.twoscoopspress.com/products/two-scoops-of-django-1-8) and 
Heroku's requirements. The folder structure can be 
changed without much trouble as well by changing the template.
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

## A note about migrations

Because of the project structure, you need to execute the following commands for migrations

```
heroku run django_project_name/manage.py makemigrations
heroku run django_project_name/manage.py migrate
```

## Compatibility
Works on both Python 2 and 3.

## Requirements

You should have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and Git installed for this to work. You need
to logged into Heroku at the time of running `djangohero`. You can login to Heroku by using the following command.

```
heroku login
```

## Additional comments

There's another project called [heroku-django-template](https://github.com/heroku/heroku-django-template) that provides a 
Heroku template. It does not fit my use case as the template 
there does not conform to the best practices outlined in 
[Two Scoops of Django](https://www.twoscoopspress.com/products/two-scoops-of-django-1-8)
and it doesn't try to automate the other command line things. But it might fit yours, do check it out.

If you think similar stuff can be done for other languages that work on Heroku, we could create a unified project containing all the code. 
Drop me a line at dibyachakravorty@gmail.com

Finally, your contributions and suggestions to improve this project is most welcome. 



