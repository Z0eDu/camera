import RPi.GPIO as GPIO
import time
import os
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera



def GPIO21_callback(channel):
	print '76876'
	if GPIO.input(21):
		print '21'
		GPIO.output(24, 1)  #video LED
		camera.start_recording('/home/pi/camera/video/video%02d'%j[0]+'.h264',quality=23)
		video[0]=True
		
	else:
		print '210'
		video[0]=False
		camera.stop_recording()
		j[0]+=1
		GPIO.output(24, 0)  #video LED


def GPIO19_callback(channel):  #picutre
	GPIO.output(23, 1)  #video LED
	print 'take pic'
	t=time.time()
	camera.capture('/home/pi/camera/image/image%02d'%i[0]+'.jpg', use_video_port=True)
	print(time.time()-t)
	i[0]+=1
	
	GPIO.output(23, 0)  #video LED
	#GPIO.add_event_detect(19, GPIO.RISING, callback=GPIO19_callback, bouncetime=300) #picture 
	
def GPIO13_callback(channel):
	os.system('sudo shutdown -h now')

def main():
	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(21, GPIO.IN)  #video signal
		GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #picutre signal
		GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #on/off signal
		
		GPIO.setup(23, GPIO.OUT,initial=0) #picutre LED
		GPIO.setup(18, GPIO.OUT,initial=1) #turn on LED	GPIO.setup(18, GPIO.OUT,initial=1) #turn on LED
		GPIO.setup(20, GPIO.OUT,initial=1) #pos
		GPIO.setup(24, GPIO.OUT,initial=0) #video LED
		
		GPIO.add_event_detect(21, GPIO.BOTH, callback=GPIO21_callback, bouncetime=300) #video
		GPIO.add_event_detect(19, GPIO.RISING, callback=GPIO19_callback, bouncetime=300) #picture 
		GPIO.add_event_detect(13, GPIO.FALLING, callback=GPIO13_callback, bouncetime=300) #on/off
		
		global i
		global j
		i=[0] #count for picutures
		j=[0] #count for videos
		
		global camera
		camera=PiCamera(resolution=(640,480), framerate=32)
		global video
		video=[False]
		time.sleep(1)
		while (True):
			while(video[0]):
				camera.wait_recording(1)
			print 'loop'
			time.sleep(5)
	except KeyboardInterrupt:
		GPIO.cleanup()
		camera.close()
main()
