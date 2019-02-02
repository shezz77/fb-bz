from flask import Flask, jsonify, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

app = Flask(__name__)

app.config['access_token'] = 'EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD'
app.config['facebook_business_api_url'] = 'https://graph.facebook.com/v3.2'

POSTGRES = {
    'user': 'postgres',
    'pw': 'root',
    'db': 'facebook_business',
    'host': 'localhost',
    'port': '5432',
}

app.config['SECRET_KEY'] = 'this_is_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(
    POSTGRES['user'],
    POSTGRES['pw'],
    POSTGRES['host'],
    POSTGRES['port'],
    POSTGRES['db']
)
app.config['DEBUG'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer
                   , primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=True)
    facebook_id = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name


class AdAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_account_id = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", backref=db.backref("ad_accounts", lazy=True))

    def __repr__(self):
        return '<Ad Account %r>' % self.ad_account_id


class AdPixel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_pixel_id = db.Column(db.String(50))
    ad_pixel_name = db.Column(db.String(50))
    ad_account_id = db.Column(db.Integer, db.ForeignKey('ad_account.id'))
    ad_account = relationship("AdAccount", backref=db.backref("ad_pixels", lazy=True))

    def __repr__(self):
        return '<Ad Account %r>' % self.ad_account_id


class FacebookPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_account_id = db.Column(db.Integer, db.ForeignKey('ad_account.id'))
    page_id = db.Column(db.String(50), nullable=True)
    page_name = db.Column(db.String(80), nullable=True)
    ad_account = relationship("AdAccount", backref=db.backref("facebook_pages", lazy=True))

    def __repr__(self):
        return '<Facebook Pages %r>' % self.ad_account_id


class Instagram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_account_id = db.Column(db.Integer, db.ForeignKey('ad_account.id'))
    instagram_id = db.Column(db.String(50), nullable=True)
    instagram_user_name = db.Column(db.String(80), nullable=True)
    ad_account = relationship("AdAccount", backref=db.backref("instagrams", lazy=True))

    def __repr__(self):
        return '<Instagram %r>' % self.ad_account_id


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_account_id = db.Column(db.Integer, db.ForeignKey('ad_account.id'))
    app_id = db.Column(db.String(50), nullable=True)
    app_name = db.Column(db.String(80), nullable=True)
    ad_account = relationship("AdAccount", backref=db.backref("applications", lazy=True))

    def __repr__(self):
        return '<Application %r>' % self.ad_account_id


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get-facebook-id-info', methods=['POST'])
def get_facebook_id_info():
    response = {}
    search_ad_account_id = request.form['search']
    # q = request.form['q']
    if search_ad_account_id:
        response = get_instagram_info(search_ad_account_id, response)
        response = get_ad_pixel_info(search_ad_account_id, response)
        response = promote_pages(search_ad_account_id, response)
        response = get_applications(search_ad_account_id, response)
        response = get_offline_conversion_data_sets(search_ad_account_id, response)
        response = get_custom_audience(search_ad_account_id, response)
        # if q:
        #     response = get_target_audience(search_ad_account_id, response, q)
        save_user_info(response, search_ad_account_id)

    return jsonify(response)


def save_user_info(data, facebook_id):
    user = User(facebook_id=facebook_id)
    ad_account = AdAccount(ad_account_id=facebook_id)
    user.ad_accounts.append(ad_account)

    print(data['ad_pixel'])
    if 'ad_pixel' in data:
        for i in (range(len(data['ad_pixel']))):
            ad_pixel = AdPixel(ad_pixel_id=data['ad_pixel'][i]['id'], ad_pixel_name=data['ad_pixel'][i]['name'])
            ad_account.ad_pixels.append(ad_pixel)

    if 'promote_pages' in data:
        for i in (range(len(data['promote_pages']))):
            application = FacebookPage(
                page_id=data['promote_pages'][i]['id'],
                page_name=data['promote_pages'][i]['name']
            )
            ad_account.facebook_pages.append(application)

    if 'instagram' in data:
        for i in (range(len(data['instagram']))):
            instagram = Instagram(
                instagram_id=data['instagram'][i]['id'],
                instagram_user_name=data['instagram'][i]['username']
            )
            ad_account.instagrams.append(instagram)

    if 'applications' in data:
        for i in (range(len(data['applications']))):
            application = Application(
                app_id=data['applications'][i]['id'],
                app_name=data['applications'][i]['name']
            )
            ad_account.applications.append(application)

    db.session.add(user)
    db.session.commit()


def get_instagram_info(search_ad_account_id, response):
    r = requests.get(
        "{}/act_{}/instagram_accounts?access_token={}&fields=username,id".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()

    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'username': r['data'][i]['username']
            })

        response['instagram'] = instances
    return response


def get_ad_pixel_info(search_ad_account_id, response):
    r = requests.get(
        "{}/act_{}/adspixels?access_token={}&fields=id,name".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()

    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['ad_pixel'] = instances
    return response


def promote_pages(search_ad_account_id, response):
    r = requests.get(
        "{}/act_{}/promote_pages?access_token={}".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()

    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['promote_pages'] = instances
    return response


def get_applications(search_ad_account_id, response):
    r = requests.get(
        "{}/act_{}/applications?access_token={}&fields=name".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()

    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['applications'] = instances
    return response


def get_offline_conversion_data_sets(search_ad_account_id, response):
    r = requests.get(
        "{}/act_{}/offline_conversion_data_sets?access_token={}&fields=name".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()

    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['offline_conversion_data'] = instances
    return response


def get_custom_audience(search_ad_account_id, response):
    r = requests.get(
        "{}/act_{}/customaudiences?access_token={}&fields=id,name".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()
    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['custom_audience'] = instances
    return response


def get_target_audience(search_ad_account_id, response, q):
    r = requests.get(
        "{}/act_{}/targetingsearch?access_token={}&q={}&fields=id,name,type,audience_size".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token'],
            q
        )).json()
    print(r)
    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name'],
                'type': r['data'][i]['type'],
                'audience_size': r['data'][i]['audience_size']
            })

        response['target_audience'] = instances
    return response


if __name__ == '__main__':
    app.run()
