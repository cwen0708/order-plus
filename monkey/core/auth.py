from google.appengine.api import users
import logging


def require_user(controller):
    """
    Requires that a user is logged in
    """
    if not controller.user:
        return False, "require_user"
    return True


def require_admin(controller):
    """
    Requires that a user is logged in and that the user is and administrator on the App Engine Application
    """
    if "administrator_key" not in controller.session:
        return False, "require_admin"
    admin_user = controller.session["administrator_key"].get()
    if admin_user is None:
        return False, "require_admin"
    if admin_user.role is None:
        return False, "require_admin"
    role = admin_user.role.get()
    if role is None:
        return False, "require_admin"
    controller.administrator = admin_user
    controller.administrator_level = role.level
    controller.prohibited_actions = str(role.prohibited_actions).split(",")
    controller.context["administrator_level"] = controller.administrator_level
    controller.context["administrator_key"] = admin_user.key
    if controller.route.name in controller.prohibited_actions:
        return controller.abort(403)
    return True


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

