#!/usr/local/bin/python3

from os import getcwd, mkdir, chdir, remove
from os.path import dirname
from shutil import rmtree, copytree
from subprocess import call
from tempfile import mkdtemp

import click

from callbacks import *


@click.command()
@click.argument("py_file",
                callback=check_py_file)
@click.option("-i", "--icon_file",
              default='',
              callback=check_icon_file,
              help="icon to give the app")
@click.option("-d", "--destination_directory",
              default="bin",
              callback=check_destination_directory,
              help="directory to create the app in")
def main(py_file, icon_file, destination_directory):

	owd = getcwd()  # save copy of original working directory to create absolute path in case of runtime error
	temporary_directory = mkdtemp()

	try:
		# -------------------------------------------- setup app variables ---------------------------------------------
		py_file = Path(py_file)
		py_file_parent_directory = Path(dirname(py_file.absolute()))
		app_name = f"{py_file.stem}.app"
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
		
		# --------------------- create app by isolating PyInstaller output in temporary directory ----------------------
		copytree(py_file_parent_directory.absolute(), f"{temporary_directory}/{py_file_parent_directory.name}")
		chdir(temporary_directory)

		call(
			["pyinstaller", f"{py_file_parent_directory.name}/{py_file.name}", "-i", icon_file, "--windowed", 
			"--hidden-import", "pkg_resources.py2_warn"]
		)

		if not icon_file:
			'''delete default icon created by PyInstaller so app icon defaults to system default'''
			remove(f"dist/{app_name}/Contents/Resources/icon-windowed.icns")	
																			
		chdir(owd)

		# ------------------------------------- extract app to target destination --------------------------------------
		copytree(f"{temporary_directory}/dist/{app_name}", app_target_path)

		# ------------------------------------------------- cleanup ----------------------------------------------------
		rmtree(temporary_directory)

		# --------------------------------------------- show app in finder ---------------------------------------------
		call(["open", "-R", app_target_path])

	except Exception as error:	# TODO: specify Exception

		# ---------------------------------------- cleanup on error before exit ----------------------------------------
		bin_directory = f"{owd}/bin"
		if exists(bin_directory):
			rmtree(bin_directory)

		if exists(temporary_directory):
			rmtree(temporary_directory)

		raise Exception(repr(error))


if __name__ == "__main__":
	main()
