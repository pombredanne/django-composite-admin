from django import forms
from django.shortcuts import redirect
from django.forms.models import modelform_factory

from ..base import BaseLeaf


class ModelChangeForm(object):

    def __init__(
            self,
            request,
            model_class,
            fields=None,
            exclude=None,
            form_class=forms.ModelForm,
            inlines=None,
            object=None):
        self._form_class = form_class
        self.fields = fields
        self.exclude = exclude
        self.request = request
        self.model_class = model_class
        self.object = object
        self.inlines = inlines if inlines else list()

    def formfield_for_dbfield(self, db_field, **kwargs):
        return db_field.formfield(**kwargs)

    def form_class(self):
        defaults = dict(
            form=self._form_class,
            fields=self.fields,
            exclude=self.exclude,
            formfield_callback=self.formfield_for_dbfield,
        )
        return modelform_factory(self.model_class, **defaults)


class BaseChangeView(BaseLeaf):

    model_class = None
    verbose_name = None

    def get_template_names(self):
        custom_template = 'compositeadmin/%s/%s/edit.html' % (
            self.model_class._meta.app_label,
            self.model_class._meta.module_name
        )
        return [custom_template, 'compositeadmin/model/edit.html']

    def changelist_url_name(self):
        return 'compositeadmin:%s-%s:object-list' % (self.model_class._meta.app_label, self.model_class._meta.module_name)

    def get_context_data(self, **kwargs):
        context = super(BaseChangeView, self).get_context_data(**kwargs)
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.module_name
        changelist = self.changelist_url_name()
        breadcrumb = (('Administration', 'compositeadmin:index'), (app_label, None), (model_name, changelist), (self.verbose_name, None))
        context['breadcrumb'] = breadcrumb
        context['model_name'] = model_name
        context['verbose_name'] = self.verbose_name
        return context


class AddView(BaseChangeView):

    def __init__(self, **kwargs):
        kwargs['verbose_name'] = 'add'
        super(AddView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        change_form = ModelChangeForm(request, self.model_class)
        Form = change_form.form_class()
        context['form'] = Form()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        change_form = ModelChangeForm(request, self.model_class)
        Form = change_form.form_class()
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.changelist_url_name())
        return self.render_to_response(context)


class EditView(BaseChangeView):

    def __init__(self, **kwargs):
        kwargs['verbose_name'] = 'edit'
        super(EditView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        pk = self.kwargs['pk']
        object = self.model_class.objects.get(pk=pk)
        change_form = ModelChangeForm(request, self.model_class)
        Form = change_form.form_class()
        context['form'] = Form(instance=object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        change_form = ModelChangeForm(request, self.model_class)
        Form = change_form.form_class()
        pk = self.kwargs['pk']
        object = self.model_class.objects.get(pk=pk)
        form = Form(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(self.changelist_url_name())
        return self.render_to_response(context)
