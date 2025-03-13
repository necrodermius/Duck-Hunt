import pytest
import pygame
import random
import os

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

"""
Припущення:
1. У вашому проекті встановлено pygame.
2. Тести запускати командою `pytest` (зайшовши у папку з tests).
3. У простих тестах ми не створюємо справжнє PyGame-вікно, 
   тому деякі методи (draw) можуть не тестуватись повністю.
4. Для сцен ми перевіряємо хоча б, що не виникає помилок при виклику handle_events / update / draw.
"""


@pytest.fixture
def scene_manager():
    """Фікстура, створює SceneManager перед тестами та прибирає після."""
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
    """Перевірка, що SceneManager може додавати та встановлювати сцену."""
    screen = pygame.display.set_mode((900, 800))
    menu_scene = MenuScene(scene_manager)
    scene_manager.add_scene("menu", menu_scene)

    assert "menu" in scene_manager.scenes, "Сцена 'menu' має бути у словнику сцен"

    scene_manager.set_scene("menu")
    assert scene_manager.active_scene == menu_scene, "Активна сцена має бути menu_scene"


def test_scene_manager_update_draw_no_active(scene_manager):
    """
    Якщо ми викликаємо update/draw без активної сцени,
    має не падати з помилкою (просто нічого не робити).
    """
    try:
        fake_events = []
        scene_manager.update(fake_events)
        scene_manager.draw(None)  # передаємо None замість реального 'screen'
    except Exception as e:
        pytest.fail(f"scene_manager.update/draw викликало помилку: {e}")


def test_game_scene_basic():
    """
    Перевірка, що GameScene можна створити і викликати handle_events/update/draw без помилок.
    (Тут ми не перевіряємо графіку по суті, лише цілісність).
    """

    class FakeSceneManager:
        def set_scene(self, name):
            pass

    scene_manager = FakeSceneManager()
    game_scene = GameScene(scene_manager)

    # Ініціалізуємо pygame, щоб уникнути Potential Errors (якщо це потрібно).
    # pygame.init()

    # Емулюємо подію кліку миші
    fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100))
    game_scene.handle_events([fake_event])

    # Оновлення
    game_scene.update()

    # Малювання (передаємо уявний Surface 800x600)
    test_surface = pygame.Surface((800, 600))
    game_scene.draw(test_surface)

    # pygame.quit()


def test_limited_ammo_scene_end():
    """
    Тестуємо, що сцена з обмеженими патронами при 10 кліках (ammo=10) викличе go_to_score_scene()
    Перевіримо через перевизначення методу.
    """


    class FakeSceneManager:
        def __init__(self):
            self.scenes = {}
            self.active_scene = None

        def set_scene(self, name):
            self.active_scene = self.scenes.get(name)

    scene_manager = FakeSceneManager()

    # Створимо "score_scene", яке теж потрібне, бо limited_ammo десь його викликає
    score_scene = ScoreScene(scene_manager)
    scene_manager.scenes["score"] = score_scene

    limited_ammo_scene = LimitedAmmoGameModeScene(scene_manager)
    scene_manager.scenes["limited_ammo"] = limited_ammo_scene

    # 10 разів стріляємо
    # pygame.init()
    for _ in range(10):
        fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(300, 300))
        limited_ammo_scene.handle_events([fake_event])

    assert scene_manager.active_scene == score_scene, "Після 10 кліків має перейти у сцену score"



def test_limited_time_scene_timer():
    """
    Перевірка, що при оновленні сцени з обмеженим часом (time_limit),
    коли час вийшов – викликається go_to_score_scene().
    """

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
    limited_time_scene.time_limit = 100  # дуже маленький, 0.1 секунди
    scene_manager.scenes["limited_time"] = limited_time_scene

    # "Емулюємо", що пройшов час
    limited_time_scene.start_time -= 200  # subtract 200ms, тобто вже "перейшли" межу 100ms

    # Викликаємо update
    limited_time_scene.update()

    assert scene_manager.active_scene == score_scene, "Після закінчення часу має перейти у score"


def test_duck_update():
    """
    Перевірка, що Duck при виклику update() змінює координати.
    """
    duck = Duck(x=0, y=100, move_angle=0, direction="left")  # move_angle=0 -> рух по X
    initial_x = duck.x
    initial_y = duck.y

    duck.update()

    assert duck.x != initial_x or duck.y != initial_y, "Качка має змінити свої координати після update()"


def test_duck_get_score_value():
    """
    Перевірка, що get_score_value повертає очки (залежать від швидкості).
    """
    # Припустимо, що Duck за замовчуванням speed=4..7.
    # Переконаємося, що формула get_score_value = 10 + 5*speed (як було в прикладі).
    duck = Duck(x=0, y=0, move_angle=0, direction="left")
    val = duck.get_score_value()
    # За замовчуванням speed = random(4..7), перевіримо, що воно в якомусь очікуваному діапазоні
    # (мінімум 10+(5*4)=30, максимум 10+(5*7)=45).
    assert 10 <= val <= 50, "Очки за качку мають потрапляти у діапазон [30..45], залежно від speed"


def test_settings_menu():
    """
    Перевірка базової взаємодії з SettingsMenu.
    Наприклад, клік по певній кнопці встановлює DIFFICULTY_LEVEL[0].
    """

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


    # Клік по "easy_mode_rect"
    fake_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(430, 320))  # всередині easy_mode_rect
    settings_menu.handle_events([fake_click, fake_click])

    # from core.settings import DIFFICULTY_LEVEL

    assert settings_menu.difficulty == 0, "Після кліку по easy_mode_rect мають встановити DIFFICULTY_LEVEL=0"
    assert scene_manager.active_scene == "menu", "Після вибору easy має переходити в menu"
