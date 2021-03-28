def cutMusic(data): #cuts music, puts into project directory

    sound = AudioSegment.from_mp3(data.musicPath)
    length = getSongLength(data.musicPath)
    start = len(sound) // length * data.cutStart
    end = len(sound) // length * data.cutEnd
    snippet = sound[start:end+50]
    snippet.export(data.songToUse, format="wav")
    
    return None


def convertMP3ToWAV(data): #converts to wav if an mp3 was inputted
    
    convertSong = data.songName[:-3] 
    mp3Path = data.musicPath
    data.musicPath = data.projectDirectory + "/" + convertSong + "wav"
    subprocess.call([data.ffmpegPath, '-i', mp3Path ,data.musicPath])
    
    return data.musicPath
    
    
def getSongLength(path):
    f = sf.SoundFile(path)
    length = format(len(f) / f.samplerate)
    
    seconds = float(length)
    seconds = int(seconds)
    
    return seconds
    
#from https://github.com/aubio/aubio/blob/master/python/demos/demo_bpm_extract.py
#modified so that it would return a list of beats
def analyzeMusic(path, params=None): #getting a list of beats for the filter
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            print("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    allBeats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            allBeats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break
    
    def beats_to_bpm(allBeats, path):
        # if enough beats are found, convert to periods then to bpm
        bpms = 60./diff(allBeats)
        return median(bpms)

    bpm = beats_to_bpm(allBeats, path)
    beatCount = bpm//30
    beats = []
    
    for i in range(len(allBeats)):
        if i % beatCount <= 1:
            beats.append(allBeats[i])
            
    print(beats)
            
    return beats

#from https://gist.github.com/THeK3nger/3624478
class WavePlayerLoop(threading.Thread): #creating a player to play while the function is still running

  CHUNK = 1024

  def __init__(self,filepath,loop=True) :

    super(WavePlayerLoop, self).__init__()
    self.filepath = os.path.abspath(filepath)
    self.loop = loop

  def run(self):
    # Open Wave File and start play!
    wf = wave.open(self.filepath, 'rb')
    player = pyaudio.PyAudio()

    # Open Output Stream (basen on PyAudio tutorial)
    stream = player.open(format = player.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)

    # PLAYBACK LOOP
    data = wf.readframes(self.CHUNK)
    while self.loop :
      stream.write(data)
      data = wf.readframes(self.CHUNK)
      if data == '' : # If file is over then rewind.
        wf.rewind()
        data = wf.readframes(self.CHUNK)

    stream.close()
    player.terminate()


  def play(self):
    self.start()

  def stop(self):
    self.loop = False

def playMusicForManualBeats(data): #playing the music
    data.musicStart = True
    data.musicStartTime = time.time()
    bgmPlayer = WavePlayerLoop(data.songToUse)
    bgmPlayer.play()
    print("this plays")
    
def addManualBeats(data): #adding beats
    beatTime = time.time() - data.musicStartTime
    data.beats.append(beatTime)