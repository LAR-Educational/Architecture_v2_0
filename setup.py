import pip
import settings
import os
import sys

def find(package):
	try:
		if package == 'opencv-python':
			package = 'cv2'
		return __import__(package)
	except:
		return None

def install(package):
    pip.main(['install', '-q', package])

if os.getuid() != 0:
	settings.info('Script must run with sudo.', 3)
	sys.exit(-1)

packages = [
			'wikipedia',
			'textblob',
			'translate',
			'numpy',
			'scipy',
			'sklearn',
			'opencv-python',
			'requests'
			]

for pkg in packages:
	settings.info('Checking for ' + pkg + '...')
	if find(pkg) is None:
		settings.info('Package not found, installing...')
		install(pkg)
		settings.info('Instaled.')

os.system('python -m textblob.download_corpora')
