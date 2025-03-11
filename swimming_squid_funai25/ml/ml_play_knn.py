import os
import pickle
import math


class MLPlay:
    def __init__(self, *args, **kwargs):
        print("Initial ml script")

        self.search_range = 1000
        encoder_path = "dataset/knn_encoder.pkl"
        model_path = "dataset/knn_model.pkl"  # Adjust path if needed
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        if not os.path.exists(encoder_path):
            raise FileNotFoundError(
                f"Encoder file not found at {encoder_path}")
        with open(encoder_path, "rb") as f:
            self.encoder = pickle.load(f)

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        score_vector = self.calculate_score(scene_info)  # score for [up, down, left, right]

        # Feature vector must match training format
        X = [score_vector[0], score_vector[1],
             score_vector[2], score_vector[3]]

        # Predict the numeric label
        pred_label = self.model.predict([X])[0]

        # Convert numeric label back to command if using encoder
        action = self.encoder.inverse_transform([pred_label])[0]

        return [action]  # Return as a list, e.g., ["UP"]
    
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



    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass

    def get_distance(self, x1, y1, x2, y2):
        """
        Calculate the distance between two points
        """
        return ((x1-x2)**2 + (y1-y2)**2)**0.5
