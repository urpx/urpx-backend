import datetime as dt

from urpx.database import Column, Model, SurrogatePK, db, relationship, reference_col

class Product(SurrogatePK, Model):
    __tablename__ = 'products'

    description = Column(db.String(100), nullable=False)
    amount = Column(db.Integer(), nullable=False)
    created_at = Column(db.DateTime, 
        nullable=False, default=dt.datetime.utcnow)

    def __init__(self, user_id, amount, description, **kwargs):
        """Create instance."""
        db.Model.__init__(self, user_id=user_id, 
            amount=amount, description=description, **kwargs)