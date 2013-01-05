from base import Base


class Index(Base):

    breadcrumb = []
    template_name = 'adminnext/index.html'

    def __init__(self, parent=None, *args, **kwargs):
        super(Index, self).__init__(parent, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.breadcrumb = [('Home', None)]
        context = super(Index, self).get_context_data(**kwargs)
        model_admins = list()
        for collection in self.collection.collections:
            if hasattr(collection, 'model_name'):
                model_admins.append(collection)
        context['model_admins'] = model_admins
        return context
