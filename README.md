# mc_downloader
Downloads Photos and Videos from [Swisscom myCloud](https://mycloud.ch). 


## Overview
The appliation will download all your photos and videos to your computer. It will automatically create folders for year and month and put the photos and videos in the respective folders

This application is currently only availble in a tech preview in alpha version.

It can be used on all myCloud enviroments (prod, dev2, test).  Default is prod.

## prerequisits

You will need to have python installed on your computer. https://www.python.org/downloads/

On windows 10 its best to type *python* in command line and it will install it from windows store.
```
python
```

## Usage

In order to use this application. You will need to login into your myCloud account (www.mycloud.ch) on browser and extract the Authtentication token from the resuests. This can be done using the inspector on a browser like chrome and observing the requests.

the Authentication token looks something like this: 
```
Bearer lAM6wZROSBWNqJRlyoZmexX==
```

Start the application
```
python mc_image_downloader.py
```

The application will prompt you to enter the access token. 


## Command line arguments

```
usage: mc_image_downloader.py [-h] [--jpg] [--auth AUTH] [--env ENV] [-f]

optional arguments:
  -h, --help   show this help message and exit
  --jpg        Will download HEIC images as jpg
  --auth AUTH  myCloud Bearer token. example "Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==
  --env ENV    Enviroment: prod, dev2 or test
  -f           Adding this option will download all images without creating sub-folders (year/month)
```

## TODO - Current limmitations

- handle file collisions with files with same name in the same month
- change creation date to reflect original date of asset
- Package application to allow it to start without python installed
