from composite.views import StackedComposite


class Dashboard(StackedComposite):

    def __init__(self, parent, *args, **kwargs):
        super(Dashboard, self).__init__(parent, *args, **kwargs)
        self._composites = list(self.composites)

    def append_composite(self, composite_class, *args):
        if args:
            args = list(args)
            args.insert(0, composite_class)
            self.composites.append(args)
        else:
            self.composites.append(composite_class)


class NamedWidgetsDashboard(StackedComposite):
    pass
