from db import db

class StoreModel(db.Model):
    __tablename__ = 'store'
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    # to establish a link between StoreModel and ItemModel 
    # cascade="all, delete" => to implement cascaded deletion, when store is delted its items will also be deleted
    items=db.relationship("ItemModel",back_populates="store",lazy="dynamic", cascade="all, delete")
    tags=db.relationship("TagModel",back_populates="store",lazy="dynamic", cascade="all, delete")
    
    def __repr__(self):
        return f'<Store {self.name}>'