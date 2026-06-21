class BaseService:
    repository = None
    model = None

    @classmethod
    def get_by_id(cls, id):
        return cls.repository.get_by_id(id)

    @classmethod
    def get_all(cls, filters):
        return cls.repository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @classmethod
    def create(cls, data):
        instance = cls.model.from_json(data)
        return cls.repository.save(instance)

    @classmethod
    def update(cls, id, data):
        instance = cls.repository.get_by_id(id)
        for key, value in data.items():
            setattr(instance, key, value)
        return cls.repository.save(instance)

    @classmethod
    def delete(cls, id):
        instance = cls.repository.get_by_id(id)
        cls.repository.delete(instance)
