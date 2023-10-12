from db import db


class TagModel(db.Model):
    __tablename__ = 'tag'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey("store.id"), unique=False, nullable=False)
    
    store=db.relationship("StoreModel", back_populates="tags")
    items=db.relationship("ItemModel", back_populates="tags", secondary="item_tags")#secondary attribute refer the third table involved in the many to many relation
    
    def __repr__(self):
        return f'<Store {self.name}>'