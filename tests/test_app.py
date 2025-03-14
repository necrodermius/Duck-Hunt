import pytest
import pygame
import random
import os

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

class TestCore:
    def test_scene_manager_add_and_set_scene(self, scene_manager):
        screen = pygame.display.set_mode((900, 800))
        menu_scene = MenuScene(scene_manager)
        scene_manager.add_scene("menu", menu_scene)

        assert "menu" in scene_manager.scenes, "Сцена 'menu' має бути у словнику сцен"

        scene_manager.set_scene("menu")
        assert scene_manager.active_scene == menu_scene, "Активна сцена має бути menu_scene"

    def test_update_scene(self, mocker):
        manager = SceneManager()
        fake_scene = mocker.Mock()
        manager.add_scene("fake", fake_scene)
        manager.set_scene("fake")
        manager.update([])
        fake_scene.handle_events.assert_called_once()
        fake_scene.update.assert_called_once()

    def test_draw_scene(self, mocker):
        manager = SceneManager()
        fake_scene = mocker.Mock()
        screen_mock = mocker.Mock()
        manager.add_scene("fake", fake_scene)
        manager.set_scene("fake")
        manager.draw(screen=screen_mock)
        fake_scene.draw.assert_called_once_with(screen_mock)

    def test_game_run_quit(self, init_pygame, monkeypatch):
        game = Game()

        def mock_event_get():
            return [pygame.event.Event(pygame.QUIT, {})]
        monkeypatch.setattr(pygame.event, 'get', mock_event_get)
        game.run()
        assert game.running is False, "Після отримання події QUIT гра має встановити running=False"

@pytest.fixture()
def scene_manager():
    return SceneManager()

@pytest.fixture(scope="class", autouse=True)
def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

class TestScenes:
    def test_game_scene_basic(self, scene_manager):
        game_scene = GameScene(scene_manager)
        fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100))
        game_scene.handle_events([fake_event])
        game_scene.update()
        test_surface = pygame.Surface((800, 600))
        game_scene.draw(test_surface)

    def test_limited_ammo_scene_end(self, scene_manager):
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)
        limited_ammo_scene = LimitedAmmoGameModeScene(scene_manager)
        scene_manager.add_scene("ammo", limited_ammo_scene)
        scene_manager.set_scene("ammo")
        for _ in range(10):
            fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(300, 300))
            limited_ammo_scene.handle_events([fake_event])

        assert (scene_manager.active_scene == score_scene), "Після 10 кліків має перейти у сцену score"

    def test_limited_time_scene_timer(self, scene_manager):
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)
        limited_time_scene = LimitedTimeGameModeScene(scene_manager)
        scene_manager.add_scene("time", limited_time_scene)
        scene_manager.set_scene("time")
        limited_time_scene.time_limit = 100
        limited_time_scene.start_time -= 200
        limited_time_scene.update()
        assert (scene_manager.active_scene == score_scene), "Після вичерпання часу має перейти у 'score'"

    def test_settings_menu(self, scene_manager):
        DIFFICULTY_LEVEL[0] = 999
        settings_menu = SettingsMenu(scene_manager)
        scene_manager.add_scene("settings", settings_menu)
        menu_scene = MenuScene(scene_manager)
        scene_manager.add_scene("menu", menu_scene)
        scene_manager.set_scene("settings")
        fake_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(430, 320))
        settings_menu.handle_events([fake_click])
        assert DIFFICULTY_LEVEL[0] == 0, ("Після кліку по easy_mode_rect має встановитись DIFFICULTY_LEVEL=0")
        assert (scene_manager.active_scene == menu_scene), "Після вибору easy має переходити в 'menu'"


@pytest.fixture
def scene_manager():
    """Створює "чистий" SceneManager для кожного тесту."""
    return SceneManager()


@pytest.fixture
def prepared_scenes(scene_manager):
    """
    Створює й додає в SceneManager базові сцени:
    - 'game' (free mode)
    - 'ammo' (limited ammo)
    - 'time' (limited time)
    - 'menu' (MenuScene)

    Повертає кортеж (game_scene, ammo_scene, time_scene, menu_scene).
    """
    game_scene = GameScene(scene_manager)
    ammo_scene = LimitedAmmoGameModeScene(scene_manager)
    time_scene = LimitedTimeGameModeScene(scene_manager)
    menu_scene = MenuScene(scene_manager)

    scene_manager.add_scene("game", game_scene)
    scene_manager.add_scene("ammo", ammo_scene)
    scene_manager.add_scene("time", time_scene)
    scene_manager.add_scene("menu", menu_scene)

    return game_scene, ammo_scene, time_scene, menu_scene


class TestPauseScene:
    def test_return_button(self, scene_manager):
        """
        Перевіряємо, що клік по return_rect викликає resume_previous_scene(),
        переключаємося на попередню сцену,
        і якщо був встановлений pause_start - воно зсуває start_time.
        """
        # Додаємо "game" як попередню сцену:
        game_scene = GameScene(scene_manager)
        scene_manager.add_scene("game", game_scene)

        # Створюємо PauseScene:
        pause_scene = PauseScene(scene_manager)
        pause_scene.previous_scene_name = "game"  # Вказуємо, що повертаємося у "game"
        scene_manager.add_scene("pause", pause_scene)

        # Робимо "pause" активною
        scene_manager.set_scene("pause")

        # Імітуємо, що у game_scene був pause_start і start_time
        game_scene.pause_start = pygame.time.get_ticks() - 1000  # на секунду раніше
        initial_start_time = 5000
        game_scene.start_time = initial_start_time

        # Координати всередині return_rect = (410,417,390,73), припустимо (420,420)
        click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            button=1,
            pos=(430, 430)
        )
        pause_scene.handle_events([click_event])

        # Перевіряємо, що сцена тепер "game"
        assert scene_manager.active_scene == game_scene, (
            "Після кліку на return_rect маємо повернутися у 'game'."
        )

        # Перевіряємо, що start_time збільшився
        # тобто що пауза дійсно додала 1 секунду
        assert game_scene.start_time > initial_start_time, (
            "При відновленні з паузи start_time має зрости на період, поки сцена була на паузі."
        )

    def test_score_button(self, scene_manager):
        """
        Перевірка, що клік по score_menu_rect -> перехід у 'score'.
        """
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)

        pause_scene = PauseScene(scene_manager)
        scene_manager.add_scene("pause", pause_scene)

        # Робимо активною "pause"
        scene_manager.set_scene("pause")

        # Клік у score_menu_rect = (510,560,395,70), беремо точку (520,570)
        click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            button=1,
            pos=(520, 570)
        )
        pause_scene.handle_events([click_event])

        assert scene_manager.active_scene == score_scene, (
            "Після кліку по score_menu_rect має встановитись сцена 'score'."
        )


class TestScoreScene:
    def test_set_stats(self, scene_manager):
        """
        Перевірка, що set_stats() зберігає передані значення у відповідних полях.
        """
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)

        # Передаємо дані
        time_sec = 123.45
        score = 999
        hits = 10
        shots = 20

        score_scene.set_stats(time_sec, score, hits, shots)

        assert score_scene.final_time == time_sec
        assert score_scene.score == score
        assert score_scene.hits_count == hits
        assert score_scene.shots_count == shots

    def test_click_main_menu_rect(self, scene_manager, prepared_scenes):
        """
        Перевіряємо, що при кліку по main_menu_rect виконується:
        - restart() у 'game', 'ammo', 'time'
        - перехід у 'menu'
        """
        (game_scene, ammo_scene, time_scene, menu_scene) = prepared_scenes

        # Переконаємося, що в game_scene / ammo_scene / time_scene є методи restart()
        # (вони там реалізовані, і обнуляють певні дані)
        # Для тесту можемо перевірити, що вони працюють чи були викликані.
        # Проте наразі просто перевіримо стан до/після.

        # Налаштуємо якісь не нульові дані, щоб потім перевірити, що restart() їх обнуляє.
        game_scene.score = 100
        ammo_scene.score = 200
        time_scene.score = 300

        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)
        scene_manager.set_scene("score")

        # Клік у main_menu_rect = (225, 552, 420, 95). Припустимо (300, 560).
        click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            button=1,
            pos=(300, 560)
        )
        score_scene.handle_events([click_event])

        # Перевіряємо, що active_scene тепер menu_scene
        assert scene_manager.active_scene == menu_scene, (
            "Після кліку по main_menu_rect має переходити в 'menu'."
        )

        # Перевіряємо, що restart() подіяв - (score має бути обнулений)
        assert game_scene.score == 0, (
            "Очікуємо, що game_scene.restart() обнулило score."
        )
        assert ammo_scene.score == 0, (
            "Очікуємо, що ammo_scene.restart() обнулило score."
        )
        assert time_scene.score == 0, (
            "Очікуємо, що time_scene.restart() обнулило score."
        )


@pytest.fixture
def reset_difficulty():
    original = DIFFICULTY_LEVEL[0]
    yield
    DIFFICULTY_LEVEL[0] = original

class TestDuck:
    def test_duck_update(self):
        duck = Duck(x=0, y=100, move_angle=0, direction="left")
        initial_x = duck.x
        initial_y = duck.y
        duck.update()
        assert duck.x != initial_x or duck.y != initial_y, "Качка має змінити свої координати після update()"

    @pytest.mark.parametrize("difficulty, direction, expected_speed_range, expected_size_range, speed_sign", [
        (0, 'left',  (3, 6),  (90, 120),  1),
        (0, 'right', (3, 6),  (90, 120), -1),
        (1, 'left',  (6, 9),  (60, 90),   1),
        (1, 'right', (6, 9),  (60, 90),  -1),
        (2, 'left',  (9, 13), (30, 60),   1),
        (2, 'right', (9, 13), (30, 60),  -1),
    ])
    def test_duck_init_speed_size(
        self,
        reset_difficulty,
        difficulty,
        direction,
        expected_speed_range,
        expected_size_range,
        speed_sign
    ):
        random.seed(42)

        DIFFICULTY_LEVEL[0] = difficulty

        x, y = 100, 100
        move_angle = 0
        duck = Duck(x, y, move_angle, direction=direction)

        speed = duck.speed
        min_spd, max_spd = expected_speed_range
        assert min_spd <= abs(speed) <= max_spd, f"Speed {speed} має бути в діапазоні [{min_spd}, {max_spd}]"
        assert speed_sign == (1 if speed > 0 else -1), f"Speed sign має відповідати напрямку {direction}"

        size = duck.size
        min_sz, max_sz = expected_size_range
        assert min_sz <= size <= max_sz, f"Size {size} має бути в діапазоні [{min_sz}, {max_sz}]"

    @pytest.mark.parametrize("difficulty", [0, 1, 2])
    def test_get_score_value(self, reset_difficulty, difficulty):
        random.seed(101)  # для стабільності
        DIFFICULTY_LEVEL[0] = difficulty

        duck = Duck(x=0, y=0, move_angle=10, direction="left")
        value = duck.get_score_value()
        s = abs(duck.speed)
        si = duck.size
        expected = int(1 / si + 5 * s)
        assert value == expected, (
            f"get_score_value() має відповідати формулі 1/size + 5*speed.\n"
            f"Очікували {expected}, отримали {value}."
        )

    def test_collision(self):
        DIFFICULTY_LEVEL[0] = 0
        duck = Duck(x=50, y=50, move_angle=0, direction='left')
        r_intersect = pygame.Rect(55, 55, 20, 20)
        assert duck.check_collision(r_intersect), "Повинні перетнутися з качкою."
        r_no_intersect = pygame.Rect(500, 500, 30, 30)
        assert not duck.check_collision(r_no_intersect), "Не мають перетинатися."