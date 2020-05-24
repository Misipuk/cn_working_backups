from typing import Dict, List, Optional, Union


class User:
    id: int
    login: str
    # TODO: keep hashed?
    password: str

    def __init__(self, login: str = '', password: str = ''):
        self.id = None
        self.login = login
        self.password = password

    def copy(self):
        u = User()
        u.id = self.id
        u.login = self.login
        u.password = self.password
        return u


class Users:
    # user_id -> User
    _users: Dict[int, User]
    # login -> user_id
    _users_login: Dict[str, int]
    _all_users: List[User]

    def __init__(self):
        self._users = {}
        self._users_login = {}
        self._all_users = []

    def get(self, uid: int) -> Optional[User]:
        uu = self._users.get(uid)
        return Users._copy_if_none(uu)

    def get_by_login(self, login: str) -> Optional[User]:
        uid = self._users_login.get(login)
        return self.get(uid) if uid is not None else None

    def put(self, user: User) -> int:
        if user.id is None:
            if len(self._all_users) != 0:
                user.id = self._all_users[-1].id + 1
            else:
                user.id = 1
        if self._users_login.get(user.login) is None:
            # To dict
            self._users[user.id] = user
            self._users_login[user.login] = user.id
            # To_list
            self._all_users.append(user)
        else:
            return -1

        return user.id

    @staticmethod
    def _copy_if_none(user):
        if user is not None:
            return user.copy()
        else:
            return None
