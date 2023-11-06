import os, time, csv, pandas
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
AUDITORY_IMAGERY_ASSESSMENT = ("During the silences, did you imagine the missing part of the different audio tracks you’ve heard ?", ['never', 'a few times', 'half the time', 'most of the time', 'always'])
FAMILIARITY_ASSESSMENT = ("Did you recognise the song ?", ['no', 'maybe', 'yes'])


class Playlist_StandAlone(object):
    def __init__(self, csv_path, exp_win):
        self.exp_win = exp_win
        self._events = []
        
        file = open(csv_path, "r")
        self.playlist = list(csv.reader(file, delimiter=","))
        file.close()

    def _log_event(self, event):
        self._events.append(event)

    def save(self):
        if len(self._events):
            fname = './Results/test'
            df = pandas.DataFrame(self._events)
            df.to_csv(fname, sep="\t", index=False)

    def run(self):
        for i, track in enumerate(self.playlist):
            track_path = track[0]
            track_name = os.path.split(track_path)[1]
            Display_track = Track(self.exp_win, track_path)
            Display_track.run()
            imagery_form = Questionnaire(self.exp_win,self._events, 
                                         trial_type='IMAGERY', name=track_name, 
                                         question=AUDITORY_IMAGERY_ASSESSMENT[0], 
                                         answers=AUDITORY_IMAGERY_ASSESSMENT[1])
            imagery_form.run()    
            familiarity_form = Questionnaire(self.exp_win, self._events,
                                             trial_type='FAMILIARITY', name=track_name, 
                                             question=FAMILIARITY_ASSESSMENT[0], 
                                             answers=FAMILIARITY_ASSESSMENT[1])
            familiarity_form.run()
        self.save()

class Track(object):
#Derived from SoundTaskBase (Narratives task)

    def __init__(self, exp_win, sound_file, initial_wait=4, final_wait=2):
        #super().__init__(**kwargs)
        #--------probably in kwargs--------------
        self.instruction = DEFAULT_INSTRUCTION
        self.exp_win = exp_win
        #----------------------------------------
        self.initial_wait, self.final_wait = initial_wait, final_wait
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

class Questionnaire(object):
        
        def __init__(self, exp_win, events, trial_type=None, name = None, question = None, answers = None, y_spacing=80):
            self.exp_win = exp_win
            self._events = events
            self.ISI = core.StaticPeriod(win=self.exp_win)
            #event.getKeys('udlra') # flush keys
            self.trial_type = trial_type
            self.name = name
            self.question = question
            self.answers = answers
            self.n_pts = len(answers)
            self.legends = []
            self.response = 0

            self.exp_win.setColor([0] * 3, colorSpace='rgb')
            self.win_width = self.exp_win.size[0]
            self.y_spacing = y_spacing
            self.scales_block_x = self.win_width * 0.25
            self.scales_block_y = self.exp_win.size[1] * 0.1
            self.extent = self.win_width * 0.2
            self.x_spacing= (self.scales_block_x  + self.extent) * 2 / (self.n_pts - 1)

        def _legend(self, text, pos):
            self.legends.append(visual.TextStim(
                self.exp_win,
                text = text,
                units="pix",
                pos=(-(self.scales_block_x + self.extent) + pos * self.x_spacing, self.exp_win.size[1] * 0.1),
                wrapWidth= self.win_width * 0.12,
                height= self.y_spacing / 4.5,
                anchorHoriz="center",
                alignText="center",
                bold=True
           ))

        def _setup(self):
            default_response = self.n_pts // 2
            self.response = default_response
            y_pos = self.scales_block_y - self.y_spacing

            self.line = visual.Line(
                    self.exp_win,
                    (-(self.scales_block_x + self.extent), y_pos),
                    (self.scales_block_x + self.extent, y_pos),
                    units="pix",
                    lineWidth=6,
                    autoLog=False,
                    lineColor=(-1, -1, -1) #if q_n == 0 else (-1, -1, -1),
                )
            
            self.bullets = [
                    visual.Circle(
                        self.exp_win,
                        units="pix",
                        radius=10,
                        pos=(
                            - (self.scales_block_x + self.extent) + i * self.x_spacing,
                            y_pos,
                        ),
                        fillColor= (1, 1, 1) if default_response == i else (-1, -1, -1),
                        lineColor=(-1, -1, -1),
                        lineWidth=10,
                        autoLog=False,
                    )
                    for i in range(self.n_pts)
                ]

            for i, answer in enumerate(self.answers):
                self._legend(answer, i)

            self.text = visual.TextStim(
                self.exp_win,
                text = self.question,
                units="pix",

                pos=(-(self.scales_block_x + self.extent), 
                     y_pos + self.exp_win.size[1] * 0.30),
                wrapWidth= self.win_width-(self.win_width*0.1),
                height= self.y_spacing / 3,
                anchorHoriz="left",
                alignText="left"
            )
        
        def _handle_controller_presses(self):
            self.ISI.start(0.01)
            self._new_key_pressed = event.getKeys('lra')
            self.ISI.complete()

        def run(self):
            self._setup()
            n_flips = 0
            while True:
                self._handle_controller_presses()
                new_key_pressed = [k[0] for k in self._new_key_pressed]

                if "r" in new_key_pressed and self.response < self.n_pts - 1:
                    self.response += 1
                elif "l" in new_key_pressed and self.response > 0:
                    self.response -= 1
                elif "a" in new_key_pressed:
                    self._events.append({
                        "trial_type": self.trial_type,
                        "track": self.name,
                        "question": self.question,
                        "value": self.answers[self.response]
                    })
                    break

                elif n_flips > 1:
                    time.sleep(.01)
                    continue

                for bullet_n, bullet in enumerate(self.bullets):
                    bullet.fillColor = (1, 1, 1) if self.response == bullet_n else (-1, -1, -1)
                
                self.line.draw(self.exp_win)
                self.text.draw(self.exp_win)
                for legend, bullet in zip(self.legends, self.bullets):
                    legend.draw(self.exp_win)
                    bullet.draw(self.exp_win)
                #stim = self.line + self.bullets + self.text + self.legends
                #stim.draw(self.exp_win)

                n_flips += 1
                self.exp_win.flip()

#-------------------------------------------------------------------------------------------------------------


















class Playlist_cneuromod(object):#inherit from class Task(object) in task_base.py
    def __init__(self, name, fname_base, csv_path):
        file = open(csv_path, "r")
        self.playlist = list(csv.reader(file, delimiter=","))
        file.close()

    #---------from class Task(object) in task_base.py------------------------------------
    def _generate_unique_filename(self, suffix, ext="tsv"):
        fname = os.path.join(
            self.output_path, f"{self.output_fname_base}_{self.name}_{suffix}.{ext}"
        )
        fi = 1
        while os.path.exists(fname):
            fname = os.path.join(
                self.output_path,
                f"{self.output_fname_base}_{self.name}_{suffix}-{fi:03d}.{ext}",
            )
            fi += 1
        return fname

    def _save(self):
        out_fname = self._generate_unique_filename("events", "tsv")
        other_events = pandas.DataFrame(self._events)
        events_df = other_events
        events_df.to_csv(out_fname, sep="\t", index=False)
        return False

    def _log_event(self, event, clock='task'):
        if clock == 'task':
            onset = self.task_timer.getTime()
        elif clock == 'flip':
            onset = self._exp_win_last_flip_time - self._exp_win_first_flip_time
        event.update({"onset": onset, "sample": time.monotonic()})
        self._events.append(event)

    def save(self):
        # call custom task _save()
        save_events = self._save()
        if save_events is None and len(self._events):
            fname = self._generate_unique_filename("events", "tsv")
            df = pandas.DataFrame(self._events)
            df.to_csv(fname, sep="\t", index=False)
    #---------------------------------------------------------------------------------------------