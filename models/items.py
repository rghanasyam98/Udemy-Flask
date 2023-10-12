from db import db

class ItemModel(db.Model):
    __tablename__="item"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    description=db.Column(db.String(100))
    price=db.Column(db.Float(precision=2),unique=False,nullable=False)
    store_id=db.Column(db.Integer,db.ForeignKey("store.id"),unique=False,nullable=False)
    
    store=db.relationship("StoreModel",back_populates="items")#to establish a link between ItemModel and StoreModel
    tags=db.relationship("TagModel", back_populates="items", secondary="item_tags")#secondary attribute refer the third table involved in the many to many relation
    
    
    def __repr__(self):
        return f'<Item {self.name}>'
    
    