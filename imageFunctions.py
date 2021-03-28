def convertToPNG(data): #converts to png if a jpg
    newFile = data.projectDirectory + "/convertedToPNG.png"
    userImage = Image.open(data.imagePath)
    userImage.save(newFile) 
    
    return newFile
    
    
def checkSquare(data):
    myImage = Image.open(data.imagePath)
    w, h = myImage.size
    
    return w == h
   
def resizeImage(data, imagePath, frameName, height):
    #resizing image; primarily for filter previews
    baseHeight = height
    userImage = Image.open(imagePath)
    
    hpercent = (baseHeight / float(userImage.size[1]))
    wsize = int((float(userImage.size[0]) * float(hpercent)))
    userImage = userImage.resize((wsize, baseHeight), Image.ANTIALIAS)

    userImage.save(frameName) 
    
    data.previewWidth = wsize
    data.previewHorizontalMargin = (data.width - 2*(data.margins +\
    data.previewWidth))/3
    while not os.path.exists(frameName):
        data.resizingDone = False
        
    data.resizingDone = True
    
def getFileName():
    fileName = tkinter.filedialog.askopenfilename()
    return fileName
    
def getDirectoryName():
    path = tkinter.filedialog.askdirectory()
    return path