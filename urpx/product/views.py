from flask import request, jsonify, current_app
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from werkzeug.exceptions import BadRequest, InternalServerError
import xml.etree.ElementTree as ET

from .models import Product
from .serializers import ProductSerializers
from urpx.exceptions import InvalidUsage
from urpx.extensions import db, cache

import os
import json
import requests
import urllib.parse
import random

api = Namespace('Product API', description='Products related operation')
serializers = ProductSerializers(api)

auth_parser = api.parser()
auth_parser.add_argument('Authorization', location='headers', 
    required=True, help='Bearer <access_token>')

SUPPORT_REASON = {
    'cost': '금액',
    'amount': '수량',
}


@api.route('api/products/recommends')
@api.expect(auth_parser, validate=True)
class ProductRecommendsResource(Resource):
    @jwt_required
    @api.marshal_list_with(serializers.product_dao)
    @cache.cached(timeout=60 * 60 * 24)
    def get(self):
        rank = 50
        round_cnt = 50

        try:
            items = get_origin_products_by_openapi('amount')
            for i in range(len(items)): #range(round_cnt):
                suffle = random.randrange(0, rank)
                items[i], items[suffle] = items[suffle], items[i]
        except Exception as ex:
            raise InternalServerError(ex)
        
        return items[:rank]


@api.route('api/products/<reason>')
@api.param('reason', description='product ranking reason, support reason [cost, amount]')
@api.expect(auth_parser, validate=True)
class ProductsResource(Resource):
    @jwt_required
    @api.marshal_list_with(serializers.product_dao)
    def get(self, reason):
        if not is_support_reason(reason):
            raise InvalidUsage.not_support_product_reason()

        try:
            items = get_origin_products_by_openapi(reason)
        except Exception as ex:
            raise InternalServerError(ex)

        return items


OPEN_API_URL = 'http://openapi.mnd.go.kr'
OPEN_API_TYPE = 'json'
SERVICE_NAME = 'DS_MND_PX_PARD_PRDT_INFO'


def is_support_reason(reason):
    return True if reason in SUPPORT_REASON.keys() else False


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_JSON_PATH = os.path.join(BASE_DIR, 'data/products.json')

@cache.cached(timeout=60 * 60 * 24 * 30)
def get_origin_products_by_openapi(reason):
    openapi_key = current_app.config['API_KEY']
    request_url = OPEN_API_URL + '/' +  \
                  openapi_key + '/' + \
                  OPEN_API_TYPE + '/' + \
                  SERVICE_NAME + '/' + \
                  '0/' + '960'
    
    res = requests.get(request_url)
    # res_json = res.json()
    with open(PRODUCT_JSON_PATH, 'r') as f:
        res_json = json.load(f)
    
    items = res_json[SERVICE_NAME]['row']
    result = []

    for item in items:
        if item['seltnstd'] == SUPPORT_REASON[reason]:
            item.update(get_product_image_url(item['prdtnm']))
            result.append(item)

    return result


ELEVEN_OPEN_API_URL = 'https://openapi.11st.co.kr/openapi/OpenApiService.tmall'


def get_product_image_url(product_name):
    openapi_key = current_app.config['ELEVEN_API_KEY']
    params = {'key': openapi_key, 'apiCode': 'ProductSearch', 'keyword': product_name}

    res = requests.get(ELEVEN_OPEN_API_URL, params=params)

    xmlp = ET.XMLParser(encoding="iso-8859-5")
    xmlroot = ET.fromstring(res.content, parser=xmlp)
    
    products = xmlroot.find('Products')
    for product in products.iter('Product'):
        return {
            '100': product.find('ProductImage100').text,
            '200': product.find('ProductImage200').text
        }

    return {}