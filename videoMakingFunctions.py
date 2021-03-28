def createVideo(data):
    
    #analyze the music and get video length
    vidDuration = int(getSongLength(data.songToUse))

    #get number of frames needed
    numFrames = vidDuration * 20
    
    
    print("Now saving frames")
    createFilteredFrames(data, data.imagePath, data.beats, numFrames, data.filter, data.projectDirectory)
    
    print("Now creating video")
    
    #concatenates frame
    noMusicVideo = data.projectDirectory + "/noAudio.mp4"
    imagesToVideo(data, data.projectDirectory, noMusicVideo)
    
    #adds music to the audio-less video
    finalVideoPath = data.projectDirectory + "/" + data.projectName + ".mp4"
    addAudioToVideo(data, noMusicVideo, data.songToUse, finalVideoPath)
    
    #delete all except final video
    deleteFilesAfterVideo(data, finalVideoPath)
    
    data.loading = False
    data.makingVideo = False
    data.finished = True
    
    print("Done making video!")
    print("Check %s for the folder that contains the video"%(data.projectDirectory))
    

def createFilteredFrames(data, image, beats, numFrames, filter, projectDir):
    #offset included to synchronize with music better
    audioOffset = 5
    offsetCount = 0
    count = 0
    if filter == "outlines":
        unfilteredFrame = cv2.imread(image, 1)
        for i in range(numFrames):
            frameName = projectDir + "/frame" + str(i) + ".png"
            if offsetCount != audioOffset:
                offsetCount += 1
            elif len(beats) == 0:
                cv2.imwrite(frameName, unfilteredFrame)
            elif abs(int(beats[0] * 20) - i) < 3:
                count += 1
                doBlur(image, frameName)
                if count == 5:
                    count = 0
                    beats.pop(0)
            else:
                cv2.imwrite(frameName, unfilteredFrame)                
        
    elif filter == "blur":
        unfilteredFrame = cv2.imread(image, 1)
        for i in range(numFrames):
            frameName = projectDir + "/frame" + str(i) + ".png"
            if offsetCount != audioOffset:
                offsetCount += 1
            elif len(beats) == 0:
                cv2.imwrite(frameName, unfilteredFrame)
            elif abs(int(beats[0] * 20) - i) < 3:
                count += 1
                doBlur(image, frameName)
                if count == 5:
                    count = 0
                    beats.pop(0)
                
            else:
                cv2.imwrite(frameName, unfilteredFrame)
            
    elif filter == "glitch":
        unfilteredFrame = cv2.imread(image, 1)
        for i in range(numFrames):
            frameName = projectDir + "/frame" + str(i) + ".png"
            if offsetCount != audioOffset:
                offsetCount += 1
            elif len(beats) == 0:
                cv2.imwrite(frameName, unfilteredFrame)
            elif abs(int(beats[0] * 20) - i) < 3:
                count += 1
                doGlitch(image, frameName)
                if count == 5:
                    count = 0
                    beats.pop(0)
                
            else:
                cv2.imwrite(frameName, unfilteredFrame)
                
    elif filter == "party":
        #split filter image and my image and merge r, g, b randomly
        r, g, b = splitToRGB(image)
        filter = Image.open(data.partyFilterPath)
        rT, gT, bT, = filter.split()
        for i in range(numFrames):
            frameName = projectDir + "/frame" + str(i) + ".png"
            if offsetCount != audioOffset:
                offsetCount += 1
            elif len(beats) == 0:
                saveUnfilPartyFrame(data, image, frameName)
            elif abs(int(beats[0] * 20 - i)) < 3:
                count += 1
                doParty(image, frameName, count, rT, gT, bT, r, g, b)
                if count == 5:
                    count = 0
                    beats.pop(0)
                
            else:
                saveUnfilPartyFrame(data, image, frameName)
                
    return None
 

#from http://tsaith.github.io/combine-images-into-a-video-with-python-3-and-opencv-3.html
#modified so that it would create a video and save it to a directory        
def imagesToVideo(data, projectDir, projectName):

    ap = argparse.ArgumentParser()
    ap.add_argument("-ext", "--extension", required=False, default='png', help="extension name. default is 'png'.")
    ap.add_argument("-o", "--output", required=False, default=projectName+'.mp4', help="output video file")
    args = vars(ap.parse_args())
    
    # Arguments
    dir_path = projectDir
    ext = args['extension']
    output = args['output']
    
    images = []
    for f in os.listdir(dir_path):
        if f.endswith(ext):
            images.append(f)
                        
            
    # Determine the width and height from the first image
    image_path = os.path.join(dir_path, images[0])
    frame = cv2.imread(image_path)
    # cv2.imshow('video',frame)
    height, width, channels = frame.shape
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    output = projectName
    out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))
    
    for image in images:
    
        image_path = os.path.join(dir_path, image)
        frame = cv2.imread(image_path)
    
        out.write(frame)
    
    print("concatenating frames done")

def addAudioToVideo(data, video, audio, savePath):
    
    cmd = data.ffmpegPath + " -i %s -i %s -shortest %s"%(video, audio, savePath)

    subprocess.call(cmd, shell=True)       
    
    print("mixing audio and video done")