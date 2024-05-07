"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import os
import shutil

from invoke import task

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
ARCHIVE_NAME = "project_rebirth_launcher"
DEVELOP_APP_VERSION = "v99-99-99"
EXECUTABLE_NAME = "Project_Rebirth_Launcher"

VIRTUALENV_NAME = "py311_projectrebirth-gui"

OPEN_IN_NEW_TAB = 2

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
def _update_requirements_txt(c):
    c.run("pip freeze > requirements.txt")


def remove_temporary_folders():
    print("-> remove unused folders")
    for folder in ["dist", "build", "temp"]:
        if os.path.exists(folder):
            print("remove: {}".format(folder))
            shutil.rmtree(folder)
    print("finished!")

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       tasks
# ------------------------------------------------------- #


@task
def update_requirements(c):
    with c.prefix("workon {}".format(VIRTUALENV_NAME)):
        _update_requirements_txt(c)


@task
def create_exe(c, version="v9-9-9"):
    with c.prefix("workon {}".format(VIRTUALENV_NAME)):

        print("---------- START CREATING EXE ----------")
        remove_temporary_folders()

        print("-> start creating .exe")
        c.run("pyinstaller start_app.spec")
        print("finished!")

        print("-> start creating temporary folders and copy files")
        for folder in ["temp", "temp/graphics/"]:
            os.mkdir(folder)
        shutil.copyfile("graphics/app_icon.ico", "temp/graphics/app_icon.ico")
        shutil.copytree("dist/start_app", "temp/apps")

        print("finished!")
        print("-> start creating .zip")

        zip_name = ARCHIVE_NAME + "_" + version

        shutil.make_archive(zip_name, "zip", "temp")
        print("finished!")
        remove_temporary_folders()
        print("---------- FINISHED CREATING EXE ----------")

