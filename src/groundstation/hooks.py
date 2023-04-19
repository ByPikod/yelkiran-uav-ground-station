class Hooks:

    __hooks: dict

    def __init__(self):
        self.__hooks = {}

    def add(self, event: str, identifier: str, callback) -> None:
        """
        Add a hook.
        :param event: Event identifier.
        :param identifier: Hook identifier per function so you can remove later.
        :param callback: Function to call back.
        """

        if not callable(callback):
            raise Exception("Callback must be a callable.")

        hooks = self.__hooks[event]
        if hooks is None:
            hooks = {}
            self.__hooks[event] = hooks

        hooks[identifier] = callback

    def remove(self, event: str, identifier: str) -> bool:
        hooks = self.__hooks[event]

        if hooks is None:
            return False

        callback = hooks[identifier]

        if callback is None:
            return False

        hooks.remove(identifier)

    def run(self, event: str, *args, **kwargs) -> any:
        """
        Calls all hooks associated with the given event until one returns something other than None and
        then returns that data.
        If no hook returns any data, it will return None.

        :param event: The event to call hooks for.
        :param args: The arguments to be passed to the hooks
        :param kwargs: The arguments to be passed to the hooks
        :return:
        """

        events = self.__hooks[event]
        if events is None:
            return None

        for k, v in events:
            if not callable(v):
                continue
            res = v()
            if res is not None:
                return res
