class InputManager:
    def __init__(self):
        self._down_keys = []

    def key_status(self, key, down):
        if down:
            if key not in self._down_keys:
                self._down_keys.append(key)
        else:
            if key in self._down_keys:
                self._down_keys.remove(key)

    def get_key(self, key):
        return key in self._down_keys
