from composite import LeafCompositeView
from composite import StackedCompositeView
from composite.mixin import LoginRequiredMixin
from composite.mixin import PermissionRequiredMixin


class Base(LoginRequiredMixin, StackedCompositeView, PermissionRequiredMixin):

    login_url_name = 'compositeadmin:login'
    is_staff = True

    template_name = 'adminnext/base.html'


class BaseLeaf(LoginRequiredMixin, LeafCompositeView, PermissionRequiredMixin):

    login_url_name = 'compositeadmin:login'
    is_staff = True

    template_name = 'adminnext/base.html'
