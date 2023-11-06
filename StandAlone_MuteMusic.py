import csv
from psychopy import visual
from Task_MuteMusic import Playlist_StandAlone

exp_win = visual.Window(units="height", allowStencil=True)
playlist_path = './subXX_runXX.csv'

run = Playlist_StandAlone(playlist_path, exp_win)
run.run()

exp_win.close()