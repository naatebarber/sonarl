'''
    Manually control env with standard input to debug
'''

from env import SonarWithAccelerometerBarometer

e = SonarWithAccelerometerBarometer()
ordi = e.reset()
while ordi[2] is False:
    ordi = e.step(int(input("0-7: ") or 9))