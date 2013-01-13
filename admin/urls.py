from django.conf import settings
from django.db.models import Model
from django.db.models.base import ModelBase
from django.utils.importlib import import_module

from composite.urls import UrlCollection

from views import admin
from views import login
from views import model


class ModelAdmin(UrlCollection):

    application_namespace = 'model-admin'

    list_display = (unicode,)
    list_filter = ()

    def __init__(self, instance_namespace, model_class):
        super(ModelAdmin, self).__init__(instance_namespace)
        self.model_class = model_class
        initkwargs = dict(
            model_class=model_class,
            list_display=self.list_display,
            list_filter=self.list_filter,
        )
        self.add_url(r'^$', model.Index, initkwargs, 'object-list')
        initkwargs = dict(
            model_class=model_class,
        )
        self.add_url(r'^add$', model.AddView, initkwargs, 'add')
        initkwargs = dict(
            model_class=model_class,
        )
        self.add_url(r'^edit/(?P<pk>\d+)$', model.EditView, initkwargs, 'edit')

    @property
    def application_namespace(self):
        return '%s-%s' % (
            self.model_class._meta.app_label,
            self.model_class._meta.module_name,
        )


class Login(UrlCollection):

    def __init__(self, instance_namespace=None):
        super(Login, self).__init__(instance_namespace)
        self.add_url('^login$', login.Login, name='login')


class AdminSite(UrlCollection):

    application_namespace = 'compositeadmin'

    ModelAdmin = ModelAdmin

    def __init__(self, instance_namespace=None):
        super(AdminSite, self).__init__(instance_namespace)
        self.model_admins = list()
        self.add_url(
            '^$',
            admin.Index,
            dict(model_admins=self.model_admins),
            'index',
        )
        self.add_collection('^', Login)

    def autodiscover(self, all=False):
        if all:
            for app in settings.INSTALLED_APPS:
                models = import_module('%s.models' % app)
                for variable_name in dir(models):
                    variable = getattr(models, variable_name)
                    if (isinstance(variable, ModelBase)
                        and issubclass(variable, Model)):
                        self.register(variable)
        else:
            for app in settings.INSTALLED_APPS:
                try:
                    models = import_module('%s.admin' % app)
                except ImportError:
                    pass

    def register(self, model, model_admin_class=None):
        model_admin = model_admin_class if model_admin_class else self.ModelAdmin
        app_label, model_name = (
            model._meta.app_label,
            model._meta.module_name
        )
        path = r'^%s/%s/' % (app_label, model_name)
        instance_name = '%s-%s' % (app_label, model_name)
        index_name = 'compositeadmin:%s:object-list' % instance_name
        initkwargs = dict(model_class=model)
        self.model_admins.append(
            dict(
                model_name=model_name,
                index_name=index_name,
                app_label=app_label,
            )
        )
        self.add_collection(path, model_admin, instance_name, initkwargs)
