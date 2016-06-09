from google.appengine.api import users
import logging



def require_user(controller):
    """
    Requires that a user is logged in
    """
    if not controller.user:
        return (False, "require_user")
    return True


def require_admin(controller):
    """
    Requires that a user is logged in and that the user is and administrator on the App Engine Application
    """
    try:
        admin_user = controller.session["administrator_name"]
        if admin_user is not None:
            return True
    except KeyError:
        pass
    return (False, "require_admin")


def predicate_chain(predicate, chain):
    """
    Returns the result of chain if predicate returns True, otherwise returns True.
    """

    def inner(*args, **kwargs):
        predicate_curried = predicate(*args, **kwargs)

        def inner_inner(controller):
            if predicate_curried(controller):
                return chain(controller)
            return True

        return inner_inner

    return inner


def prefix_predicate(prefix):
    prefix = prefix if isinstance(prefix, (list, tuple)) else (prefix,)

    def inner(controller):
        if controller.route.prefix in prefix:
            return True
        return False
    return inner


def action_predicate(action):
    action = action if isinstance(action, (list, tuple)) else (action,)

    def inner(controller):
        if controller.route.action in action:
            return True
        return False
    return inner


def route_predicate(route):
    route = route if isinstance(route, (list, tuple)) else (route,)

    def inner(controller):
        route_name = controller.route.name.split(":")[0]
        if route_name in route:
            return True
        return False
    return inner


require_user_for_prefix = predicate_chain(prefix_predicate, require_user)
require_user_for_action = predicate_chain(action_predicate, require_user)
require_user_for_route = predicate_chain(route_predicate, require_user)

require_admin_for_prefix = predicate_chain(prefix_predicate, require_admin)
require_admin_for_action = predicate_chain(action_predicate, require_admin)
require_admin_for_route = predicate_chain(route_predicate, require_admin)

