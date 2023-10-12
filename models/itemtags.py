from db import db

# this third table is required for many to many mapping 
# flask doesn't create it automatically like in django

class ItemTagModel(db.Model):
    __tablename__="item_tags"
    
    id=db.Column(db.Integer, primary_key=True)
    item_id=db.Column(db.Integer,db.ForeignKey("item.id"))
    tag_id=db.Column(db.Integer,db.ForeignKey("tag.id"))