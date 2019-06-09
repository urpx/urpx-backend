from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (isinstance(record_id, str) and record_id.isdigit(),
             isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))