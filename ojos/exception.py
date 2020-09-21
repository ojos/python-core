class BaseException(Exception):
    MESSAGE_TEMPLATE = "Exception {}: {}"

    def __init__(self, name: str, value, *args, **kwargs):
        self.message = self.MESSAGE_TEMPLATE.format(name, value)
        super(BaseException, self).__init__(*args)

    def __str__(self):
        return "{}".format(self.message)

    def __repr__(self):
        return "<{}('{}')>".format(self.__class__.__name__, self.message)
