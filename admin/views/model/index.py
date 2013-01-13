from django.core.urlresolvers import reverse

from composite import Filter
from composite import ChangeList
from composite import LeafCompositeView

from ..base import Base


class AdminChangeList(ChangeList):

    def item(self, object, i):
        iterator = super(AdminChangeList, self).item(object, i)
        field = next(iterator)
        name = '%s-%s' % (
            self.parent.model_class._meta.app_label,
            self.parent.model_class._meta.module_name
        )
        name = 'compositeadmin:%s:edit' % name
        url = reverse(name, kwargs=dict(pk=object.pk))
        yield '<a href="%s">%s</a>' % (url, field)
        for field in iterator:
            yield field


class ObjectTools(LeafCompositeView):

    template_name = 'compositeadmin/model/widgets/object_tools.html'

    def get_context_data(self, **kwargs):
        context = super(ObjectTools, self).get_context_data(**kwargs)
        name = '%s-%s' % (
            self.parent.model_class._meta.app_label,
            self.parent.model_class._meta.module_name,
        )
        urlname = 'compositeadmin:%s:add' % name
        buttons = (('Add', urlname),)
        context['buttons'] = buttons
        return context


class Index(Base):

    template_name = 'compositeadmin/model/index.html'

    model_class = None
    list_display = None
    list_filter = None

    def _composites(self, request, *args, **kwargs):
        yield ObjectTools(parent=self)
        # FIXME: ChangeList depends on filter to work
        filter = Filter(parent=self, list_filter=self.list_filter, model_class=self.model_class)
        # filter is used before it has been init for this request
        # it expects request to be available
        filter.request = self.request
        change_list = AdminChangeList(parent=self, filter=filter, model_class=self.model_class, list_display=self.list_display)
        yield change_list
        yield filter

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.module_name
        breadcrumb = (('Home', 'compositeadmin:index'), (app_label, None), (model_name, None))
        context['breadcrumb'] = breadcrumb
        context['model_name'] = model_name
        return context
