import csv
from psychopy import visual
from Task_MuteMusic import MuteMusic

playlist_path = './subXX_runXX.csv'
file = open(playlist_path, "r")
tracks = list(csv.reader(file, delimiter=","))
file.close()

exp_win = visual.Window()

#basic instructions for psychopy--------------
#instruction = visual.TextStim(win=exp_win, text=DEFAULT_INSTRUCTION)
#instruction.draw()
#exp_win.flip()
#time.sleep(1) #core.wait(1.0)

for i, track in enumerate(tracks):
    track_path = track[0]
    Display_track = MuteMusic(track_path, exp_win)
    Display_track.run()

    #basic instructions for psychopy--------------
    #track_nb = visual.TextStim(win=exp_win, text="track {}".format(i))
    #track_nb.draw()
    #track_path = track[0]
    #track = sound.Sound(track_path)
    #track.play()
    #exp_win.flip()
    #time.sleep(track.duration)#core.wait(2.0)

exp_win.close()