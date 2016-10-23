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
            ('self', reverse('category-detail', kwargs={
                'category': category.id}, request=self.request)),
            ('options', reverse('option-list', kwargs={
                'category': category.id}, request=self.request)),
            ('topics', reverse('topic-list', kwargs={
                'category': category.id}, request=self.request)),
        ]


class TopicSerializer(HateoasFieldSerializer):
    fields = ('label',)

    def getLinks(self, topic):
        return [
            ('self', reverse('topic-detail', kwargs={
                'category': topic.category_id,
                'topic': topic.id}, request=self.request)),
            ('options', reverse('topic-options-list', kwargs={
                'category': topic.category_id,
                'topic': topic.id}, request=self.request)),
        ]


class OptionSerializer(HateoasFieldSerializer):
    fields = ('label',)

    def getLinks(self, option):
        return [
            ('self', reverse('option-detail', kwargs={
                'category': option.category_id,
                'option': option.id}, request=self.request)),
            ('topics', reverse('option-topics-list', kwargs={
                'category': option.category_id,
                'option': option.id}, request=self.request)),
        ]
