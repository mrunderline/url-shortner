import datetime
from ..api import db
from sqlalchemy.exc import IntegrityError


class Url(db.Model):
    original_url = db.Column(db.String(2048))
    shorted_url = db.Column(db.String(32), primary_key=True)
    seen = db.Column(db.BigInteger(), default=0)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now)

    def insert(self):
        session = db.session
        try:
            session.add(self)
            session.commit()
            return True, self
        except IntegrityError as err:
            session.rollback()
            if err.code == 'gkpj':  # check Duplicate entry
                exists = Url.query.filter_by(
                    shorted_url=self.shorted_url,
                    original_url=self.original_url,
                ).first()

                if exists:
                    return True, self
                else:
                    return False, {'message': 'this shorted_name is inaccessible'}

            return False, {'message': 'excepted error'}
        except:
            return False, {'message': 'excepted error'}

    def find_original_url(self, shorted_url):
        session = db.session
        record = self.query.filter_by(shorted_url=shorted_url)
        if record.first() is None:
            return None

        record.update({'seen': Url.seen + 1})
        session.commit()

        return record.first()
