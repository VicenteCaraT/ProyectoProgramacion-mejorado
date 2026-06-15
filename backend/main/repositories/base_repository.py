from .. import db

class BaseRepository:
    model = None
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls.model, id)
    
    @classmethod
    def get_all(cls, page=1, per_page=10, filters=None):
        query = db.session.query(cls.model)
        if filters:
            query = cls._apply_filters(query, filters)
        return query.paginate(page=page, per_page=per_page, error_out=True)
    

    @classmethod
    def save(cls, instance):
        db.session.add(instance)
        db.session.commit()
        return instance
    
    @classmethod
    def delete(cls, instance):
        db.session.delete(instance)
        db.session.commit()
        
    @classmethod
    def _apply_filters(cls, query, filters):
        return query