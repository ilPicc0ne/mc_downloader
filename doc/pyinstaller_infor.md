# installer for windows

make sure pyinstaller is installed on windows (pip install pyinstaller)

execute to build the windows dist

```
pyinstaller mc_image_downloader.py -F --onefile --hidden-import requests
```


Mac:

$ rm -rf build dist
$ python setup.py py2app