#!/usr/local/bin/python3

from os import getcwd, mkdir, chdir, remove
from os.path import dirname, exists
from shutil import rmtree, copytree
from subprocess import call, check_output, STDOUT, CalledProcessError
from tempfile import mkdtemp

import click

from callbacks import *


@click.command()
@click.argument("py_file",
                callback=check_py_file)
@click.option("-r", "--resources_directory",
              default=None,
              callback=check_directory,
              help="directory that contains resources for binary")
@click.option("-i", "--icon_file",
              default='',
              callback=check_icon_file,
              help="icon to give the app")
@click.option("-d", "--destination_directory",
              default=None,
              callback=check_directory,
              help="directory to create the app in")
def main(py_file, resources_directory, icon_file, destination_directory):

	owd = getcwd()  # save copy of original working directory to create absolute path in case of runtime error
	temporary_directory = mkdtemp()	# create temporary directory

	try:
		# -------------------------------------------- setup app variables ---------------------------------------------
		py_file = Path(py_file)
		py_file_parent_directory = Path(dirname(py_file.absolute()))
		app_name = f"{py_file.stem}.app"

		if not destination_directory:
			app_target_path = f"{py_file_parent_directory.absolute()}/{app_name}"
		else:
			app_target_path = f"{destination_directory}/{app_name}"

		# ------------------------------------------- check app target path --------------------------------------------
		if exists(app_target_path):
			overwrite = ""
			while not (overwrite == 'y' or overwrite == 'n'):
				overwrite = str(input(f"{app_target_path} already exists. Replace? [y/n] "))

			if overwrite == 'y':
				rmtree(app_target_path)
			else:
				exit(0)
				
		# --------------------------- copy parent directory of script to temporary directory ---------------------------
		copytree(py_file_parent_directory.absolute(), f"{temporary_directory}/{py_file_parent_directory.name}")
		
		# ----------------------------------------- go to temporary directory ------------------------------------------
		chdir(temporary_directory)
		py_file_copy = f"{py_file_parent_directory.name}/{py_file.name}"

		# -------------------------------------------- execute pyinstaller ---------------------------------------------
		pyinstaller_call = ["pyinstaller", py_file_copy]
		pyinstaller_arguments = ["--windowed", "--hidden-import", "pkg_resources.py2_warn", "-i", icon_file]		
		
		if resources_directory:
			pyinstaller_arguments += ["--add-data", f"{resources_directory}:resources"]

		try:
			check_output(pyinstaller_call + pyinstaller_arguments, stderr=STDOUT)
		except CalledProcessError as error:
			print(error.output.decode("UTF8"))
			exit(1)

		if not icon_file:
			'''delete default icon created by PyInstaller so app icon defaults to system default'''
			remove(f"dist/{app_name}/Contents/Resources/icon-windowed.icns")	

		# ------------------------------------- extract app to target destination --------------------------------------
		copytree(f"dist/{app_name}", app_target_path)																

		# ------------------------------------------------- cleanup ----------------------------------------------------
		chdir(owd)
		rmtree(temporary_directory)

		# ------------------------------------------- show new app in finder -------------------------------------------
		call(["open", "-R", app_target_path])

	except Exception as error:	# TODO: specify Exception

		# ---------------------------------------- cleanup on error before exit ----------------------------------------
		if exists(temporary_directory):
			rmtree(temporary_directory)

		raise error


if __name__ == "__main__":
	main()
