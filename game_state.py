"""
ゲームのスコアや残機などの状態を管理するクラス。
（現状は未使用だが、スコア・ライフ管理用のサンプル）
"""

class GameState:
    def __init__(self):
        """
        ゲーム状態の初期化（スコア・残機）
        """
        self.score = 0
        self.lives = 3

    def add_score(self, points):
        """
        スコアを加算する。
        :param points: 加算する得点
        """
        self.score += points

    def lose_life(self):
        """
        残機を1減らし、ゲームオーバー判定を返す。
        :return: "game_over" or "continue"
        """
        self.lives -= 1
        if self.lives <= 0:
            return "game_over"
        return "continue"
