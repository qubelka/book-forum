from sqlalchemy import and_
from flask import redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import current_user
from flask_security.utils import hash_password
from application import db
from application.topics.helper import create_slug
from application.models import User

def active_users_excluding_admin():
    return User.query.filter(and_(User.active, User.id != current_user.id))

class AdminView(ModelView):
    column_display_pk = True
    can_view_details = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        flash('Please log in as admin to access this page.', category='warning')
        return redirect(url_for('index'))

    def on_model_change(self, form, model, is_created):
        if type(model).__name__ in ['Topic', 'Thread', 'Message']:
            if hasattr(model, 'name'):
                model.slug = create_slug(title=model.name, type=type(model).__name__)

                if hasattr(model, 'secret_users'):
                    if model.secret_users:
                        model.secret_users.append(current_user)

            else:
                model.slug = create_slug(title=model.body, type='Message')

            if hasattr(model, 'creator_id'):
                admin = User.query.filter(User.username == 'admin').first()
                model.creator_id = admin.id

        if type(model) is User:
            model.password = hash_password(model.password)

        return super(AdminView, self).on_model_change(form, model, is_created)

    def delete_model(self, model):
        if type(model) is User:
            model.active = False
            db.session.add(model)
            db.session.commit()
            return True

        super(AdminView, self).delete_model(model)

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        flash('Please log in as admin to access this page.', category='warning')
        return redirect(url_for('index'))

class UserCustomView(AdminView, ModelView):
    form_columns = ['roles', 'email', 'username']
    column_exclude_list = ('password')
    column_details_exclude_list = ('password')

class ThreadCustomView(AdminView, ModelView):
    form_columns = ['name', 'topic', 'secret_users']
    form_args = dict(
        secret_users = dict(
            query_factory=active_users_excluding_admin
        )
    )

class MessageCustomView(AdminView, ModelView):
    form_columns = ['body', 'thread']

class TopicCustomView(AdminView, ModelView):
    form_columns = ['name', 'description']