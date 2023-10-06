import os, time, random
from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']
from psychopy import visual, sound, event, core


#task : 1 run = 1 playlist = around 10 audio tracks
#repeat for n songs in subXX_runXX.csv :
#   step 1: DEFAULT_INSTRUCTION
#   step 2: display audio
#   step 3: Auditory imagery assessment
#   step 4: Familiarity assessment

#Global Variables if multiples tasks
INSTRUCTION_DURATION = 3
DEFAULT_INSTRUCTION = """Listen to the following track"""
AUDITORY_IMAGERY_ASSESSMENT = ["""During the silences, did you imagine the missing part of the different audio tracks you’ve heard ?"""]
FAMILIARITY_ASSESSMENT = ["""Did you recognise the song ?"""]
imagery_quest = [(k, q, 5) for k, q in enumerate(AUDITORY_IMAGERY_ASSESSMENT)]
familiarity_quest = [(k, q, 5) for k, q in enumerate(FAMILIARITY_ASSESSMENT)]


class Track(object):
#Derived from SoundTaskBase (Narratives task)

    def __init__(self, sound_file, exp_win, initial_wait=4, final_wait=2, num=None):
        #super().__init__(**kwargs)
        #--------probably in kwargs--------------
        self.instruction = DEFAULT_INSTRUCTION
        self.exp_win = exp_win
        #----------------------------------------
        self.initial_wait, self.final_wait = initial_wait, final_wait
        self.num = num
        if os.path.exists(sound_file):
            self.sound_file = sound_file
        else:
            raise ValueError("File %s does not exists" % sound_file)   
    
    def _instructions(self): #, exp_win, ctl_win):
        screen_text = visual.TextStim(
            self.exp_win,
            text=self.instruction,
            alignText="center",
            color="white",
            units='height',
            height=0.05
        )
        screen_text.draw(self.exp_win)

    def _setup(self): #, exp_win):
        self.sound = sound.Sound(self.sound_file)
        self.duration = self.sound.duration
    
    def _play_track(self):
        screen_text = visual.TextStim(
            self.exp_win,
            text=f'track {self.num}',
            alignText="center",
            color="white",
            units='height',
            height=0.05
        )
        screen_text.draw(self.exp_win)
        self.sound.play()

    def run(self): 
        self._instructions()
        self.exp_win.flip()
        time.sleep(INSTRUCTION_DURATION)
        self._setup()
        self._play_track()
        self.exp_win.flip()
        time.sleep(self.sound.duration + self.final_wait)
        while self.sound.status > 0:
            pass
        