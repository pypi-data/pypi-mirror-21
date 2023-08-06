import threading
cimport pypurple

class MiniClient(threading.Thread):

    core = None

    def __init__(self, *args):
        if not MiniClient.core:
            core = pypurple.Purple(args)

        self.core = MiniClient.core
        s

    def run(self):
        pass

    def createAccount(self, username, protocol):

        def callback(self, username, protocol):
            self.account = pypurple.Account("andrey.petrov@gmail.com", pypurple.Protocol('prpl-jabber'), self.core)
        core.add_event((callback, username, protocol))
