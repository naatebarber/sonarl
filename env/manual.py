'''
    Manually control env with standard input to debug
'''

from env import SonarWithAccelerometerBarometer

e = SonarWithAccelerometerBarometer()
e.set_init_position([0,0,0]).set_init_velocity([0,0,0])
ordi = e.reset()
# while ordi[2] is False:
#     print(ordi[1])
#     ordi = e.step(int(input("0-7: ") or 9))

e.position = [0, 0, -500]
for i in range(10):
    e.position_vec_prev = e.dist_from_center()
    e.position[2] += 100
    print("Reward ", e.ordi()[1])
    print("Distance ", e.dist_from_center())