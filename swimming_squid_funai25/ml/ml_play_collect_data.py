import pickle
import os
import random


class MLPlay:
    def __init__(self, *args, **kwargs):

        self.search_range = 1000
        self.data = []
        self.all_data = []

        # check if the directory dataset exists
        if not os.path.exists("dataset"):
            os.makedirs("dataset")
            print("Directory 'dataset' created.")

        # check if the file training_data.pkl exists
        if os.path.exists("dataset/training_data.pkl"):
            with open("dataset/training_data.pkl", "rb") as f:
                self.all_data = pickle.load(f)
            print(
                f"Loaded existing data with {len(self.all_data)} entries.")
        else:
            print("No existing data found, starting fresh.")

        self.last_status = None

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """

        
        score_vector = self.calculate_score(scene_info) # score for [up, down, left, right]
        print(score_vector)

        # decide the command according to score_vector
        command = self.decide_command(score_vector)

        # collect the data
        row = [score_vector[0], score_vector[1],
               score_vector[2], score_vector[3], command[0]]
        self.data.append(row)

        self.last_status = scene_info["status"]

        # return the command to move squid
        return command
    
    def calculate_score(self, scene_info):

        # 初始分數
        score_vector = [0, 0, 0, 0]  # [UP, DOWN, LEFT, RIGHT]
        squid_x, squid_y = scene_info["self_x"], scene_info["self_y"]

        for obj in scene_info["foods"]:  # "foods" 裡既包含食物，也包含垃圾
            obj_x, obj_y = obj["x"], obj["y"]
            obj_score = obj["score"]

            # 計算與物體的距離
            distance = self.get_distance(squid_x, squid_y, obj_x, obj_y)

            # 避免除以零
            if distance == 0:
                continue  

            # **食物影響力**
            if obj_score > 0:
                weight = obj_score / distance  # 食物影響力
            # **垃圾影響力（負數，影響力較弱）**
            else:
                weight = (obj_score * 0.5) / distance  # 讓垃圾的影響力較弱，避免過度驚慌

            # 根據物品位置影響得分向量
            if obj_y < squid_y:
                score_vector[0] += weight  # 影響 UP
            elif obj_y > squid_y:
                score_vector[1] += weight  # 影響 DOWN

            if obj_x < squid_x:
                score_vector[2] += weight  # 影響 LEFT
            elif obj_x > squid_x:
                score_vector[3] += weight  # 影響 RIGHT

        return score_vector



    def decide_command(self, score_vector):
        """
        Decide the command to move the squid
        """
        actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        max_score = max(score_vector)

    # 找出所有分數最高的方向，隨機選擇一個
        best_moves = [actions[i] for i in range(4) if score_vector[i] == max_score]

        return best_moves

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")

        if self.last_status == "GAME_PASS":
            self.all_data.extend(self.data)

            with open("dataset/training_data.pkl", "wb") as f:
                pickle.dump(self.all_data, f)
            print(f"Data appended, total {len(self.all_data)} entries saved.")

        self.data.clear()

    def get_distance(self, x1, y1, x2, y2):
        """
        Calculate the distance between two points
        """
        return ((x1-x2)**2 + (y1-y2)**2)**0.5
