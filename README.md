# mc_downloader
Downloads Photos and Videos from Swisscom myCloud

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

If you get error messages, you may need to to install extra libraries such as requests. 

```
pip install requests
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

To start the application with your bearer you can run it with these parameters
```
python mc_image_downloader.py --auth 'Bearer lAM6wZROSBWNqJRlyoZmexD=='
```

If you want to access a myCloud account on a test or development enviroment you can use an additional argument
```
python mc_image_downloader.py --auth 'Bearer lAM6wZROSBWNqJRlyoZmexD==' --env dev
```

# TODO

- handle file collisions with files with same name in the same month
- change creation date to reflect original date of asset
- Package application to allow it to start without python installed
