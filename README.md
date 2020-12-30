# mc_downloader
Downloads Photos and Videos from Swisscom myCloud

The appliation will download all your photos and videos to your computer. It will automatically create folders for year and month and put the photos and videos in the respective folders

This application is currently only availble in a tech preview in alpha version.

It can be used on all myCloud enviroments (prod, dev2, test).  Default is prod.

**prerequisits**

You will need to have python installed on your computer. https://www.python.org/downloads/

**Useage**

In order to use this application. You will need to login into your myCloud account (www.mycloud.ch) on browser and extract the Authtentication token from the resuests. This can be done using the inspector on a browser like chrome and observing the requests.

the Authentication token looks something like this: 
```
'Bearer lAM6wZROSBWNqJRlyoZmexX=='
```

To start the application with your bearer you can run it with these parameters
```
python mc_image_downloader.py --auth 'Bearer lAM6wZROSBWNqJRlyoZmexD=='
```

If you want to access a myCloud account on a test or development enviroment you can use an additional argument
```
python mc_image_downloader.py --auth 'Bearer lAM6wZROSBWNqJRlyoZmexD==' --env dev
```
