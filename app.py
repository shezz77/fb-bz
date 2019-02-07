from flask import Flask, jsonify, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
import json

app = Flask(__name__)

app.config['access_token'] = 'EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD'
app.config['facebook_id'] = ''
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cbymbzyosnqsdg:045013faa43ffb6466cd3b5e6fd0ae328930ac8f3d0de8dc96bdff79c74cbfe8@ec2-107-22-162-8.compute-1.amazonaws.com:5432/devgm2sk4pajqt'

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(
#     POSTGRES['user'],
#     POSTGRES['pw'],
#     POSTGRES['host'],
#     POSTGRES['port'],
#     POSTGRES['db']
# )
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


class FbTargeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_type = db.Column(db.String(50), nullable=True)
    common_name = db.Column(db.String(50), nullable=True)
    section_id = db.Column(db.String(50), nullable=True)
    section_name = db.Column(db.String(50), nullable=True)
    field_id = db.Column(db.String(50), nullable=True)
    field_name = db.Column(db.String(50), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    path = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    city_id = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    region_id = db.Column(db.String(50), nullable=True)
    region = db.Column(db.String(50), nullable=True)
    country_code = db.Column(db.String(50), nullable=True)
    country_name = db.Column(db.String(50), nullable=True)
    audience_size = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'db_type': self.db_type,
            'common_name': self.common_name,
            'section_id': self.section_id,
            'section_name': self.section_name,
            'field_id': self.field_id,
            'field_name': self.field_name,
            'type': self.type,
            'path': self.path,
            'name': self.name,
            'city_id': self.city_id,
            'city': self.city,
            'region_id': self.region_id,
            'region': self.region,
            'country_code': self.country_code,
            'country_name': self.country_name,
            'audience_size': self.audience_size,
        }


@app.route('/user-info')
def user_info():
    app.config['access_token'] = request.args.get('access_token')
    app.config['facebook_id'] = request.args.get('id')
    return render_template('index.html')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/facebook-search', methods=['GET'])
def facebook_search():
    return render_template('facebook_search.html')


@app.route('/get-facebook-id-info', methods=['GET'])
def get_facebook_id_info():
    response = {}
    search_ad_account_id = app.config['facebook_id']
    # q = request.form['q']
    if search_ad_account_id:
        response = get_ad_accounts(search_ad_account_id, response)
        response = get_businesses(search_ad_account_id, response)
        response = get_pages(search_ad_account_id, response)

        # response = get_instagram_info(search_ad_account_id, response)
        # response = get_ad_pixel_info(search_ad_account_id, response)
        # response = promote_pages(search_ad_account_id, response)
        # response = get_applications(search_ad_account_id, response)
        # response = get_offline_conversion_data_sets(search_ad_account_id, response)
        # response = get_custom_audience(search_ad_account_id, response)
        # if q:
        #     response = get_target_audience(search_ad_account_id, response, q)
        save_user_info(response, search_ad_account_id)

    return jsonify(response)


def save_user_info(data, facebook_id):
    user = User(facebook_id=facebook_id)
    ad_account = AdAccount.query.filter_by(ad_account_id=facebook_id).first()
    print(ad_account)

    if not ad_account:
        ad_account = AdAccount(ad_account_id=facebook_id)
        user.ad_accounts.append(ad_account)

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


def get_ad_accounts(search_ad_account_id, response):
    r = requests.get(
        "{}/{}/adaccounts?access_token={}".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()

    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id']
            })

        response['ad_account'] = instances
    return response


def get_pages(search_ad_account_id, response):
    r = requests.get(
        "{}/{}/accounts?access_token={}".format(
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

        response['page'] = instances
    return response


def get_businesses(search_ad_account_id, response):
    r = requests.get(
        "{}/{}/businesses?access_token={}".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()
    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            response = get_owned_apps(r['data'][i]['id'], response)
            response = get_client_apps(r['data'][i]['id'], response)
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['business'] = instances
    return response


def get_owned_apps(business_id, response):
    r = requests.get(
        "{}/{}/owned_apps?access_token={}".format(
            app.config['facebook_business_api_url'],
            business_id,
            app.config['access_token']
        )).json()
    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['app'] = instances
    return response


def get_client_apps(business_id, response):
    r = requests.get(
        "{}/{}/client_apps?access_token={}".format(
            app.config['facebook_business_api_url'],
            business_id,
            app.config['access_token']
        )).json()
    if 'data' in r:
        instances = []
        for i in (range(len(r['data']))):
            instances.append({
                'id': r['data'][i]['id'],
                'name': r['data'][i]['name']
            })

        response['client_app'] = instances
    return response


def get_instagram_info(search_ad_account_id, response):
    r = requests.get(
        "{}/{}/instagram_accounts?access_token={}&fields=username,id".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token']
        )).json()
    print(r)
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
        "{}/{}/adspixels?access_token={}&fields=id,name".format(
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
        "{}/{}/promote_pages?access_token={}".format(
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
        "{}/{}/applications?access_token={}&fields=name".format(
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
        "{}/{}/offline_conversion_data_sets?access_token={}&fields=name".format(
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
        "{}/{}/customaudiences?access_token={}&fields=id,name".format(
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
        "{}/{}/targetingsearch?access_token={}&q={}&fields=id,name,type,audience_size".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token'],
            q
        )).json()
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


@app.route('/search-city')
def search_city():
    response = dict()
    query = request.args.get('q')
    r = requests.get(
        "https://graph.facebook.com/v2.10/search?access_token={}&type=adgeolocation&q={}".format(
            app.config['access_token'],
            query
        )).json()
    db_search = FbTargeting.query.filter(FbTargeting.field_name.like('%'+query+'%')).all()
    response['local'] = [obj.serialize() for obj in db_search]
    response['facebook'] = r
    return jsonify(response)


@app.route('/select-location', methods=['POST'])
def selected_location_save():
    response = {
        'message': 'Entry already added to db',
        'added': False
    }
    selected_location_obj = request.json
    fb_targeting = FbTargeting.query.filter_by(
        field_name=selected_location_obj['name'],
        type=selected_location_obj['type']).first()

    if not fb_targeting:
        fb_targeting = FbTargeting(
            section_id="sec:loc",
            section_name="location",
            field_id=selected_location_obj['name'][:3],
            field_name=selected_location_obj['name'],
            type=selected_location_obj['type'],
            region_id=selected_location_obj['region_id'],
            region=selected_location_obj['region'],
            country_code=selected_location_obj['country_code'],
            country_name=selected_location_obj['country_name']
        )
        db.session.add(fb_targeting)
        db.session.commit()
        response['message'] = "New entry added"
        response['added'] = True
    return jsonify(response)


@app.route('/search-interest')
def search_interest():
    q = request.args.get('q')
    response = dict()
    search_ad_account_id = '832687727072200'
    r = requests.get(
        "{}/{}/targetingsearch?access_token={}&q={}&fields=id,name,type,audience_size".format(
            app.config['facebook_business_api_url'],
            search_ad_account_id,
            app.config['access_token'],
            q
        )).json()

    db_search = FbTargeting.query.filter(FbTargeting.field_name.like('%'+q+'%')).all()
    response['local'] = [obj.serialize() for obj in db_search]
    response['facebook'] = r
    return jsonify(response)


@app.route('/select-interest', methods=['POST'])
def selected_interest_save():
    response = {
        'message': 'Entry already added to db',
        'added': False
    }
    selected_interest_obj = request.json
    fb_targeting = FbTargeting.query.filter_by(
        field_name=selected_interest_obj['name'],
        type=selected_interest_obj['type']).first()

    if not fb_targeting:
        fb_targeting = FbTargeting(
            section_id="sec:loc",
            section_name="interest",
            field_id=selected_interest_obj['name'][:3],
            field_name=selected_interest_obj['name'],
            type=selected_interest_obj['type'],
        )
        db.session.add(fb_targeting)
        db.session.commit()
        response['message'] = "New entry added"
        response['added'] = True
    return jsonify(response)


if __name__ == '__main__':
    app.run()
