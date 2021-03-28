def doOutlines(imagePath, frameName):
    img = cv2.imread(imagePath, 1)
    
    kernel = np.array(([-1, -1, -1],[-1,8,-1],[-1,-1,-1]), np.float32)
    image = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(frameName, image)
    
    
def doBlur(imagePath, frameName):
    img = cv2.imread(imagePath, 1)
    
    kernel = np.array(np.ones((15,15), np.float32))/225
    image = cv2.filter2D(img, -1, kernel)
    
    cv2.imwrite(frameName, image)
    

#https://gist.github.com/evan3334/a84ac035d2186ae7e058#file-glitch-py
#modified so that it would glitch according to the intensity of beats, save image to a directory
def doGlitch(imagePath, frameName):
    glitchfactor_x = .3
    glitchlen_x = .1
    glitchchance = .8
    
    def getlist(mat):
        rows = len(mat)
        cols = len(mat[0])
        list = [0 for x in range(0,rows*cols)]
        for y in range(0,rows):
            for x in range(0,cols):
                list[(y*cols)+x] = mat[y][x]
        return list
    
    def getimagematrix(image):
        ibbox = image.getbbox()
        iw = bbox[2]
        ih = bbox[3]
        ls = list(image.getdata())
        im_matrix = [0 for x in range(0,ih)]
        for i in range(0,ih):
            row = [0 for x in range(0,iw)]
            for j in range(0,iw):
                row[j] = ls[(i*iw)+j]
            im_matrix[i] = row
        return im_matrix

    im = Image.open(imagePath)
    format = im.format

        
    bbox = im.getbbox()
    w = bbox[2]
    h = bbox[3]
        
    maxglitch_x = int(w*glitchfactor_x)
    maxglitchlen_x = int(h*glitchlen_x)
        
    matrix = getimagematrix(im)
    newmatrix = getimagematrix(im)
        
    glitching = False
    glitchlen = 0
    glitchamount = 0
    glitchpos = 0
        
    for i in range(0,h):
        
        if glitching==True:
            row = matrix[i]
            newrow = [0 for x in range(0,w)]
            for x in range(0,w):
                ofsx = x+glitchamount
                if ofsx >= w:
                    ofsx = ofsx-w
                newrow[x] = row[ofsx]
            newmatrix[i] = newrow
            if glitchpos == (glitchlen-1):
                glitching = False
            else:
                glitchpos = glitchpos+1
        else:
            willglitch = random.randint(0,int(((1-glitchchance)*100)))
            if willglitch == 0:
                glitching = True
                glitchlen = random.randint(1,maxglitchlen_x)
                glitchamount = random.randint(1,maxglitch_x)
                glitchpos = 0
            else:
                glitching = False
        
    im.putdata(getlist(newmatrix))
        
    im.save(frameName)
    
def doParty(imagePath, frameName, count, rT, gT, bT, r, g, b):
    
    if count%5 == 0:
        filteredFrame = Image.merge('RGB', (rT, g, b))
    elif count%5 == 1:
        filteredFrame = Image.merge('RGB', (r, g, bT))
    elif count%5 == 2:
        filteredFrame = Image.merge('RGB', (r, gT, b))
    elif count%5 == 3:
        filteredFrame = Image.merge('RGB', (rT, g, bT))
    elif count%5 == 4:
        filteredFrame = Image.merge('RGB', (r, gT, b))
        
    filteredFrame.save(frameName)

   
def splitToRGB(imagePath):
    basewidth = 612
    
    userImage = Image.open(imagePath)
    wpercent = (basewidth / float(userImage.size[0]))
    hsize = int((float(userImage.size[1]) * float(wpercent)))
    userImage = userImage.resize((basewidth, hsize), Image.ANTIALIAS)

    r, g, b, = userImage.split()
    
    return (r, g, b)
    
def saveUnfilPartyFrame(data, imagePath, frameName):
    basewidth = 612
    
    userImage = Image.open(imagePath)
    wpercent = (basewidth / float(userImage.size[0]))
    hsize = int((float(userImage.size[1]) * float(wpercent)))
    userImage = userImage.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
           
    userImage.save(frameName)