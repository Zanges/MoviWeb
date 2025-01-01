from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    def __init__(self):
        self._current_user_id = None

    def set_current_user_id(self, user_id: int) -> None:
        """ Set the current user """
        self._current_user_id = user_id

    def get_current_user_id(self) -> int:
        """ Get the current user """
        return self._current_user_id

    @abstractmethod
    def get_current_user_name(self) -> str:
        """ Get the current user's name """
        pass