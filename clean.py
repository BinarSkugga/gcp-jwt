import os
import shutil

dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(dir, 'build')):
    shutil.rmtree(os.path.join(dir, 'build'))
if os.path.exists(os.path.join(dir, 'dist')):
    shutil.rmtree(os.path.join(dir, 'dist'))

for i in os.listdir(dir):
    if i.endswith('.egg-info'):
        shutil.rmtree(os.path.join(dir, i))
