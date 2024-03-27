from flask_sqlalchemy import SQLAlchemy
from module import auxiliary, database_type
import config

DB = SQLAlchemy()

class Core(DB.Model):
    __tablename__ = f'{config.DATABASE["tablePrefix"]}core'

    name = DB.Column(DB.String(255), primary_key=True)
    content = DB.Column(DB.String(255))

    def __init__(self, name: str, content: str) -> None:
        self.name = name
        self.content = content

class Domain(DB.Model):
    __tablename__ = f'{config.DATABASE["tablePrefix"]}domain'

    id = DB.Column(DB.Integer, primary_key=True)
    protocol = DB.Column(DB.Integer)
    domain = DB.Column(DB.String(255))

class Url(DB.Model):
    __tablename__ = f'{config.DATABASE["tablePrefix"]}url'

    id = DB.Column(DB.Integer, primary_key=True)
    type_ = DB.Column(DB.Integer)
    domain_id = DB.Column(DB.Integer)
    long_url = DB.Column(DB.String(255))
    signature = DB.Column(DB.String(255))
    valid_day = DB.Column(DB.Integer)
    count = DB.Column(DB.Integer)
    creation_timestamp = DB.Column(DB.Integer)

    def __init__(self, type_: database_type.Url, domain_id: int, long_url: str, valid_day: int, signature: str=None) -> None:
        self.type_ = type_.value
        self.domain_id = domain_id
        self.long_url = long_url
        self.signature = signature or ''
        self.valid_day = valid_day
        self.count = 0
        self.creation_timestamp = auxiliary.getTimestamp()