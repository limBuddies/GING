import os
import Runtime.DebugLoader

if __name__ == '__main__':
    project = os.path.split(os.path.realpath(__file__))[0]
    Runtime.DebugLoader.load(project)
