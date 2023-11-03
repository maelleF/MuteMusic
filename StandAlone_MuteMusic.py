import csv
from psychopy import visual
from Task_MuteMusic import Track, Questionnaire

imagery_Question = ("During the silences, did you imagine the missing part of the different audio tracks you’ve heard ?", ['never', 'a few times', 'half the time', 'most of the time', 'always'])
familiarity_Question = ("Did you recognise the song ?", ['no', 'maybe', 'yes'])


playlist_path = './subXX_runXX.csv'
file = open(playlist_path, "r")
tracks = list(csv.reader(file, delimiter=","))
file.close()

exp_win = visual.Window(units="height", allowStencil=True)

for i, track in enumerate(tracks):
    track_path = track[0]
    Display_track = Track(track_path, exp_win, num=i+1)
    Display_track.run()

    imagery_form = Questionnaire(exp_win, question=imagery_Question[0], answers=imagery_Question[1])
    imagery_form.run()    
    familiarity_form = Questionnaire(exp_win, question=familiarity_Question[0], answers=familiarity_Question[1])
    familiarity_form.run()

exp_win.close()