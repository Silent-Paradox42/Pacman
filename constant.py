import tkinter # GUIアプリケーション作成のための標準的なPythonインターフェース
import ctypes
from ctypes import wintypes

class const:
    TILE_SIZE = 40
    CHAR_SIZE = 40
    GRID_SIZE = 21
    SCREEN_WIDTH = TILE_SIZE * GRID_SIZE
    SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)  # ← 追加
    FPS = 60
    PLAYER_SPEED = 2
    ENEMY_SPEED = 2
    INITIAL_LIVES = 3
    MAIN_FONT_NAME = "yumincho"
    MAIN_FONT_SIZE = 48
    SUB_FONT_NAME = "yumincho"
    SUB_FONT_SIZE = 36
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
    INPUT_TIME = 10000
    NEXT_FONT_SIZE = 100
    MAP_DATA = {
        1: 'assets/map/stage1.csv',
        2: 'assets/map/stage2.csv',
        3: 'assets/map/sample_stage3.csv',
        90: 'assets/map/pacman_stage.csv',
        91: 'assets/map/sample_stage.csv',
    }

    # --- 画面サイズ取得(作業領域) ---
    def get_screen_size():
        try:
            user32 = ctypes.windll.user32
            work_area = wintypes.RECT()
            SPI_GETWORKAREA = 0x0030
            result = user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0)
            if result:
                width = work_area.right - work_area.left
                height = work_area.bottom - work_area.top
                return(width, height)
        except Exception:
            try:
                root = tkinter.Tk()
                root.withdraw()
                width = root.winfo_screenwidth()
                height = root.winfo_screenheight()
                root.destroy()
                return (width, height)
            except Exception:
                return None

    @staticmethod # staticmethodデコレータを使用して、インスタンス化せずに呼び出せるようにする
    def get_screen_size():
        """画面の作業領域のサイズを取得する関数"""
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            work_area = wintypes.RECT()
            SPI_GETWORKAREA = 0x0030
            result = user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0)

            if result:
                width = work_area.right - work_area.left
                height = work_area.bottom - work_area.top
                return (width, height)
            else:
                return None  # API呼び出し失敗時
        except Exception as e:
            print(f"get_screen_size fallback: {e}")
            try:
                root = tkinter.Tk()
                root.withdraw()
                width = root.winfo_screenwidth()
                height = root.winfo_screenheight()
                root.destroy()
                return (width, height)
            except Exception as e:
                print(f"tkinter fallback failed: {e}")
                return None
