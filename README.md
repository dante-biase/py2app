![Image description](https://i.ibb.co/3BZjX6m/banner.png)


# py2app

**py2app** is a hassle-free, command-line-tool that allows you to easily convert Python files/projects into Mac OS Applications with a single line of code.

>py2app **is** a streamlined version of and built from: [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/).

>py2app **is not** to be confused with this [py2app](https://bitbucket.org/ronaldoussoren/py2app/src/default/). 

## py2app vs PyInstaller?
- **minimal** command-line-interface
- **cleaner** output and file handling
- **constrained** functionality 

## Compatibility
- Mac OSX
- Python >= 3.6

## Dependencies
- [PyInstaller](https://github.com/pyinstaller/pyinstaller)
- [Click](https://github.com/pallets/click)

## Installation and Usage

|          	| Installation                                                                                                                          	| Usage                           	|
|----------	|---------------------------------------------------------------------------------------------------------------------------------------	|---------------------------------	|
| **Homebrew** 	| $ brew install dante-biase/x2appUtils/py2app                                                                                          	| $ py2app PY_FILE [OPTIONS]      	|
| **Manual**   	| $ git clone https://github.com/dante-biase/py2app.git<br>$ cd py2app<br>$ pip3 install -r requirements.txt<br>$ chmod +x py2app.py 	| $ ./py2app.py PY_FILE [OPTIONS] 	|


### PY_FILE
> specifies the py file to be converted into an application, required

### [OPTIONS]
```
  -i, --icon_file               TEXT    icon to give the app
  -d, --destination_directory   TEXT    directory to create the app in
  --help                                print this message and exit
```
### NOTES
1. the output app will be named with the stem of `PY_FILE`
2. if your app uses any **resources**:
    * move all resources into a new directory called "resources"
    * place "resources" into the same directory as `PY_FILE`
    * update any references to files within "resources" in `PY_FILE`
3. if `destination_directory` is not specified, the app will be placed in the same directory as `PY_FILE`
