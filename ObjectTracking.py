import imutils #resize
import cv2
redLower=(28,69,120)
redUpper=(171,255,224)
camera=cv2.VideoCapture(0) # iniitalize the camera

while True:
    ret, frame = camera.read() # read the camera frame
    frame=imutils.resize(frame,width=1000) # resize the frame
    blurred=cv2.GaussianBlur(frame,(11,11),0) # blur the frame
    hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV) # convert to HSV
    mask=cv2.inRange(hsv,redLower,redUpper) # create a mask out of the range /// mask the object color
    mask=cv2.erode(mask,None,iterations=2) # erode the mask  remove noise or left overs
    mask=cv2.dilate(mask,None,iterations=2) # dilate the mask
    contours=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] # find contours
    center=None
    if len(contours)>0: # if there are contours
        c=max(contours,key=cv2.contourArea)
        ((x,y),radius)=cv2.minEnclosingCircle(c) # find the minimum enclosing circle
        M=cv2.moments(c) # find the moments
        center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"])) # find the center
        if radius >10:
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,0),2)
            cv2.circle(frame,center,5,(0,255,0),-1)
            print(center,radius)
            if radius >250:
                print("stop")
            else:
                if center[0]<150:
                    print("Right")
                elif center[0]>450:
                    print("Left")
                elif radius <250:
                    print("front")
                else:
                    print("Stop")
    cv2.imshow("frame",frame)
    k=cv2.waitKey(1)
    if k==27:
        break
camera.release()
cv2.destroyAllWindows()