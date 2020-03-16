import numpy as np

config = np.load('init_config.npy')
pubstring = '''header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: 'map'
pose:
  pose:
    position: {x: ''' + str(config[0]) + ", y: " + str(config[1]) + ", z: " + str(config[2]) + '''}
    orientation: {x: ''' + str(config[3]) + ", y: " + str(config[4]) + ", z: " + str(config[5]) + ", w: " + str(config[6]) + '''}
  covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0] '''
print(pubstring)
