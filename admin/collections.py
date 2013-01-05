from django.conf import settings
from django.db.models import Model
from django.db.models.base import ModelBase
from django.utils.importlib import import_module

from composite.views import ViewCollection

from views import admin
from views import login
from views import model


class ModelAdmin(ViewCollection):

    application_namespace = 'model-admin'

    list_display = (unicode,)
    list_filter = ()

    def __init__(self, instance_namespace, model_class):
        super(ModelAdmin, self).__init__(instance_namespace)
        self.model_class = model_class
        path = r'^$'
        name = 'object-list'
        self.add_view(path, model.Index, name=name)

    def app_label(self):
        return self.model_class._meta.app_label

    def model_name(self):
        return self.model_class._meta.module_name

    @property
    def application_namespace(self):
        return '%s-%s' % (self.app_label, self.model_name)

    def index_name(self):
        return 'adminnext:%s:object-list' % self.application_namespace


class Login(ViewCollection):

    def __init__(self, instance_namespace=None):
        super(Login, self).__init__(instance_namespace)
        self.add_view('^login$', login.Login, name='login')


class AdminSite(ViewCollection):

    application_namespace = 'adminnext'

    ModelAdmin = ModelAdmin

    def __init__(self, instance_namespace=None):
        super(AdminSite, self).__init__(instance_namespace)
        self.add_view('^$', admin.Index, name='index')
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
        app_name, model_name = (
            model._meta.app_label,
            model._meta.module_name
        )
        path = r'^%s/%s/' % (app_name, model_name)
        instance_name = '%s-%s' % (app_name, model_name)
        initkwargs = dict(model_class=model)
        self.add_collection(path, model_admin, instance_name, initkwargs)
