from base import Base


class Index(Base):

    breadcrumb = []
    template_name = 'compositeadmin/index.html'

    model_admins = None

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        breadcrumb = [('Home', None)]
        context['breadcrumb'] = breadcrumb
        context['model_admins'] = self.model_admins
        return context
