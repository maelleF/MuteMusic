import csv, time
from psychopy import visual, event, core
from Task_MuteMusic import Track

playlist_path = './subXX_runXX.csv'
file = open(playlist_path, "r")
tracks = list(csv.reader(file, delimiter=","))
file.close()

questions = [
    {
    'index': None,
    'itemText': "During the silences, did you imagine the missing part of the different audio tracks you’ve heard ?",
    'itemWidth': 1,
    "type": 'rating',
    'responseWidth': 1,
    'options': ['never', 'a few times', 'half the time', 'most of the time', 'always'],
    'layout': 'horiz'
    },
    {
    'index': None,
    'itemText': "Did you recognise the song ?",
    'itemWidth': 1,
    'type': 'rating',
    'responseWidth': 1,
    'options': ['no', 'yes'],
    'layout': 'horiz'
    }]

exp_win = visual.Window(units="height", allowStencil=True)
imagery_form = visual.Form(win=exp_win, items=questions, units="height")
ISI = core.StaticPeriod(win=exp_win)

for i, track in enumerate(tracks):
    track_path = track[0]
    Display_track = Track(track_path, exp_win, num=i+1)
    Display_track.run()
    imagery_form.draw()
    exp_win.flip()

    while True :
        ISI.start(1)
        keys = event.getKeys(keyList='uldra')
        ISI.complete()
        if 'a' in keys:
            break
        print(keys)
    pass
    
        
exp_win.close()