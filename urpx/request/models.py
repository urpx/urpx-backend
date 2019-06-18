import datetime as dt

from urpx.database import Column, Model, SurrogatePK, db, relationship, reference_col

class Request(SurrogatePK, Model):
    __tablename__ = 'requests'

    product_name = Column(db.String(100), nullable=False)
    company = Column(db.String(100), nullable=False)
    belongto = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, 
        nullable=False, default=dt.datetime.utcnow)

    user_id = reference_col('users')

    def __init__(self, user_id, product_name, 
        company, belongto, **kwargs):
        """Create instance."""
        db.Model.__init__(self, user_id=user_id, product_name=product_name,
            company=company, belongto=belongto, **kwargs)