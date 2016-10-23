from rest_framework.reverse import reverse


class BaseSerializer(object):
    values = []
    request = None
    many = False

    def __init__(self, request, values, many=False):
        self.values = values
        self.request = request
        self.many = many

    def serialize(self, value):
        raise NotImplementedError()

    @property
    def data(self):
        if self.many:
            return (self.serialize(v) for v in list(self.values))
        else:
            return self.serialize(self.values)


class FieldSerializer(BaseSerializer):
    fields = ()

    def serialize(self, value):
        return {k: getattr(value, k) for k in self.fields}


class HateoasFieldSerializer(FieldSerializer):
    def getLinks(self, value):
        raise NotImplementedError()

    def serialize(self, value):
        fields = super(HateoasFieldSerializer, self).serialize(value)
        fields['links'] = [
            {'rel': k, 'href': v} for (k, v) in self.getLinks(value)
        ]
        return fields


class CategorySerializer(HateoasFieldSerializer):
    fields = ('label',)

    def getLinks(self, category):
        return [
            ('self', reverse('category-detail', kwargs={'id': category.id}, request=self.request))
        ]
