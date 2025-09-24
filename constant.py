import tkinter as tk  # GUIアプリケーション作成のための標準的なPythonインターフェース

class constant():
    TILE_SIZE = 40
    CHAR_SIZE = 40
    GRID_SIZE = 21
    SCREEN_WIDTH = TILE_SIZE  * GRID_SIZE
    SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE
    FPS = 60
    PLAYER_SPEED = 2
    ENEMY_SPEED = 2
    INITIAL_LIVES = 3
    FONT_NAME = "yumincho"
    FONT_SIZE = 24
    TITLE_IMAGE_PATH = "assets\\title\\titleSample.png"
    BACKGROUND_COLOR = (0, 0, 0)
    PLAYER_START_POS = (1, 1)
    ENEMY_START_POSITIONS = [(10, 1), (10, 10), (1, 10)]
    PELLET_SCORE = 10
    POWER_PELLET_SCORE = 50
    GHOST_SCORE = 200
    LEVEL_UP_SCORE = 1000
    MAX_LEVEL = 5
    DEBUG_MODE = False

    def __init__(self):
        self.aa = self.TILE_SIZE
        dwith,dheight = self.get_screen_size()

    def get_screen_size():
        """
        使用しているPCの画面サイズ（幅と高さ）を辞書形式で返します。

        tkinterの機能を使用して、現在の画面解像度を取得します。

        Returns:
            list of dict: 画面の幅と高さをキーとする辞書のリスト。
        """
        
        # tkinterのルートウィンドウを作成
        root = tk.Tk()  
        
        # ウィンドウを表示せずに実行
        root.withdraw()  
        
        # 画面の幅を取得
        width = root.winfo_screenwidth()  
        
        # 画面の高さを取得
        height = root.winfo_screenheight()  
        
        # ルートウィンドウを破棄
        root.destroy()  
        
        # 画面サイズを辞書形式でリストにして返す
        return (width, height)
