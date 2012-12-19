from django.conf import settings
from django.db.models import Model
from django.core.paginator import Paginator
from django.utils.importlib import import_module
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from composite.sub import Sub
from composite.widget import Widget
from composite.pages.bootstrap import OneColumn


class ObjectListWidget(Widget):

    template_name = 'admin/widgets/object_list.html'

    def get_context_data(self, page, request, *args, **kwargs):
        ctx = super(ObjectListWidget, self).get_context_data(page, request, *args, **kwargs)
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
        return ctx


class ObjectList(OneColumn):

    widgets = (ObjectListWidget(),)

    path = r'$'

    @property
    def name(self):
        return 'object-list-%s-%s' % (
            self.sub.model._meta.app_label,
            self.sub.model._meta.object_name,
        )

    def get_queryset(self, request):
        model = self.sub.model
        queryset = model.objects.all()
        return queryset


class ObjectChange(OneColumn):
    pass


class ModelAdmin(Sub):

    def __init__(self, model):
        super(ModelAdmin, self).__init__()
        self.model = model
        self.register(ObjectList)

    @property
    def app_label(self):
        return self.model._meta.app_label

    @property
    def model_name(self):
        return self.model._meta.module_name

    @property
    def path(self):
        return r'%s/%s' % (self.app_label, self.model_name)


class Admin(Sub):

    app_name = 'newadmin'
    namespace = 'newadmin'
    path = ''

    def register(self, model, ModelAdminClass=None):
        if ModelAdminClass:
            admin = ModelAdminClass(model)
            super(Admin, self).register(admin)
        else:  # Use default ModelAdmin
            admin = ModelAdmin(model)
            super(Admin, self).register(admin)

    def autodiscover(self, all=False):
        for app in settings.INSTALLED_APPS:
            models = import_module('%s.models' % app)
            for variable_name in dir(models):
                variable = getattr(models, variable_name)
                if isinstance(variable, Model):
                    self.register(variable)
