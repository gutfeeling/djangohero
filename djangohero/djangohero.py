#!/usr/bin/env python

import argparse
import subprocess
import sys
import re
import random
import shutil
import os

class DjangoHero(object):

    def __init__(self, args):
        self.args = args
        self.steps = 10
        self.requirements_text = ("dj-database-url==0.4.1\n"
                                  "Django==1.10.4\n"
                                  "gunicorn==19.6.0\n"
                                  "psycopg2==2.6.2\n"
                                  "whitenoise==3.2\n"
                                  "Unipath==1.1")

    def create_root_directory(self, direction):
        if direction == "execute":
            if self.args.container_name is None and self.args.app is None:
                raise ValueError("app_name and container_name cannot both be"
                    " empty.")
            elif self.args.container_name is None:
                self.container_name = self.args.app
            else:
                self.container_name = self.args.container_name
            os.makedirs(self.container_name)
            os.chdir(self.container_name)
            print("Created container folder.")
        elif direction == "revert":
            os.chdir("..")
            shutil.rmtree(self.container_name)
            print("Deleted container folder.")

    def initialize_git(self, direction):
        if direction == "execute":
            try:
                command = ["git", "init"]
                output_bytestring = subprocess.check_output(command)
                output= output_bytestring.decode("utf-8")
                print(output.strip())
            except (FileNotFoundError, OSError) as e:
                print("Could not initialize a git repo. Is git installed?")
                raise(e)
        elif direction == "revert":
            pass

    def create_django_project_from_template(self, direction):
        if direction == "execute":
            try:
                command = ["django-admin", "startproject",
                    "--template={0}".format(self.args.template),
                    "--name=Procfile", self.args.django_project_name]
                output_bytestring = subprocess.check_output(command)
                print("Created Django project from specified template.")
            except (FileNotFoundError, OSError) as e:
                print("Could not create Django project. Is Django installed and"
                      " accessible?")
                raise(e)
        elif direction == "revert":
            pass

    def create_requirements_file_and_procfile(self, direction):
        if direction == "execute":
            with open("requirements.txt", "w") as requirements_file:
                requirements_file.write(self.requirements_text)
            with open("Procfile", "w") as procfile:
                procfile.write("web: sh -c 'cd {0} && gunicorn"
                    " {0}.wsgi.wsgi_heroku --log-file -'".format(
                        self.args.django_project_name)
                    )
            print("Created requirements file and Procfile.")
        elif direction == "revert":
            pass

    def create_runtime_file(self, direction):
        if direction == "execute":
            if self.args.python == "3":
                with open("runtime.txt", "w") as runtime_file:
                    runtime_file.write("python-3.6.0")
            elif self.args.python == "2":
                with open("runtime.txt", "w") as runtime_file:
                    runtime_file.write("python-2.7.13")
            else:
                raise ValueError("Python version can be 2 or 3.")
        if direction == "revert":
            pass

    def app_exists(self, app_name):
        try:
            app_info_bytestring = subprocess.check_output(["heroku", "apps"])
            app_info = app_info_bytestring.decode("utf-8").split("\n")
            for line in app_info:
                items = line.split()
                if len(items) > 0 and items[0] == app_name:
                    return True
            return False
        except FileNotFoundError as e:
            print("Could not find the Heroku CLI. Is it installed?")
            raise(e)

    def get_app_name(self, line_with_url):
        items = line_with_url.split()
        for item in items:
            match = re.match(re.compile("http(s?)://(.+)\.herokuapp.com(/?)$"),
                item)
            if match is not None:
                return match.group(2)

    def create_app(self, command):
        try:
            line_with_url_bytestring = subprocess.check_output(command)
            line_with_url= line_with_url_bytestring.decode("utf-8")
            print(line_with_url.strip())
            return self.get_app_name(line_with_url)
        except subprocess.CalledProcessError as e:
            print("Could not create the Heroku app. Is your quota full"
                " or the name taken?")
            raise(e)

    def create_heroku_app(self, direction):
        if direction == "execute":
            command = ["heroku", "create"]
            self.app_name = self.args.app
            self.delete_app_on_error = True
            if self.app_name is None:
                self.app_name = self.create_app(command)
            elif not self.app_exists(self.app_name):
                command += [self.app_name]
                if self.args.region is not None:
                    command += ["--region", self.args.region]
                self.app_name = self.create_app(command)
            else:
                print("Heroku app with that name exists. Skipping creation.")
                command = ["heroku", "git:remote", "-a", self.app_name]
                output_bytestring = subprocess.check_output(command)
                self.delete_app_on_error = False

        elif direction == "revert":
            if self.delete_app_on_error:
                command = ["heroku", "apps:destroy", "--app", self.app_name,
                           "--confirm", self.app_name]
                output_bytestring = subprocess.check_output(command)

    def add_django_settings_module_config_var(self, direction):
        if direction == "execute":
            output_bytestring = subprocess.check_output(
                ["heroku", "config:set", "DJANGO_SETTINGS_MODULE"
                 "={0}.settings.settings_heroku".format(
                    self.args.django_project_name)]
                )
            print(output_bytestring.decode("utf-8").strip())

        elif direction == "revert":
            command = ["heroku", "config:unset", "DJANGO_SETTINGS_MODULE"]
            output_bytestring = subprocess.check_output(command)



    def add_secret_key_config_var(self, direction):
        if direction == "execute":
            secret_key = "".join([random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
                for i in range(50)])
            output_bytestring = subprocess.check_output(["heroku",
                "config:set", "DJANGO_SECRET_KEY={0}".format(secret_key)])
            print(output_bytestring.decode("utf-8").strip())
        elif direction == "revert":
            command = ["heroku", "config:unset", "DJANGO_SECRET_KEY"]
            output_bytestring = subprocess.check_output(command)

    def database_exists(self):
        command = ["heroku", "config:get", "DATABASE_URL"]
        output_bytestring = subprocess.check_output(command)
        output = output_bytestring.decode("utf-8")
        if output.strip() != "":
            return True
        return False

    def create_database(self, direction):
        if self.args.database:
            if direction == "execute":
                if self.database_exists():
                    raise ValueError("You cannot use the --database flag"
                        " if a database already exists")
                command = ["heroku", "addons:create",
                           "heroku-postgresql:{0}".format(
                                self.args.database_type)]
                output_bytestring = subprocess.check_output(command)
                output= output_bytestring.decode("utf-8")
                print(output.strip())

            elif direction == "revert":
                command = ["heroku", "addons:destroy", "DATABASE",
                           "--confirm", self.app_name]
                output_bytestring = subprocess.check_output(command)


    def add_allowed_hosts_settings_var(self, direction):
        if direction == "execute":
            with open("./{0}/{0}/settings/settings_heroku.py".format(
                self.args.django_project_name), "r") as heroku_settings_file:
                lines = heroku_settings_file.readlines()
            with open("./{0}/{0}/settings/settings_heroku.py".format(
                self.args.django_project_name), "a") as heroku_settings_file:
                newline = "ALLOWED_HOSTS = ['{0}.herokuapp.com']\n".format(
                    self.app_name)
                if not lines[-1].endswith("\n"):
                    newline = "\n" + newline
                heroku_settings_file.write(newline)
            print("Added alllowed host to settings file.")
        elif direction == "revert":
            pass

    def commit_changes_to_git_and_push(self, direction):
        if direction == "execute":
            try:
                command1 = ["git", "add", "."]
                command2 = ["git", "commit", "-m", "First commit"]
                command3 = ["git", "push", "heroku", "master"]
                output1_bytestring = subprocess.check_output(command1)
                output2_bytestring = subprocess.check_output(command2)
                output3_bytestring = subprocess.check_output(command3)
                print("Commited changes to git and pushed to Heroku.")
            except subprocess.CalledProcessError as e:
                print("Could not commit changes and push to Heroku."
                      " Did some data already exist in the app?")
                raise(e)
        elif direction == "revert":
            pass

    def scale_app(self, direction):
        if direction == "execute":
            command = ["heroku", "ps:scale", "web={0}".format(
                self.args.scale)]
            output_bytestring = subprocess.check_output(command)
            print("\nYour app is now live on Heroku!.".format(
                self.app_name))
            os.chdir("..")
        elif direction == "revert":
            pass


    def deploy(self):
        self.pipeline = [self.create_root_directory,
                         self.initialize_git,
                         self.create_django_project_from_template,
                         self.create_requirements_file_and_procfile,
                         self.create_runtime_file,
                         self.create_heroku_app,
                         self.add_django_settings_module_config_var,
                         self.add_secret_key_config_var,
                         self.create_database,
                         self.add_allowed_hosts_settings_var,
                         self.commit_changes_to_git_and_push,
                         self.scale_app]
        for step in range(len(self.pipeline)):
            try:
                self.pipeline[step]("execute")
            except Exception as e:
                print("\n!!!\n")
                print("An error occured.")
                print("The full traceback will appear after cleanup.")
                self.current_step = step
                self.cleanup()
                raise(e)

    def cleanup(self):
        for step in range(self.current_step - 1, -1 , -1):
            self.pipeline[step]("revert")

def deploy(args):

    dh = DjangoHero(args)
    dh.deploy()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

deploy_parser = subparsers.add_parser("deploy")

deploy_parser.add_argument("--app", default = None)
deploy_parser.add_argument("--region", default = None)
deploy_parser.add_argument("--template",
    default = "https://github.com/gutfeeling/djangohero_default_template/"
    "archive/master.zip")
deploy_parser.add_argument("--database", action = "store_true")
deploy_parser.add_argument("--database_type", default = "hobby-dev")
deploy_parser.add_argument("--python", default = "3")
deploy_parser.add_argument("--container_name", default = None)
deploy_parser.add_argument("--scale", default = "1")
deploy_parser.add_argument("django_project_name")

deploy_parser.set_defaults(func = deploy)

def main():
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
