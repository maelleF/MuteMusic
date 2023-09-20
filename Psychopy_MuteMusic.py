import csv, time
from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']
from psychopy import visual, sound, core

#Global Variables if multiples tasks

#class MuteMusic(Task):

#Global Variables to the Task

DEFAULT_INSTRUCTION = """Listen to the following track"""
AUDITORY_IMAGERY_ASSESSMENT = """During the silences, did you imagine the missing part of the different audio tracks you’ve heard ?"""
FAMILIARITY_ASSESSMENT = """Did you recognise the song ?"""

#task : 1 run = 1 playlist = around 10 audio tracks
#repeat for n songs in subXX_runXX.csv :
#   step 1: DEFAULT_INSTRUCTION
#   step 2: display audio
#   step 3: Auditory imagery assessment
#   step 4: Familiarity assessment

def __init__():
    pass
 
def _instructions():
    pass

def _run():
    pass

def _setup():
    pass

def _stop():
    pass

def _save():
    pass

def _restart():
    pass

def _questionnaire(self, exp_win, ctl_win, questions):
    if questions is None:
        return
    exp_win.setColor([0] * 3, colorSpace='rgb')
    lines = []
    bullets = []
    responses = []
    texts = []
    legends = []
    y_spacing = 80
    win_width = exp_win.size[0]
    scales_block_x = win_width * 0.25
    scales_block_y = len(questions) // 2 * y_spacing
    extent = win_width * 0.2

    # add legends to Likert scale
    legends.append(visual.TextStim(
        exp_win,
        text = 'Disagree',
        units="pix",
        pos=(scales_block_x - extent*0.75, scales_block_y*1.1),
        wrapWidth= win_width * 0.5,
        height= y_spacing / 3,
        anchorHoriz="right",
        alignText="right",
        bold=True
    ))
    legends.append(visual.TextStim(
        exp_win,
        text = 'Agree',
        units="pix",
        pos=(scales_block_x + extent*1.15, scales_block_y*1.1),
        wrapWidth= win_width * 0.5,
        height= y_spacing / 3,
        anchorHoriz="right",
        alignText="right",
        bold=True
    ))


    active_question = 0

    # create all stimuli
    #all_questions_text = ""
    for q_n, (key, question, n_pts) in enumerate(questions):
        default_response = n_pts // 2
        responses.append(default_response)
        x_spacing = extent * 2 / (n_pts - 1)
        #all_questions_text += question + "\n\n"

        y_pos = scales_block_y - q_n * y_spacing

        lines.append(
            visual.Line(
                exp_win,
                (scales_block_x - extent, y_pos),
                (scales_block_x + extent, y_pos),
                units="pix",
                lineWidth=6,
                autoLog=False,
                lineColor=(0, -1, -1) if q_n == 0 else (-1, -1, -1),
            )
        )
        bullets.append(
            [
                visual.Circle(
                    exp_win,
                    units="pix",
                    radius=10,
                    pos=(
                        scales_block_x - extent + i * x_spacing,
                        y_pos,
                    ),
                    fillColor= (1, 1, 1) if default_response == i else (-1, -1, -1),
                    lineColor=(-1, -1, -1),
                    lineWidth=10,
                    autoLog=False,
                )
                for i in range(n_pts)
            ]
        )
        texts.append(visual.TextStim(
            exp_win,
            text = question,
            units="pix",
            bold = q_n == active_question,
            pos=(0, y_pos),
            wrapWidth= win_width * 0.5,
            height= y_spacing / 3,
            anchorHoriz="right",
            alignText="right"
        ))
        responses[q_n] = default_response



    # questionnaire interaction loop
    n_flips = 0
    while True:
        self._handle_controller_presses(exp_win)
        new_key_pressed = [k[0] for k in self._new_key_pressed]
        if "u" in new_key_pressed and active_question > 0:
            active_question -= 1
        elif "d" in new_key_pressed and active_question < len(questions)-1:
            active_question += 1
        elif "r" in new_key_pressed and responses[active_question] < n_pts - 1:
            responses[active_question] += 1
        elif "l" in new_key_pressed and responses[active_question] > 0:
            responses[active_question] -= 1
        elif "a" in new_key_pressed:
            for (key, question, n_pts), value in zip(questions, responses):
                self._log_event({
                    "trial_type": "questionnaire-answer",
                    "game": self.game_name,
                    "level": self.state_name,
                    "stim_file": self.movie_path,
                    "question": key,
                    "value": value
                })
            break
        elif n_flips > 1:
            time.sleep(.01)
            continue

        if n_flips > 0: #avoid double log when first loading questionnaire
            self._log_event({
                "trial_type": "questionnaire-value-change",
                "game": self.game_name,
                "level": self.state_name,
                "stim_file": self.movie_path,
                "question": questions[active_question][0],
                "value": responses[active_question]
            })

        exp_win.logOnFlip(
            level=logging.EXP,
            msg="level ratings %s" % responses)
        for q_n, (txt, line, bullet_q) in enumerate(zip(texts, lines, bullets)):
            #txt.bold = q_n == active_question
            txt._pygletTextObj.set_style('bold', q_n == active_question)
            line.lineColor = (0, -1, -1) if q_n == active_question else (-1, -1, -1)
            for bullet_n, bullet in enumerate(bullet_q):
                bullet.fillColor = (1, 1, 1) if responses[q_n] == bullet_n else (-1, -1, -1)

        for stim in lines + sum(bullets, []) + texts + legends:
            stim.draw(exp_win)
        yield True
        n_flips += 1

if __name__=="__main__":
    playlist_path = './subXX_runXX.csv'
    file = open(playlist_path, "r")
    tracks = list(csv.reader(file, delimiter=","))
    file.close()
    
    exp_win = visual.Window()
    instruction = visual.TextStim(win=exp_win, text=DEFAULT_INSTRUCTION)
    instruction.draw()
    exp_win.flip()
    time.sleep(1) #core.wait(1.0)

    for i, track in enumerate(tracks):

        track_nb = visual.TextStim(win=exp_win, text="track {}".format(i))
        track_nb.draw()
        track_path = track[0]
        track = sound.Sound(track_path)
        track.play()
        exp_win.flip()
        time.sleep(track.duration)#core.wait(2.0)
    
    exp_win.close()