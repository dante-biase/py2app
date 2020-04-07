#!/usr/local/bin/python3

from os import getcwd, mkdir, chdir, remove
from shutil import rmtree, copytree
from subprocess import call

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

	cwd = getcwd()  # save copy of current working directory to create absolute path in case of runtime error

	try:
		# -------------------------------------------- setup app variables ---------------------------------------------
		py_file = Path(py_file)
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
		mkdir("temp")
		chdir("temp")
		call(["pyinstaller", py_file.absolute(), "-i", icon_file, "--windowed"])
		if not icon_file:
			'''delete default icon created by PyInstaller so app icon defaults to system default'''
			remove(f"dist/{app_name}/Contents/Resources/icon-windowed.icns")	
																			
		chdir("..")

		# ------------------------------------- extract app to target destination --------------------------------------
		copytree(f"temp/dist/{app_name}", app_target_path)

		# ------------------------------------------------- cleanup ----------------------------------------------------
		rmtree("temp")

		# --------------------------------------------- show app in finder ---------------------------------------------
		call(["open", "-R", app_target_path])

	except Exception as error:	# TODO: specify Exception

		# ---------------------------------------- cleanup on error before exit ----------------------------------------
		bin_directory = f"{cwd}/bin"
		if exists(bin_directory):
			rmtree(bin_directory)

		temp_directory = f"{cwd}/temp"		
		if exists(temp_directory):
			rmtree(temp_directory)

		raise Exception(repr(error))


if __name__ == "__main__":
	main()
