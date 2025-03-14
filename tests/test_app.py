import pytest
import pygame

from core.settings import DIFFICULTY_LEVEL

from core.scene_manager import SceneManager
from scenes.free_gamemode_scene import GameScene
from scenes.limited_ammo_gamemode_scene import LimitedAmmoGameModeScene
from scenes.limited_time_gamemode_scene import LimitedTimeGameModeScene
from scenes.menu_scene import MenuScene
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

class TestsGun:
    @pytest.fixture
    def gun(self, mocker):
        mocker.patch('pygame.image.load', return_value=pygame.Surface((100, 100)))
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
        mocker.patch("pygame.image.load", return_value=pygame.Surface((100, 100)))
        scene_manager_mock = mocker.Mock()
        scene_manager_mock.scenes = {"time": mocker.Mock()}
        return MenuScene(scene_manager_mock)
    
    def test_handle_events_settings(self, menu_scene, mocker):
        mock_pos = (460 + 10, 59 + 10)  
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos)
        menu_scene.handle_events([event])
        
        menu_scene.scene_manager.set_scene.assert_called_once_with("settings")

    def test_handle_events_free_mode(self, menu_scene, mocker):
        mock_pos = (100 + 10, 345 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos)
        menu_scene.handle_events([event])
        
        menu_scene.scene_manager.set_scene.assert_called_once_with("game")

    def test_handle_events_limited_ammo(self, menu_scene, mocker):
        mock_pos = (100 + 10, 490 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos)
        menu_scene.handle_events([event])
        
        menu_scene.scene_manager.set_scene.assert_called_once_with("ammo")

    def test_handle_events_limited_time(self, menu_scene, mocker):
        mock_pos = (100 + 10, 635 + 10)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)
        
        mocker.patch('pygame.time.get_ticks', return_value=123456)

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=mock_pos)
        menu_scene.handle_events([event])

        assert menu_scene.scene_manager.scenes["time"].start_time == 123456
        
        menu_scene.scene_manager.set_scene.assert_called_once_with("time")

    def test_handle_events_no_click(self, menu_scene, mocker):
        mock_pos = (0, 0)
        mocker.patch('pygame.mouse.get_pos', return_value=mock_pos)

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=mock_pos)
        menu_scene.handle_events([event])

        menu_scene.scene_manager.set_scene.assert_not_called()

    def test_draw(self, menu_scene, mocker):
        screen_mock = mocker.Mock()
        menu_scene.draw(screen_mock)
        screen_mock.blit.assert_called_once_with(menu_scene.menu_bg, (0, 0))

class TestsSettingsScene:
    @pytest.fixture
    def settings_scene(self, mocker):
        mocker.patch('pygame.image.load', return_value=pygame.Surface((100, 100)))
        self.scene_manager_mock = mocker.Mock()
        return SettingsMenu(self.scene_manager_mock)

    def test_handle_events_easy(self, settings_scene):
        self.event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(420, 400))
        settings_scene.handle_events([self.event])
        assert DIFFICULTY_LEVEL[0] == 0
        assert settings_scene.difficulty == 0

    def test_handle_events_medium(self, settings_scene):
        self.event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(420, 550))
        settings_scene.handle_events([self.event])
        assert DIFFICULTY_LEVEL[0] == 1
        settings_scene.scene_manager.set_scene.assert_called_with("menu")

    def test_handle_events_hard(self, settings_scene):
        self.event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(420, 620))
        settings_scene.handle_events([self.event])
        assert DIFFICULTY_LEVEL[0] == 2
        settings_scene.scene_manager.set_scene.assert_called_with("menu")

class TestsFreeGameScene:
    @pytest.fixture
    def free_game_scene(self, mocker):
        mocker.patch('pygame.image.load', return_value=pygame.Surface((100, 100)))
        
        self.scene_manager_mock = mocker.Mock()
        self.scene_manager_mock.scenes = {
            "score": mocker.Mock(),
            "pause": mocker.Mock()
        }
        
        return GameScene(self.scene_manager_mock)

    def test_restart(self, free_game_scene):
        free_game_scene.score = 150
        free_game_scene.hits_count = 3
        free_game_scene.shots_count = 5
        free_game_scene.ducks = [Duck(100, 100, 45)]

        free_game_scene.restart()

        assert free_game_scene.score == 0
        assert free_game_scene.hits_count == 0
        assert free_game_scene.shots_count == 0
        assert free_game_scene.ducks == []

    def test_handle_events_click_restart(self, free_game_scene, mocker):
        self.event_mock = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(700, 720))
        self.restart_mock = mocker.patch.object(free_game_scene, 'restart')

        free_game_scene.handle_events([self.event_mock])

        self.restart_mock.assert_called_once()

    def test_handle_events_click_pause(self, free_game_scene, mocker):
        self.event_mock = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(700, 640))
        
        free_game_scene.handle_events([self.event_mock])

        free_game_scene.scene_manager.set_scene.assert_called_once_with("pause")
        assert free_game_scene.scene_manager.scenes["pause"].previous_scene_name == "game"

    def test_handle_events_shoot_duck(self, free_game_scene, mocker):
        self.duck_mock = mocker.Mock()
        self.duck_mock.check_collision.return_value = True
        self.duck_mock.get_score_value.return_value = 10

        free_game_scene.ducks.append(self.duck_mock)
        
        self.event_mock = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(100, 100))
        
        free_game_scene.handle_events([self.event_mock])

        assert free_game_scene.score == 10 or free_game_scene.score == 35 or free_game_scene.score == 45  # в зависимости от get_score_value()
        assert free_game_scene.hits_count == 1
        assert free_game_scene.shots_count == 1
        assert self.duck_mock not in free_game_scene.ducks

    def test_go_to_score_scene(self, free_game_scene):
        current_time_ms = pygame.time.get_ticks() - free_game_scene.start_time
        current_time_sec = current_time_ms / 1000.0

        score_scene = free_game_scene.scene_manager.scenes["score"]
        score_scene.set_stats(
            time_sec=current_time_sec,
            score=free_game_scene.score,
            hits_count=free_game_scene.hits_count,
            shots_count=free_game_scene.shots_count
        )
        free_game_scene.scene_manager.set_scene("score")

    def test_update_spawns_ducks(self, free_game_scene, mocker):
        mocker.patch('pygame.time.get_ticks', return_value=free_game_scene.last_spawn_time + 2500)
        mocker.patch('random.choice', return_value=True)
        mocker.patch('random.randint', return_value=100)

        self.initial_duck_count = len(free_game_scene.ducks)
        free_game_scene.update()

        assert len(free_game_scene.ducks) == self.initial_duck_count + 1

class TestsLimitedTimeScene:
    @pytest.fixture
    def limited_time_scene(self, mocker):
        mocker.patch('pygame.image.load', return_value=pygame.Surface((100, 100)))
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

    def test_restart(self, limited_time_scene):
        limited_time_scene.score = 100
        limited_time_scene.hits_count = 5
        limited_time_scene.shots_count = 5
        limited_time_scene.ducks = ['duck1']
        limited_time_scene.restart()
        assert limited_time_scene.score == 0
        assert limited_time_scene.hits_count == 0
        assert len(limited_time_scene.ducks) == 0

    def test_handle_events_click_restart(self, limited_time_scene, mocker):
        event = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(700, 720))
        mocker.patch.object(limited_time_scene, 'restart')
        limited_time_scene.handle_events([event])
        limited_time_scene.restart.assert_called_once()

    def test_go_to_score_scene(self, limited_time_scene):
        limited_time_scene.score = 200
        limited_time_scene.hits_count = 20
        limited_time_scene.shots_count = 25
        limited_time_scene.go_to_score_scene(flag=True)

        limited_time_scene.scene_manager.set_scene.assert_called_once_with("score")
        limited_time_scene.scene_manager.scenes["score"].set_stats.assert_called_once()

class TestsLimitedAmmoScene:
    @pytest.fixture
    def limited_ammo_scene(self, mocker):
        mocker.patch('pygame.image.load', return_value=pygame.Surface((100, 100)))
        scene_manager_mock = mocker.Mock()
        scene_manager_mock.scenes = {
            "score": mocker.Mock(),
            "pause": mocker.Mock()
        }
        return LimitedAmmoGameModeScene(scene_manager_mock)

    def test_restart(self, limited_ammo_scene):
        limited_ammo_scene.score = 50
        limited_ammo_scene.ammo = 0
        limited_ammo_scene.hits_count = 5
        limited_ammo_scene.shots_count = 5
        limited_ammo_scene.ducks = [1,2,3]

        limited_ammo_scene.restart()

        assert limited_ammo_scene.score == 0
        assert limited_ammo_scene.hits_count == 0
        assert limited_ammo_scene.ammo == 10
        assert limited_ammo_scene.ducks == []

    def test_handle_events_ammo_decrease(self, limited_ammo_scene, mocker):
        event = mocker.Mock(type=pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch('pygame.mouse.get_pos', return_value=(0, 0))
        limited_ammo_scene.ammo = 10

        limited_ammo_scene.handle_events([event])

        assert limited_ammo_scene.ammo == 9
        assert limited_ammo_scene.shots_count == 1

    def test_go_to_score_scene(self, limited_ammo_scene):
        limited_ammo_scene.score = 100
        limited_ammo_scene.hits_count = 10
        limited_ammo_scene.shots_count = 20

        limited_ammo_scene.go_to_score_scene()

        limited_ammo_scene.scene_manager.scenes["score"].set_stats.assert_called_once()
        limited_ammo_scene.scene_manager.set_scene.assert_called_once_with("score")
