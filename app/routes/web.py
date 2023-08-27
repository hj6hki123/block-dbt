from flask import Blueprint, current_app, g
from app.middleware.authenticate import Authenticate

import app.controller.user as user_ctrl
import app.controller.oauth as oauth_ctrl
import app.controller.exp.public as public_ctrl
import app.controller.exp.parent as parent_ctrl
import app.controller.exp.private as private_ctrl


# class MyBlueprint(Blueprint):
#     def __init__(self, *args, middleware_decorator=None, **kwargs):
#         self.middleware_decorator = middleware_decorator
#         super().__init__(*args, **kwargs)
#
#     def add_url_rule(self, rule: str, endpoint: t.Optional[str] = None, view_func: t.Optional[ft.RouteCallable] = None,
#                      provide_automatic_options: t.Optional[bool] = None, **options: t.Any) -> None:
#         if self.middleware_decorator is None:
#             new_view_func = view_func
#         else:
#             new_view_func = self.middleware_decorator(view_func)
#         super().add_url_rule(rule, endpoint, new_view_func, provide_automatic_options, **options)


def register_before_request(app: Blueprint, middleware_func):
    empty_func = lambda: None
    return app.before_request(middleware_func(empty_func))


def init_blueprint():
    '''
    Blueprint(name, import_name, static_folder, static_url_path, template_folder, url_prefix)
    blueprint.add_url_rule(rule, endpoint, view_func, methods)
    '''
    # User Blueprint
    user = Blueprint('user', __name__, url_prefix='/user')
    user.add_url_rule('/sign_up', None, user_ctrl.sign_up, methods=['GET', 'POST'])
    user.add_url_rule('/login', None, user_ctrl.login, methods=['GET', 'POST'])
    user.add_url_rule('/logout', None, user_ctrl.logout, methods=['POST'])

    # OAuth Blueprint
    oauth = Blueprint('oauth', __name__, url_prefix='/oauth')
    oauth.add_url_rule('/', None, oauth_ctrl.index, methods=['GET'])
    oauth.add_url_rule('/store', None, oauth_ctrl.store, methods=['GET', 'POST'])
    oauth.add_url_rule('/authenticate', None, oauth_ctrl.authenticate, methods=['GET', 'POST'])

    # Exp Blueprint
    ## Public Blueprint
    public = Blueprint('public', __name__, url_prefix='/public')
    public.add_url_rule('/', None, public_ctrl.index, methods=['GET'])
    public.add_url_rule('/index', None, public_ctrl.index, methods=['GET'])
    public.add_url_rule('/show/<state>/<id>', None, public_ctrl.show, methods=['GET', 'POST'])

    ## Parent Blueprint
    parent = Blueprint('parent', __name__, url_prefix='/parent')
    parent.add_url_rule('/', None, parent_ctrl.index, methods=['GET'])
    parent.add_url_rule('/index', None, parent_ctrl.index, methods=['GET'])
    parent.add_url_rule('/build', None, parent_ctrl.build, methods=['GET', 'POST'])
    parent.add_url_rule('/build/update/<id>', None, parent_ctrl.update4build, methods=['GET', 'POST'])
    parent.add_url_rule('/build/auth/<id>', None, parent_ctrl.build2auth, methods=['GET'])
    parent.add_url_rule('/experiment/subject/<id>', None, parent_ctrl.exp2sub, methods=['GET'])
    parent.add_url_rule('/subject/object/<id>', None, parent_ctrl.obj4sub, methods=['GET', 'POST'])
    parent.add_url_rule('/subject/start/<id>', None, parent_ctrl.start4sub, methods=['GET', 'POST'])
    parent.add_url_rule('/running/object/<id>', None, parent_ctrl.obj4run, methods=['GET', 'POST'])
    parent.add_url_rule('/sign_up/<address>/<type>/<location>', None, parent_ctrl.sign_up, methods=['GET'])

    ## Private Blueprint
    private = Blueprint('private', __name__, url_prefix='/private')
    private.add_url_rule('/', None, private_ctrl.index, methods=['GET'])
    private.add_url_rule('/index', None, private_ctrl.index, methods=['GET'])
    private.add_url_rule('/show/<state>/<id>', None, private_ctrl.show, methods=['GET', 'POST'])
    private.add_url_rule('/running/scan/<id>', None, private_ctrl.scan4run, methods=['GET', 'POST'])
    private.add_url_rule('/running/<id>', None, private_ctrl.form4run, methods=['GET', 'POST'])
    private.add_url_rule('/consent/<id>', None, private_ctrl.consent, methods=['GET'])

    ## Exp Blueprint
    exp = Blueprint('exp', __name__, url_prefix='/exp')
    exp.register_blueprint(public)
    exp.register_blueprint(parent)
    exp.register_blueprint(private)

    register_before_request(oauth, Authenticate.user())
    register_before_request(exp, Authenticate.user())

    current_app.register_blueprint(user)
    current_app.register_blueprint(oauth)
    current_app.register_blueprint(exp)
