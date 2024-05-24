from .session import Session

DEFAULT_SESSION = None


def setup_default_session(**kwargs):
    """
    Set up the default session for the module.
    """
    global DEFAULT_SESSION
    DEFAULT_SESSION = Session(**kwargs)


def _get_default_session():
    """
    Get the default session for the module.
    """
    if DEFAULT_SESSION is None:
        setup_default_session()

    return DEFAULT_SESSION


def resource(*args, **kwargs):
    """
    Create a resource using the default session.
    """
    return _get_default_session().resource(*args, **kwargs)