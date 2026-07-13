class UserNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class FollowUserConflictError(Exception):
    pass


class FollowUserError(Exception):
    pass


class FollowNotFoundError(Exception):
    pass
