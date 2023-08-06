============
SPOTLIGHTPY
============
**************************************
A Windows X spotlight extraction tool.
**************************************
Introduction 
************
Now get a hold  on the beautiful lock screen wallpapers displayed under the spotlight project for windows 10.Use this tool to either store the cached images in a folder you specify, or get their PIL.Image.Image object to transform them the way you like.

Installation
******************
Install using 

 pip install spotlightpy

Usage
******************

Windows X operating system is must for executing this module.
All the methods reside in "spotlight" submodule of spotlightpy.Firstly, import spotlight 

   >>> from spotlightpy import spotlight

The spotlight module has two methods.

1. getimages : 

    getimages(None) --: List(PIL.Image.Image)

    this method returns a list of PIL.Image.Image objects of the cached images with each object                             representing a spotlight image of resolution 1920*1080.
   
   >>> spotlight.getimages()
   [<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1920x1080 at 0x34305F0>, <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1920x1080 at 0x3430F70>, <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1920x1080 at 0x1518030>, ...]
2. storeimages(destination_path = "C:\\spotlight")
    Store the spotlight images from your PC to the path specified by the argument.If no path is provided then a new folder at "C:\\spotlight" is constructed and images are stored there.If the given argument does not represent any existing folder then a new folder is created to stores images.If given string does not qualify as valid path for even a new folder or a file already exists with same absolute path, then "ValueError" will be raised.
   
   >>> spotlight.storeimages("C:\\MySpotlightImages") 



 