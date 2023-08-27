from json import loads as json_loads
import asyncio

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from app.config.exception import exception_code
from app.config.endpoint import endpoint
from app.model.exp import Exp
from app.model.form import Form


def index():
    if request.method == 'GET':
        title = '實驗管理'
        return render_template('./exp/parent/index.html', **locals())
    abort(404)


def build():
    if request.method == 'GET':
        title = '新增實驗'
        return render_template('./exp/parent/build.html', **locals())
    elif request.method == 'POST':
        try:
            form_data = request.values.to_dict()
            exp = Exp.store(form_data)
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('新增成功', category='success-toast')
            return redirect(url_for(endpoint.exp.parent.index))


def update4build(id):
    if request.method == 'GET':
        title = '編輯問卷'
        return render_template('./exp/parent/build-form.html', **locals())
    elif request.method == 'POST':
        try:
            form_data = request.values.to_dict()
            multiple_choice = json_loads(form_data['MCTable'])
            short_answer = json_loads(form_data['SATable'])
            # for _, value in enumerate(multiple_choice):
            #     data = dict(address=id, content=value['multipleChoice'], value=value['maxScore'])
            #     Form.store_mc(data)
            # for _, value in enumerate(short_answer):
            #     data = dict(address=id, content=value['shortAnswer'])
            #     Form.store_sa(data)
            results = asyncio.run(Form.store_mc_and_sa(id, multiple_choice, short_answer))
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('新增成功', category='success-toast')
            return redirect(url_for(endpoint.exp.parent.index))


def build2auth(id):
    if request.method == 'GET':
        data = dict(address=id)
        try:
            Form.confirm(data)
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('成功', category='success')
            return redirect(url_for(endpoint.exp.parent.index))


def exp2sub(id):
    if request.method == 'GET':
        data = dict(address=id)
        try:
            Exp.sign_sub(data)
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('成功', category='success')
            return redirect(url_for(endpoint.exp.parent.index))


def obj4sub(id):
    if request.method == 'GET':
        title = '新增實驗物'
        return render_template('./exp/parent/subject-object.html', **locals())
    elif request.method == 'POST':
        try:
            form_data = request.values.to_dict()
            data = dict(address=id, form_data=form_data)
            Exp.add_obj(data)
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('成功', category='success')
            return redirect(url_for(endpoint.exp.parent.obj4sub, id=id))
    abort(404)


def start4sub(id):
    if request.method == 'GET':
        title = '開始實驗'
        return render_template('./exp/parent/subject.html', **locals())
    elif request.method == 'POST':
        form_data = request.values.to_dict()
        data = dict(address=id, date=form_data['date'])
        try:
            Exp.start(data)
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('成功', category='success')
            return redirect(url_for(endpoint.exp.parent.index))


def obj4run(id):
    if request.method == 'GET':
        title = '實驗物清單'
        return render_template('./exp/parent/running.html', **locals())


def sign_up(address, type, location):
    if request.method == 'GET':
        data = dict(address=address, type=type, location=location)
        try:
            Exp.sign_up(data)
        except Exception as e:
            if e.args[0] in exception_code.dict().values():
                flash(e.args[0], category='error')
                return redirect(request.referrer)
            current_app.logger.error(f'error msg: {e}')
            abort(404)
        else:
            flash('成功', category='success')
            return redirect(url_for(endpoint.exp.public.index))


# parent = Blueprint('parent', __name__, url_prefix='/parent')
# parent.add_url_rule(rule='/', endpoint=None, view_func=index, methods=['GET'])
# parent.add_url_rule(rule='/index', endpoint=None, view_func=index, methods=['GET'])
# parent.add_url_rule(rule='/build', endpoint=None, view_func=build, methods=['GET', 'POST'])
# parent.add_url_rule(rule='/build/update/<id>', endpoint=None, view_func=update4build, methods=['GET', 'POST'])
# parent.add_url_rule(rule='/build/auth/<id>', endpoint=None, view_func=build2auth, methods=['GET'])
# parent.add_url_rule(rule='/experiment/subject/<id>', endpoint=None, view_func=exp2sub, methods=['GET'])
# parent.add_url_rule(rule='/subject/object/<id>', endpoint=None, view_func=obj4sub, methods=['GET', 'POST'])
# parent.add_url_rule(rule='/subject/start/<id>', endpoint=None, view_func=start4sub, methods=['GET', 'POST'])
# parent.add_url_rule(rule='/running/object/<id>', endpoint=None, view_func=obj4run, methods=['GET', 'POST'])
# parent.add_url_rule(rule='/sign_up/<address>/<type>/<location>', endpoint=None, view_func=sign_up, methods=['GET'])
