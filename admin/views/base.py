from composite.views import StackedComposite
from composite.mixin import LoginRequiredMixin
from composite.mixin import PermissionRequiredMixin


class Bootstrap(StackedComposite):

    css_files = ['css/bootstrap.css', 'css/bootstrap-responsive.css', 'css/admin.css']
    javascript_files = ['js/jquery.js', 'js/bootstrap.js']

    template_name = 'adminnext/base.html'


class Base(LoginRequiredMixin, Bootstrap, PermissionRequiredMixin):

    login_url_name = 'adminnext:login'
    is_staff = True

    def get_context_data(self, **kwargs):
        ctx = super(Base, self).get_context_data(**kwargs)
        ctx['breadcrumb'] = self.breadcrumb
        return ctx
