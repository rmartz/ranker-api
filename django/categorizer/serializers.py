class BaseSerializer(object):
    objects = []
    many = False

    def __init__(self, objects, many=False):
        self.many = many
        self.objects = objects

    def serialize(self, object):
        raise NotImplementedError()

    @property
    def data(self):
        if self.many:
            return (self.serialize(o) for o in list(self.objects))
        else:
            return self.serialize(self.objects)


class CategorySerializer(BaseSerializer):
    def serialize(self, category):
        return {'a': 15}
