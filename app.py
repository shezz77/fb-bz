from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():

    return 'Home page'


@app.route('/ad-account-detail')
def ad_account_detail():
    r = requests.get('https://graph.facebook.com/v3.2/act_319269675356107?access_token=EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD&fields=owner,age,account_status,agency_client_declaration,amount_spent,attribution_spec,balance,business,business_city,business_name,business_state,business_zip,created_time,currency,end_advertiser,end_advertiser_name,funding_source,user_role,user_tos_accepted').json()

    return jsonify(r)


@app.route('/custom-audience')
def custom_audience():
    r = requests.get(
        "https://graph.facebook.com/v3.2/act_319269675356107/customaudiences?access_token=EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD&fields=id,name").json()

    return jsonify(r)


@app.route('/instagram')
def instagram():
    r = requests.get(
        "https://graph.facebook.com/v3.2/act_319269675356107/instagram_accounts?access_token=EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD").json()

    return jsonify(r)


@app.route('/ad-pixel')
def ad_pixel():
    r = requests.get(
        "https://graph.facebook.com/v3.2/act_319269675356107/adspixels?access_token=EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD&fields=id,name").json()

    return jsonify(r)


if __name__ == '__main__':
    app.run()
