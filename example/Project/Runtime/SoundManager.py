import winsound
import base64
import threading

# BUGGY
class SoundManager:
    def __init__(self, data):
        self._sounds = {}
        for k in data.keys():
            self._sounds[k] = base64.b64decode(data[k])

    def play(self, name):
        if name in self._sounds.keys():
            t = threading.Thread(
                target=winsound.PlaySound,
                args=(self._sounds[name], winsound.SND_MEMORY)
            )
            t.setDaemon(True)
            t.start()
