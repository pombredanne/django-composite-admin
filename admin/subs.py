from django.conf import settings
from django.db.models import Model
from django.db.models.base import ModelBase
from django.views.generic import View
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.importlib import import_module
from django.contrib.admin.models import LogEntry
from django.forms.models import modelform_factory

from composite.sub import Sub
from composite.views import StackedComposite
from composite.utils import OrderedSet




class ObjectChange(AdminPage):

    path = r'^/edit/(\d+)$'
    name = 'object-change'

    template_name = 'adminnext/object_change.html'

    def __init__(self):
        super(ObjectChange, self).__init__()
        self.breadcrumb = (
            ('Home', 'index'),
            (self.sub.app_label, None),  # FIXME need url name
            (self.sub.model_name, None),  # FIXME need url name
            ('edit', None),
        )

    def get_object(self, request, pk):
        return get_object_or_404(self.sub.model, pk=pk)

    def get_form(self, request, obj=None):
        ObjectModelForm = modelform_factory(self.sub.model)
        if request.method == 'POST':
            form = ObjectModelForm(request.POST, instance=obj)
        else:
            form = ObjectModelForm(instance=obj)
        return form

    def get_context_data(self, request, *args, **kwargs):
        ctx = super(ObjectChange, self).get_context_data(request, *args, **kwargs)
        pk = args[0]
        ctx['object'] = obj = self.get_object(request, pk)
        ctx['form'] = self.get_form(request, obj)
        return ctx

    def post(self, request, pk):
        obj = self.get_object(request, pk)
        form = self.get_form(request, obj)
        if form.is_valid():
            form.save()
            url = '/adminnext/%s/%s' % (
                self.sub.app_label,
                self.sub.model_name,
            )
            return redirect(url)  # FIXME: hardcoded urls
        ctx = self.get_context_data(request, pk)
        r = self.render_to_response(ctx)
        return r


class ObjectListWidget(Widget):

    template_name = 'adminnext/widgets/object_list.html'

    def __init__(self, *columns):
        super(ObjectListWidget, self).__init__()
        self.columns = columns

    def get_context_data(self, page, request, *args, **kwargs):
        ctx = super(ObjectListWidget, self).get_context_data(page, request, *args, **kwargs)
        # FIXME: merge the actions in this widget
        queryset = page.get_queryset(request)
        paginator = Paginator(queryset, 30)  # FIXME: hardcoded value
        page = request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objects = paginator.page(paginator.num_pages)
        ctx['objects'] = objects
        ctx['columns'] = self.columns
        ctx['object_change'] = '%s:%s' % (
            self.page().sub.instance_namespace,
            'object-change',
        )
        return ctx


class ObjectList(AdminPage):

    widgets = (
        ObjectListWidget(),
    )
    path = r'^$'
    name = 'object-list'

    def __init__(self):
        super(ObjectList, self).__init__()
        self.breadcrumb = OrderedSet((
            ('Home', 'index'),
            (self.sub.app_label, None),
            (self.sub.model_name, None),
        ))

    def get_queryset(self, request):
        model = self.sub.model
        queryset = model.objects.all()
        return queryset




class ModelAdmin(Sub):

    application_namespace = None

    ObjectList = ObjectList
    ObjectChange = ObjectChange

    def __init__(self, model):
        self.model = model
        instance_namespace = '%s-%s' % (
            self.app_label,
            self.model_name
        )
        super(ModelAdmin, self).__init__(instance_namespace)
        self.register(subclass_for_model(self.ObjectList, model))
        self.register(subclass_for_model(self.ObjectChange, model))

    @property
    def app_label(self):
        return self.model._meta.app_label

    @property
    def model_name(self):
        return self.model._meta.module_name

    @property
    def path(self):
        return r'%s/%s' % (self.app_label, self.model_name)


class AppList(Widget):

    template_name = 'adminnext/widgets/app_list.html'

    def get_context_data(self, page, request, *args, **kwargs):
        ctx = super(AppList, self).get_context_data(page, request, *args, **kwargs)
        ctx['app_subs'] = self.page().sub.app_subs
        return ctx


class RecentActions(Widget):

    template_name = 'adminnext/widgets/recent_actions.html'

    def get_context_data(self, page, request, *args, **kwargs):
        ctx = super(RecentActions, self).get_context_data(page, request, *args, **kwargs)
        ctx['entries'] = LogEntry.objects.all()[:10]
        return ctx


class AdminIndex(AdminPage):

    path = r'^$'
    name = 'index'

    widgets = (AppList(), RecentActions())

    def __init__(self):
        super(AdminIndex, self).__init__()
        self.breadcrumb = OrderedSet((
            ('Home', None),
        ))


class Login(AdminPage):

    path = r'^login$'
    name = 'login'

    widgets = (LoginWidget('index'),)
    body_class = 'login-index'

    is_staff = False


class Logout(View):

    path = r'^logout$'
    name = 'logout'


class ChangePassword(AdminPage):

    path = r'^change_password$'
    name = 'change-password'


class LoginManagement(Sub):

    application_namespace = 'login'
    path = r''

    Login = Login
    Logout = Logout
    ChangePassword = ChangePassword

    def __init__(self):
        super(LoginManagement, self).__init__()
        self.register(self.Login)
        self.register(self.Logout)
        self.register(self.ChangePassword)


class Admin(Sub):

    application_namespace = 'composite-admin'
    path = r''

    # subs
    ModelAdmin = ModelAdmin
    LoginManagement = LoginManagement

    # pages
    AdminIndex = AdminIndex

    def __init__(self, instance_namespace=None):
        super(Admin, self).__init__(instance_namespace)
        self.app_subs = dict()
        self.register(self.AdminIndex)
        self.register(self.LoginManagement())

    def register_model(self, model, ModelAdmin=None):
        app_label = model._meta.app_label
        if app_label not in self.app_subs:
            self.app_subs[app_label] = list()
        ModelAdmin = ModelAdmin if ModelAdmin else self.ModelAdmin
        admin = ModelAdmin(model)
        self.register(admin)
        self.app_subs[app_label].append(admin)

    def autodiscover(self, all=False):
        if all:
            for app in settings.INSTALLED_APPS:
                models = import_module('%s.models' % app)
                for variable_name in dir(models):
                    variable = getattr(models, variable_name)
                    if (isinstance(variable, ModelBase)
                        and issubclass(variable, Model)):
                        self.register_model(variable)
        else:
            raise NotImplementedError()
