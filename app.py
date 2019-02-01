from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

app.config['access_token'] = 'EAACcz9Hkm2EBAGB5s4B6yFmCmzBKmlBteykwTovxExSM9pqnW5Psbblcg1yDcp8qd9T8Wp9a4EqscT2HeqTyGCBki5ykaa6Y7KjOIKsZCfMxi8EfAjZBYrdGdLJGexYhwOjhjTxaL1YvxoKff9MYcup40Ylx8kl30kjYENRQZDZD'
app.config['facebook_business_api_url'] = 'https://graph.facebook.com/v3.2'


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get-facebook-id-info', methods=['POST'])
def get_facebook_id_info():
    response = {}
    search_ad_account_id = request.form['search']
    q = request.form['q']
    if search_ad_account_id:
        response = get_instagram_info(search_ad_account_id, response)
        response = get_ad_pixel_info(search_ad_account_id, response)
        response = promote_pages(search_ad_account_id, response)
        response = get_applications(search_ad_account_id, response)
        response = get_offline_conversion_data_sets(search_ad_account_id, response)
        response = get_custom_audience(search_ad_account_id, response)
        if q:
            response = get_target_audience(search_ad_account_id, response, q)

    return jsonify(response)


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
