import cv2
from tracker import *

# 추적기 객체 생성 따로 파일을 만든후 같은 위치에 넣어야 실행이 됩니다. 
tracker = EuclideanDistTracker() 

cap = cv2.VideoCapture('challenge.mp4')

# 카메라에서 물체 감지
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
#카메라가 고정되어 있기 때문에 기록이 100으로 설정되어 첫 번째 매개 변수. 대신 var 임계값은 값이 낮을수록 거짓 긍정을 만들 가능성이 커지므로 40입니다. 이 경우 더 큰 개체에만 집중
#배경 제거 함수: 히스토리 갯수 , 분산 임계 값 ,detectShadows=True로 설정하면 그림자를 회색으로 표시하고 속도가 다소 느려짐

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # 관심영역 추출

    roi = frame[240 : 480, 200 :504 ] #왼쪽 상단 점부터 오른쪽 하단점까지 사각형을 만들것이다  240 : 480 200 :504 
    #(y1:y2,x1:x2) 로 설정한다.

    # 1. Object Detection #객체 감지 
    mask = object_detector.apply(roi) #까만배경 
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY) #까만창 쓰레쉬홀드
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 모든 윤곽선을 검출하며, 계층 구조를 모두 형성 , 윤곽점들을 단순화 수평, 수직 및 대각선 요소를 압축하고 끝점만 냄김
    detections = []
    for cnt in contours:
        # 면적 계산 
        area = cv2.contourArea(cnt) #
        if area > 100:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2) #검출된 윤곽선을 그리기 (이미지, [윤곽선], 윤곽선 인덱스, (B, G, R), 두께, 선형 타입)
            x, y, w, h = cv2.boundingRect(cnt) #contour중 하나를 직사각형 형태로 x, y, w, h로 반환한다. contour의 외각으로 직사각형을 그리게 된다.

            detections.append([x, y, w, h])


    # 2. Object Tracking #객체 따라가기
    boxes_ids = tracker.update(detections) #각 개체에 대해 고유 id할당 
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2) #id 할당. 없어도 되는 코드
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3) #따라가면서 초록색 직사각형 만들기
        print("카메라부터의 거리는%d : %d m "  %(id,480-(y+h))) #수직으로 했을때 직선길이 

    cv2.imshow("roi", roi) #관심영역 설정한 창 출력 
    cv2.imshow("Frame", frame) #원래 비디오 출력
    cv2.imshow("Mask", mask) #배경제거한 마스크 출력 

    key = cv2.waitKey(30)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()