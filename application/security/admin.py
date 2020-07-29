from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import current_user
from application.topics.helper import create_slug
from application.models import User

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

    def on_model_change(self, form, model, is_created):
        if type(model).__name__ in ['Topic', 'Thread', 'Message']:
            if hasattr(model, 'name'):
                model.slug = create_slug(title=model.name, type=type(model).__name__)
            else:
                model.slug = create_slug(title=None, type='Message')

            if hasattr(model, 'user_id'):
                admin = User.query.filter(User.username == 'admin').first()
                model.user_id = admin.id

        return super(AdminView, self).on_model_change(form, model, is_created)


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

