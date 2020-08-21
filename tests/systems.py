from stup.system import System


class UpdateSystem(System):
    updates = 0

    def update(self, deltatime):
        self.updates += 1
