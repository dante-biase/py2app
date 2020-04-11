![Image description](https://i.ibb.co/3BZjX6m/banner.png)


# py2app

**py2app** is a hassle-free, command-line-tool that allows you to easily convert Python files/projects into Mac OS Applications with a single line of code.

![](https://i.ibb.co/Jjvv03Q/demo.gif)


>py2app **is** a streamlined version of and built from: [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/).

>py2app **is not** to be confused with this [py2app](https://bitbucket.org/ronaldoussoren/py2app/src/default/). 

## py2app vs PyInstaller?
- **minimal** command-line-interface
- **easier** resource integration
- **cleaner** output and file handling
- **constrained** functionality 

## Compatibility
- Mac OSX
- Python >= 3.6

## Dependencies
- [PyInstaller](https://github.com/pyinstaller/pyinstaller)
- [Click](https://github.com/pallets/click)
- [py2x](https://github.com/dante-biase/py2x)

## Installation and Usage

|          	| Installation                                                                                                                          	| Usage                           	|
|----------	|---------------------------------------------------------------------------------------------------------------------------------------	|---------------------------------	|
| **Homebrew** 	| $ brew install dante-biase/x2x/py2app                                                                                          	| $ py2app PY_FILE [OPTIONS]      	|
| **Manual**   	| $ git clone https://github.com/dante-biase/py2app.git<br>$ cd py2app<br>$ pip3 install -r requirements.txt<br>$ chmod +x py2app.py 	| $ ./py2app.py PY_FILE [OPTIONS] 	|


### PY_FILE
> specifies the py file to be converted into an application, required

### [OPTIONS]
```
  -r, --resources_directory     TEXT    directory that contains app resources
  -i, --icon_file               TEXT    icon to give the app
  -d, --destination_directory   TEXT    directory to create the app in
  --help                                print this message and exit
```
## Notes

### Resources
1. If your app requires any resources, you must consolidate these files into a single directory - `resources_directory`
2. Install [py2x](https://github.com/dante-biase/py2x)

       $ pip3 install py2x
3. Add this import statement to any script that references resources you might need:
      
       from py2x import Resources
4. Update references:

   **EXAMPLE:** suppose you need to read a text file located within your `resources_directory`:
          
   change:
   
       text_file = open("path/to/resources/file.txt", "r")

   to:
   
       text_file = open(Resources.get("file.txt"), "r")`

5. Execute py2app while making sure to pass the path to your `resources_directory` to the `-r` flag:
   
       py2app main.py -r path/to/resources [OTHER OPTIONS]

### Output
1. The output app will be named with the stem of `PY_FILE`
2. If `destination_directory` is not specified, the app will be placed in the same directory as `PY_FILE`
