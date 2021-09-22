# videoGenerator
Generate videos from batch of image and mp3 files. Auto resize / adds blurred backgrounds to images to match desired video resolution.
Supports slides, fade animations.


```
usage: vidGenerate.py [-h] [-t] -d  [-i] [-e] mp3File

Generate Video from batch of images and mp3 files

positional arguments:
  mp3File               Mp3 file / path

optional arguments:
  -h, --help            show this help message and exit
  -t , --time           Number of Seconds [default : 5 seconds]
  -d , --directory      Directory of images
  -i , --imageSequence 
                        Sequence of Images [1: Alphabatically 2: Random Default: Random]
  -e , --effect         Effects between image transitions [0: No Effects, 11: FadeIn Only, 12:FadeOut Only, 2: Slide
                        Left, Right, Up, Down Random Combination, 21: Slide from Left Only, 22: Slide from Right Only,
                        23: Slide from Top Only, 24: Slide from Bottom Only, Default Value: 0 ]
                        
```
