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
        menu_scene = MenuScene(scene_manager)
        scene_manager.add_scene("menu", menu_scene)

        assert "menu" in scene_manager.scenes, (
            "Сцена 'menu' має бути у словнику сцен"
        )

        scene_manager.set_scene("menu")
        assert scene_manager.active_scene == menu_scene, (
            "Активна сцена має бути menu_scene"
        )

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
        assert game.running is False, (
            "Після отримання події QUIT гра має встановити running=False"
        )


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
        fake_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100)
        )
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
            fake_event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, button=1, pos=(300, 300)
            )
            limited_ammo_scene.handle_events([fake_event])

        assert scene_manager.active_scene == score_scene, (
            "Після 10 кліків має перейти у сцену score"
        )

    def test_limited_time_scene_timer(self, scene_manager):
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)
        limited_time_scene = LimitedTimeGameModeScene(scene_manager)
        scene_manager.add_scene("time", limited_time_scene)
        scene_manager.set_scene("time")
        limited_time_scene.time_limit = 100
        limited_time_scene.start_time -= 200
        limited_time_scene.update()
        assert scene_manager.active_scene == score_scene, (
            "Після вичерпання часу має перейти у 'score'"
        )

    def test_settings_menu(self, scene_manager):
        DIFFICULTY_LEVEL[0] = 999
        settings_menu = SettingsMenu(scene_manager)
        scene_manager.add_scene("settings", settings_menu)
        menu_scene = MenuScene(scene_manager)
        scene_manager.add_scene("menu", menu_scene)
        scene_manager.set_scene("settings")
        fake_click = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=(430, 320)
        )
        settings_menu.handle_events([fake_click])
        assert DIFFICULTY_LEVEL[0] == 0, (
            "Після кліку по easy_mode_rect має встановитись DIFFICULTY_LEVEL=0"
        )
        assert scene_manager.active_scene == menu_scene, (
            "Після вибору easy має переходити в 'menu'"
        )


class TestsGun:
    @pytest.fixture
    def gun(self, mocker):
        mocker.patch(
            'pygame.image.load', return_value=pygame.Surface((100, 100))
        )
        mocker.patch('pygame.mixer.Sound')
        return Gun()

    def test_gun_init(self, gun):
        assert gun.gun_image is not None
        assert gun.shot_image is not None
        assert gun.shot_triggered is False

    def test_gun_draw_no_click(self, gun, mocker):
        mocker.patch('pygame.mouse.get_pos', return_value=(400, 400))
        mocker.patch('pygame.mouse.get_pressed', return_value=(0, 0, 0))
        self.screen = mocker.Mock()
        gun.draw(self.screen)
        assert not gun.shot_triggered

    def test_gun_draw_click_triggered(self, gun, mocker):
        mocker.patch('pygame.mouse.get_pos', return_value=(450, 300))
        mocker.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))
        gun.shot_triggered = False
        gun.draw(pygame.Surface((800, 600)))
        assert gun.shot_triggered is True


class TestsMenuScene:
    @pytest.fixture
    def menu_scene(self, mocker):
        mocker.patch(
            "pygame.image.load", return_value=pygame.Surface((100, 100))
        )
        scene_manager_mock = mocker.Mock()
        scene_manager_mock.scenes = {"time": mocker.Mock()}
        return MenuScene(scene_manager_mock)

    def test_handle_events_settings(self, menu_scene, mocker):
        mock_pos = (460 + 10, 59 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos
        )
        menu_scene.handle_events([event])
        menu_scene.scene_manager.set_scene.assert_called_once_with("settings")

    def test_handle_events_free_mode(self, menu_scene, mocker):
        mock_pos = (100 + 10, 345 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos
        )
        menu_scene.handle_events([event])
        menu_scene.scene_manager.set_scene.assert_called_once_with("game")

    def test_handle_events_limited_ammo(self, menu_scene, mocker):
        mock_pos = (100 + 10, 490 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos
        )
        menu_scene.handle_events([event])

        menu_scene.scene_manager.set_scene.assert_called_once_with("ammo")

    def test_handle_events_limited_time(self, menu_scene, mocker):
        mock_pos = (100 + 10, 635 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        mocker.patch('pygame.time.get_ticks', return_value=123456)

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos
        )
        menu_scene.handle_events([event])

        assert menu_scene.scene_manager.scenes["time"].start_time == 123456
        menu_scene.scene_manager.set_scene.assert_called_once_with("time")

    def test_handle_events_no_click(self, menu_scene, mocker):
        mock_pos = (0, 0)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=3, pos=mock_pos
        )
        menu_scene.handle_events([event])

        menu_scene.scene_manager.set_scene.assert_not_called()

    def test_draw(self, menu_scene, mocker):
        screen_mock = mocker.Mock()
        menu_scene.draw(screen_mock)
        screen_mock.blit.assert_called_once_with(menu_scene.menu_bg, (0, 0))


class TestsSettingsScene:
    @pytest.fixture
    def settings_scene(self, mocker):
        mocker.patch(
            'pygame.image.load', return_value=pygame.Surface((100, 100))
        )
        self.scene_manager_mock = mocker.Mock()
        return SettingsMenu(self.scene_manager_mock)

    def test_handle_events_easy(self, settings_scene):
        self.event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=(420, 400)
        )
        settings_scene.handle_events([self.event])
        assert DIFFICULTY_LEVEL[0] == 0
        assert settings_scene.difficulty == 0

    def test_handle_events_medium(self, settings_scene):
        self.event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=(420, 550)
        )
        settings_scene.handle_events([self.event])
        assert DIFFICULTY_LEVEL[0] == 1
        settings_scene.scene_manager.set_scene.assert_called_with("menu")

    def test_handle_events_hard(self, settings_scene):
        self.event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=(420, 620)
        )
        settings_scene.handle_events([self.event])
        assert DIFFICULTY_LEVEL[0] == 2
        settings_scene.scene_manager.set_scene.assert_called_with("menu")


class TestsFreeGameScene:
    @pytest.fixture
    def free_game(self, mocker):
        mocker.patch(
            'pygame.image.load', return_value=pygame.Surface((100, 100))
        )
        self.scene_manager_mock = mocker.Mock()
        self.scene_manager_mock.scenes = {
            "score": mocker.Mock(),
            "pause": mocker.Mock()
        }
        return GameScene(self.scene_manager_mock)

    def test_restart(self, free_game):
        free_game.score = 150
        free_game.hits_count = 3
        free_game.shots_count = 5
        free_game.ducks = [Duck(100, 100, 45)]

        free_game.restart()

        assert free_game.score == 0
        assert free_game.hits_count == 0
        assert free_game.shots_count == 0
        assert free_game.ducks == []

    def test_handle_events_click_restart(self, free_game, mocker):
        self.event_mock = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(700, 720))
        self.restart_mock = mocker.patch.object(free_game, 'restart')

        free_game.handle_events([self.event_mock])

        self.restart_mock.assert_called_once()

    def test_handle_events_click_pause(self, free_game, mocker):
        self.event_mock = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(700, 640))
        free_game.handle_events([self.event_mock])

        free_game.scene_manager.set_scene.assert_called_once_with("pause")
        assert free_game.scene_manager.scenes["pause"].previous_scene_name == (
            "game"
        )

    def test_handle_events_shoot_duck(self, free_game, mocker):
        self.duck_mock = mocker.Mock()
        self.duck_mock.check_collision.return_value = True
        self.duck_mock.get_score_value.return_value = 10

        free_game.ducks.append(self.duck_mock)

        self.event_mock = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(100, 100))

        free_game.handle_events([self.event_mock])

        assert free_game.score in {10, 35, 45}
        assert free_game.hits_count == 1
        assert free_game.shots_count == 1
        assert self.duck_mock not in free_game.ducks

    def test_go_to_score_scene(self, free_game):
        current_time_ms = pygame.time.get_ticks() - free_game.start_time
        current_time_sec = current_time_ms / 1000.0

        score_scene = free_game.scene_manager.scenes["score"]
        score_scene.set_stats(
            time_sec=current_time_sec,
            score=free_game.score,
            hits_count=free_game.hits_count,
            shots_count=free_game.shots_count
        )
        free_game.scene_manager.set_scene("score")

    def test_update_spawns_ducks(self, free_game, mocker):
        mocker.patch(
            'pygame.time.get_ticks',
            return_value=free_game.last_spawn_time + 2500,
        )
        mocker.patch('random.choice', return_value=True)
        mocker.patch('random.randint', return_value=100)

        self.initial_duck_count = len(free_game.ducks)
        free_game.update()

        assert len(free_game.ducks) == self.initial_duck_count + 1


class TestsLimitedTimeScene:
    @pytest.fixture
    def lim_time(self, mocker):
        mocker.patch(
            'pygame.image.load', return_value=pygame.Surface((100, 100))
        )
        scene_manager_mock = mocker.Mock()

        score_scene_mock = mocker.Mock()
        pause_scene_mock = mocker.Mock()

        scene_manager_mock.scenes = {
            "score": score_scene_mock,
            "pause": pause_scene_mock
        }

        scene = LimitedTimeGameModeScene(scene_manager_mock)
        scene.time_limit = 10000
        return scene

    def test_restart(self, lim_time):
        lim_time.score = 100
        lim_time.hits_count = 5
        lim_time.shots_count = 5
        lim_time.ducks = ['duck1']
        lim_time.restart()
        assert lim_time.score == 0
        assert lim_time.hits_count == 0
        assert len(lim_time.ducks) == 0

    def test_handle_events_click_restart(self, lim_time, mocker):
        event = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(700, 720))
        mocker.patch.object(lim_time, 'restart')
        lim_time.handle_events([event])
        lim_time.restart.assert_called_once()

    def test_go_to_score_scene(self, lim_time):
        lim_time.score = 200
        lim_time.hits_count = 20
        lim_time.shots_count = 25
        lim_time.go_to_score_scene(flag=True)

        lim_time.scene_manager.set_scene.assert_called_once_with("score")
        lim_time.scene_manager.scenes["score"].set_stats.assert_called_once()


class TestsLimitedAmmoScene:
    @pytest.fixture
    def lim_ammo(self, mocker):
        mocker.patch(
            'pygame.image.load', return_value=pygame.Surface((100, 100))
        )
        scene_manager_mock = mocker.Mock()
        scene_manager_mock.scenes = {
            "score": mocker.Mock(),
            "pause": mocker.Mock()
        }
        return LimitedAmmoGameModeScene(scene_manager_mock)

    def test_restart(self, lim_ammo):
        lim_ammo.score = 50
        lim_ammo.ammo = 0
        lim_ammo.hits_count = 5
        lim_ammo.shots_count = 5
        lim_ammo.ducks = [1, 2, 3]

        lim_ammo.restart()

        assert lim_ammo.score == 0
        assert lim_ammo.hits_count == 0
        assert lim_ammo.ammo == 10
        assert lim_ammo.ducks == []

    def test_handle_events_ammo_decrease(self, lim_ammo, mocker):
        event = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(0, 0))
        lim_ammo.ammo = 10

        lim_ammo.handle_events([event])

        assert lim_ammo.ammo == 9
        assert lim_ammo.shots_count == 1

    def test_go_to_score_scene(self, lim_ammo):
        lim_ammo.score = 100
        lim_ammo.hits_count = 10
        lim_ammo.shots_count = 20

        lim_ammo.go_to_score_scene()

        lim_ammo.scene_manager.scenes["score"].set_stats.assert_called_once()
        lim_ammo.scene_manager.set_scene.assert_called_once_with("score")


@pytest.fixture
def prepared_scenes(scene_manager):
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
        game_scene = GameScene(scene_manager)
        scene_manager.add_scene("game", game_scene)

        pause_scene = PauseScene(scene_manager)
        pause_scene.previous_scene_name = "game"
        scene_manager.add_scene("pause", pause_scene)

        scene_manager.set_scene("pause")

        game_scene.pause_start = pygame.time.get_ticks() - 1000
        initial_start_time = 5000
        game_scene.start_time = initial_start_time

        click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            button=1,
            pos=(430, 430)
        )
        pause_scene.handle_events([click_event])

        assert scene_manager.active_scene == game_scene, (
            "Після кліку на return_rect маємо повернутися у 'game'."
        )

        assert game_scene.start_time > initial_start_time, (
            "При виході з паузи start_time має збільшитися на час паузи."
        )

    def test_score_button(self, scene_manager):
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)

        pause_scene = PauseScene(scene_manager)
        scene_manager.add_scene("pause", pause_scene)

        scene_manager.set_scene("pause")

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
        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)

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

        game_scene.score = 100
        ammo_scene.score = 200
        time_scene.score = 300

        score_scene = ScoreScene(scene_manager)
        scene_manager.add_scene("score", score_scene)
        scene_manager.set_scene("score")

        click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            button=1,
            pos=(300, 560)
        )
        score_scene.handle_events([click_event])

        assert scene_manager.active_scene == menu_scene, (
            "Після кліку по main_menu_rect має переходити в 'menu'."
        )
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
        assert duck.x != initial_x or duck.y != initial_y, (
            "Качка має змінити свої координати після update()"
        )

    @pytest.mark.parametrize(
        "difficulty, direction, expected_speed_range, "
        "expected_size_range, speed_sign",
        [
            (0, 'left',  (3, 6),  (90, 120),  1),
            (0, 'right', (3, 6),  (90, 120), -1),
            (1, 'left',  (6, 9),  (60, 90),   1),
            (1, 'right', (6, 9),  (60, 90),  -1),
            (2, 'left',  (9, 13), (30, 60),   1),
            (2, 'right', (9, 13), (30, 60),  -1),
        ]
    )
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
        assert min_spd <= abs(speed) <= max_spd, (
            f"Speed {speed} має бути в діапазоні [{min_spd}, {max_spd}]"
        )
        assert speed_sign == (1 if speed > 0 else -1), (
            f"Speed sign має відповідати напрямку {direction}"
        )

        size = duck.size
        min_sz, max_sz = expected_size_range
        assert min_sz <= size <= max_sz, f"Розмір поза [{min_sz}, {max_sz}]"

    @pytest.mark.parametrize("difficulty", [0, 1, 2])
    def test_get_score_value(self, reset_difficulty, difficulty):
        random.seed(101)
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
        assert duck.check_collision(r_intersect), "Має перетнутися з качкою."
        r_no_intersect = pygame.Rect(500, 500, 30, 30)
        assert not duck.check_collision(r_no_intersect), "Не має перетинатися."
