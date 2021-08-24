import math


class EuclideanDistTracker:
    def __init__(self):
        # 객체의 중앙 좌표 저장 
        self.center_points = {}
        # id 갯수 유지 
        # 새 객체가 탐지될때마다 +1씩 카운트 된다 
        self.id_count = 0 # 0부터 시작


    def update(self, objects_rect): 
        # 객체상자 / id
        objects_bbs_ids = [] #방 생성

        # 새 객체의 중앙점 
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2 #cx 중앙좌표의 x
            cy = (y + y + h) // 2 #cy 중앙좌표의 y

            # 해당 객체가 이미 탐지되어있던건지 판단 
            same_object_detected = False
            for id, pt in self.center_points.items(): 
                dist = math.hypot(cx - pt[0], cy - pt[1]) #인수로 전달받은 값들을 제곱한후 총합의 제곱근을 반환 

                if dist < 25:
                    self.center_points[id] = (cx, cy) #중앙 좌표 id는 갯수를 세는 카운트 
                    #print(self.center_points) #앞서 객체를 contour에서 가져왔던 중앙 좌표(cx,cy)를 출력한다.
                    objects_bbs_ids.append([x, y, w, h, id]) #추가 
                    same_object_detected = True
                    break

            # 새 객체로 확인되면 새로운 id를 준다 
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1 #id(객체의 갯수)에 + 1 해서 카운트 하는식으로 

        # Clean the dictionary by center points to remove IDS not used anymore
        #중앙점으로 사전을 정리하여 더 이상 사용되지 않는 IDS 제거
        new_center_points = {} #새로운 객체가 발견되었을 시(새로운 중앙 좌표)
        for obj_bb_id in objects_bbs_ids: 
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center 

        # 사용되지 않은 id로 제거 함. 
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



