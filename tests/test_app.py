import pytest
import pygame

from core.settings import DIFFICULTY_LEVEL

from core.scene_manager import SceneManager
from core.game import Game
from scenes.free_gamemode_scene import GameScene
from scenes.limited_ammo_gamemode_scene import LimitedAmmoGameModeScene
from scenes.limited_time_gamemode_scene import LimitedTimeGameModeScene
from scenes.menu_scene import MenuScene
from scenes.pause_scene import PauseScene
from scenes.score_scene import ScoreScene
from scenes.settings_scene import SettingsMenu

from entities.duck import Duck
from entities.gun import Gun

@pytest.fixture
def scene_manager():
    return SceneManager()

import os

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def test_scene_manager_add_and_set_scene(scene_manager):
    screen = pygame.display.set_mode((900, 800))
    menu_scene = MenuScene(scene_manager)
    scene_manager.add_scene("menu", menu_scene)

    assert "menu" in scene_manager.scenes, "Сцена 'menu' має бути у словнику сцен"

    scene_manager.set_scene("menu")
    assert scene_manager.active_scene == menu_scene, "Активна сцена має бути menu_scene"


def test_scene_manager_update_draw_no_active(scene_manager):
    try:
        fake_events = []
        scene_manager.update(fake_events)
        scene_manager.draw(None)  # передаємо None замість реального 'screen'
    except Exception as e:
        pytest.fail(f"scene_manager.update/draw викликало помилку: {e}")


def test_game_scene_basic():

    class FakeSceneManager:
        def set_scene(self, name):
            pass

    scene_manager = FakeSceneManager()
    game_scene = GameScene(scene_manager)

    fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100))
    game_scene.handle_events([fake_event])

    game_scene.update()

    test_surface = pygame.Surface((800, 600))
    game_scene.draw(test_surface)


def test_limited_ammo_scene_end():

    class FakeSceneManager:
        def __init__(self):
            self.scenes = {}
            self.active_scene = None

        def set_scene(self, name):
            self.active_scene = self.scenes.get(name)

    scene_manager = FakeSceneManager()
    score_scene = ScoreScene(scene_manager)
    scene_manager.scenes["score"] = score_scene

    limited_ammo_scene = LimitedAmmoGameModeScene(scene_manager)
    scene_manager.scenes["limited_ammo"] = limited_ammo_scene

    for _ in range(10):
        fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(300, 300))
        limited_ammo_scene.handle_events([fake_event])

    assert scene_manager.active_scene == score_scene, "Після 10 кліків має перейти у сцену score"



def test_limited_time_scene_timer():

    class FakeSceneManager:
        def __init__(self):
            self.scenes = {}
            self.active_scene = None

        def set_scene(self, name):
            self.active_scene = self.scenes.get(name)

    scene_manager = FakeSceneManager()
    score_scene = ScoreScene(scene_manager)
    scene_manager.scenes["score"] = score_scene

    limited_time_scene = LimitedTimeGameModeScene(scene_manager)
    limited_time_scene.time_limit = 100  
    scene_manager.scenes["limited_time"] = limited_time_scene

    limited_time_scene.start_time -= 200  

    limited_time_scene.update()

    assert scene_manager.active_scene == score_scene, "Після закінчення часу має перейти у score"


def test_duck_update():
    duck = Duck(x=0, y=100, move_angle=0, direction="left") 
    initial_x = duck.x
    initial_y = duck.y

    duck.update()

    assert duck.x != initial_x or duck.y != initial_y, "Качка має змінити свої координати після update()"


def test_duck_get_score_value():
    duck = Duck(x=0, y=0, move_angle=0, direction="left")
    val = duck.get_score_value()
    assert 10 <= val <= 50, "Очки за качку мають потрапляти у діапазон [30..45], залежно від speed"


def test_settings_menu():
    
    class FakeSceneManager:
        def __init__(self):
            self.scenes = {}
            self.active_scene = None

        def set_scene(self, name):
            self.active_scene = name

    pygame.init()

    scene_manager = FakeSceneManager()

    settings_menu = SettingsMenu(scene_manager)
    scene_manager.scenes["settings"] = settings_menu

    menu_scene = MenuScene(scene_manager)
    scene_manager.scenes["menu"] = menu_scene

    fake_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(430, 320)) 
    settings_menu.handle_events([fake_click, fake_click])

    assert DIFFICULTY_LEVEL[0] == 0, "Після кліку по easy_mode_rect мають встановити DIFFICULTY_LEVEL=0"
    print(scene_manager.active_scene)
    assert scene_manager.active_scene == "menu", "Після вибору easy має переходити в menu"
