from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# TODO merge User and Employee
# Employee: full info referring weixin user info
class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(36), primary_key=True)
    wx_user_id = db.Column(db.String(40), unique=True,nullable=False)
    merchant_id = db.Column(db.String(36), nullable=True)
    role = db.Column(db.String(40), nullable=True)


class Instance(db.Model):
    instance_id = db.Column(db.String(40), primary_key=True)
    service_id = db.Column(db.String(40))
    plan_id = db.Column(db.String(40))
    organization_guid = db.Column(db.String(40))
    space_guid = db.Column(db.String(40))


class Client(db.Model):
    # TODO use Instance class to represent the relation from Client to Instance
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)
    instance_id = db.Column(db.String(40))
    binding_id = db.Column(db.String(40))
    plan_id = db.Column(db.String(40))
    service_id = db.Column(db.String(40))
    app_guid = db.Column(db.String(40))

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.String(36), db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.String(36), db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
# 
# class Employee(db.Model):
#     id = db.Column(db.String(32), primary_key=True)
#     wx_user_id = db.Column(db.String(40), unique=True, nullable=False)
#     merchant_id = db.Column(db.String(40), nullable=False)
#     role = db.Column(db.String(40), nullable=False)
