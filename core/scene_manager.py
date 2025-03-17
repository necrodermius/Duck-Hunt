class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        self.active_scene = self.scenes.get(name)

    def update(self, events):
        if self.active_scene:
            self.active_scene.handle_events(events)
            self.active_scene.update()

    def draw(self, screen):
        if self.active_scene:
            self.active_scene.draw(screen)
