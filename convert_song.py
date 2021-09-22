import moviepy.editor as mpy
import random, time, os, argparse
import moviepy.video.compositing.transitions as transfx
import imageResize as ir

parser = argparse.ArgumentParser( description='Generate Video from batch of images and mp3 files' ,)
parser.add_argument( '-t', '--time', type=int, metavar='', default=5, help='Number of Seconds [default : 5 seconds]' )
parser.add_argument( '-d', '--directory', type=str ,metavar='', help='Directory of images', required=True )
parser.add_argument( '-i', '--imageSequence', type=int,metavar='', default=2, choices= {1,2} , help='Sequence of Images [1: Alphabatically 2: Random Default: Random]' )
parser.add_argument('-e', '--effect', type=int, metavar='', default=0, choices={0,1,11,12,2,21,22,23,24}, help='''\
                                                                    Effects between image transitions
                                                                        [0: No Effects,
                                                                        11: FadeIn Only,
                                                                        12:FadeOut Only,
                                                                        2: Slide Left, Right, Up, Down Random Combination,
                                                                        21: Slide from Left Only,
                                                                        22: Slide from Right Only,
                                                                        23: Slide from Top Only,
                                                                        24: Slide from Bottom Only,
                                                                        Default Value: 0
                                                                                             ]''')
parser.add_argument('mp3File', help='Mp3 file / path')
args = parser.parse_args()

#This function calcualtes the duration of mp3 file
def calculateDurationOfMp3File(  ):
    audioClip = mpy.AudioFileClip( args.mp3File )
    return int( audioClip.duration ) + 1   


#Read Image from directory and sorts them alphabeticaly or randomly depending upon input
#Calculates how many images will be required for duration (Totalduration / time) and generates a list of that many images
def generateImageSequenceForSlideshow(  ):
    listOfImages = os.listdir( args.directory )
    if args.imageSequence == 1:
       listOfImages = sorted( listOfImages ) #Sorting Alphabetically
    else:
        random.shuffle( listOfImages )
    numberOfImagesInAVideo = int( DURATION / args.time ) + 1
    if numberOfImagesInAVideo > len( listOfImages ):
        #repeat Images until number of images required for duration is met
        img = 0
        while numberOfImagesInAVideo > len( listOfImages ):
            listOfImages.append( listOfImages[img % len( listOfImages )] )
            img += 1
        return listOfImages
    else :
        #trim the listOfImages to fit duration
        listOfImages = listOfImages[:numberOfImagesInAVideo]
        return listOfImages
    

#Generates a video from given list of Images and mp3 file.
def generateVideoFileFromImageSequence( listOfImages ):
    imageClipList = []
    remainderTime = DURATION
    for image in listOfImages:
        if remainderTime <= args.time:
            imageClipList.append( mpy.ImageClip( args.directory + '/' + image ).set_duration( remainderTime ) )  
        else:
            imageClipList.append( mpy.ImageClip( args.directory + '/' + image ).set_duration( args.time ) )
        remainderTime -= args.time
    if args.effect in [2,21,22,23,24]:
        slideClips = applySlideEffectsToClips(imageClipList)
    elif args.effect == 11:
        slideClips = [clip.fadein(1) for x,clip in enumerate(imageClipList)]
    elif args.effect == 12:
        slideClips = [clip.fadeout(1) for x,clip in enumerate(imageClipList)]
    else: 
        slideClips = imageClipList
    audioClip = mpy.AudioFileClip( args.mp3File )
    final_audio = mpy.CompositeAudioClip( [audioClip] )
    final = mpy.concatenate_videoclips( slideClips, method="chain" ).set_duration( DURATION )
    final_video = mpy.CompositeVideoClip( [final], size=VIDEO_SIZE ).set_audio( final_audio ).set_duration( audioClip.duration )
    fileName = 'Output_{}.mp4'.format(time.strftime("%Y%m%d-%H%M%S"))
    final_video.write_videofile( fileName, fps=FPS)


def applySlideEffectsToClips(imageClipList):
    i = 0
    slideClips = []
    effects = ['left', 'right', 'top', 'bottom']  #moves in inverted direction of name
    temp = []
    while i < len(imageClipList):
        if args.effect == 2:
            random.shuffle(effects)
            ef = effects[0]
        elif args.effect == 21:
            ef = 'left'
        elif args.effect == 22:
            ef = 'right'
        elif args.effect == 23:
            ef = 'top'
        elif args.effect == 24:
            ef = 'bottom'
        for x,clip in enumerate(imageClipList):
            if x==i-1:
                temp.append(clip.fx(transfx.slide_out, duration=0.5, side=ef))
            if x==i:
                temp.append(clip.fx(transfx.slide_in, duration=0.5, side=ef))
        sc = mpy.CompositeVideoClip(temp[-2:], size=VIDEO_SIZE).set_duration(args.time)
        slideClips.append(sc)
        i+=1
    return slideClips


def deleteGeneratedImages(imgList):
    for img in imgList:
        os.remove(args.directory + '/' + img)

VIDEO_SIZE = ( 1280, 720 ) #Defined Video Resoultion
DURATION = calculateDurationOfMp3File() #Calculating duration of vide from duration of mp3 file
FPS = 24 #Since video is a slideshow , lower frame rate will result in faster video processing time and smaller size

if __name__ == '__main__':
    listOfImages = generateImageSequenceForSlideshow()
    listOfFullImages = []
    for img in listOfImages:
        listOfFullImages.append(ir.reSizeImage(args.directory + img, VIDEO_SIZE))
    generateVideoFileFromImageSequence( listOfFullImages )
    deleteGeneratedImages(listOfFullImages)
