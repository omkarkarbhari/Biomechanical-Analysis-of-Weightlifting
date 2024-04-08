import cv2
import numpy as np

ix, iy, k = 200, 200, 1
xc = []
yc = []

def onMouse(event, x, y, flag, param):
    global ix, iy, k
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        k = -1

def run(filename):
    global ix, iy, k, xc, yc

    cv2.namedWindow("window")
    cv2.resizeWindow("window", 900, 600)
    cv2.setMouseCallback("window", onMouse)
    cap = cv2.VideoCapture(filename)

    # Initial processing and user input
    while True:
        _, frm = cap.read()
        if frm is None:
            break
        frm = cv2.resize(frm, (900, 600))
        cv2.imshow("window", frm)
        key = cv2.waitKey(0)  # Wait for a key press to advance
        if key == 27 or k == -1:
            old_gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            cv2.destroyAllWindows()
            break

    old_pts = np.array([[ix, iy]], dtype="float32").reshape(-1, 1, 2)
    mask = np.zeros_like(frm)

    prev_y = iy  # Initial y-coordinate

    while True:
        _, frame2 = cap.read()
        if frame2 is None:
            break

        frame2 = cv2.resize(frame2, (900, 600))
        new_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        new_pts, status, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, old_pts, None, maxLevel=1,
                                                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 0.08))

        x, y = new_pts.ravel()
        color = (0, 255, 0) if y < prev_y else (0, 0, 255)  # Green for up, Red for down
        cv2.circle(mask, (int(x), int(y)), 2, color, 2)

        combined = cv2.addWeighted(frame2, 0.7, mask, 0.3, 0.1)
        cv2.imshow("combined", combined)

        old_gray = new_gray.copy()
        old_pts = new_pts.copy()
        prev_y = y

        xc.append(x)
        yc.append(y)

        key = cv2.waitKey(0)  # Wait for a key press to advance
        if key == 27:
            break

    temp = list(zip(xc, yc))
    pts = np.array(temp, np.int32)
    pts = pts.reshape((-1, 1, 2))
    image = np.zeros((600, 900, 3), dtype=np.uint8)

    # Color the path based on up or down movement
    for i in range(1, len(pts)):
        color = (0, 255, 0) if yc[i] < yc[i-1] else (0, 0, 255)  # Green for up, Red for down
        image = cv2.line(image, tuple(pts[i-1][0]), tuple(pts[i][0]), color, 2)

    # Mark initial and final positions
    image = cv2.circle(image, (int(xc[0]), int(yc[0])), 5, (255, 255, 255), -1)
    image = cv2.circle(image, (int(xc[-1]), int(yc[-1])), 5, (255, 255, 0), -1)
    cv2.putText(image, 'Initial Position', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    cv2.putText(image, 'Final Position', (30, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    cv2.imshow('plot', image)
    cv2.waitKey(0)
    cv2.imwrite('barbellyour.jpeg', image)
    print(max(xc), min(xc))

    cv2.destroyAllWindows()
    cap.release()

    return 'barbellyour.jpeg'

# Uncomment and specify the correct file path to run the function
#run(r'/Users/shruti/Downloads/CJ_FV_G_1.mp4')
