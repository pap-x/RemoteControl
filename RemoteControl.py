from SimpleCV import *
import time
import win32com.client as comclt

firefox = Image("firefox.jpg")
chrome = Image("chrome.jpg")
img2 = Image("draw.jpg")

display = SimpleCV.Display()
cam = SimpleCV.Camera()

now = time.time() 
while (display.isNotDone()) & (now+3>time.time()):
	img = cam.getImage().flipHorizontal()
	dist = img.colorDistance(SimpleCV.Color.BLUE).dilate(2)
	segmented = dist.stretch(200,255)
	blobs = segmented.findBlobs()
	if blobs:
		circles = blobs.filter([b.isCircle(0.25) for b in blobs])
		if circles:
			img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLACK,3)
			img2.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLACK,-1)

	img.save(display)

	if display.mouseLeft:
		break

img2.save("res.jpg")
img2 = Image("res.jpg")

diff1 = firefox - img2
diff2 = chrome - img2
sum1 = 0
sum2 = 0

for i in range(diff1.size()[0]):
	for j in range(diff1.size()[1]):
		if diff1[i,j][0] == 255:
			sum1 += 1
		if diff2[i,j][0] == 255:
			sum2 += 1

wsh = comclt.Dispatch("WScript.Shell")
if sum1<sum2:
	wsh.Run("firefox") # select another application
else:
	wsh.Run("chrome")