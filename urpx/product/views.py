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

import asyncio
import aiohttp
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

        try:
            items = filter_products_json(lambda item: is_equal_reason(item, 'amount'))
            result = get_products_by_range(items, 0, rank)
            for i in range(len(result)):
                suffle = random.randrange(0, rank)
                result[i], result[suffle] = result[suffle], result[i]
        except Exception as ex:
            raise InternalServerError(ex)
        
        return result[:rank]


@api.route('api/products/<reason>')
@api.param('reason', description='product ranking reason, support reason [cost, amount]')
@api.doc(params={'offset': 'offset of pagination', 'count': 'count of pagination'})
@api.expect(auth_parser, validate=True)
class ProductsResource(Resource):
    @jwt_required
    @api.marshal_list_with(serializers.product_dao)
    def get(self, reason):
        if not is_support_reason(reason):
            raise InvalidUsage.not_support_product_reason()

        offset = request.args.get('offset')
        count = request.args.get('count')

        try:
            items = filter_products_json(lambda item: is_equal_reason(item, reason))
            result = get_products_by_range(items, int(offset), int(count))
        except Exception as ex:
            raise InternalServerError(ex)

        return result


@api.route('api/products/<reason>/<year>/<month>')
@api.param('reason', description='product ranking reason, support reason [cost, amount]')
@api.param('year', description='year')
@api.param('month', description='month')
@api.doc(params={'offset': 'offset of pagination', 'count': 'count of pagination'})
@api.expect(auth_parser, validate=True)
class ProductsDateResource(Resource):
    @jwt_required
    @api.marshal_list_with(serializers.product_dao)
    def get(self, reason, year, month):
        if not is_support_reason(reason):
            raise InvalidUsage.not_support_product_reason()

        offset = request.args.get('offset')
        count = request.args.get('count')

        if len(month) < 2:
            month = '0' + month

        try:
            items = filter_products_json(lambda product: is_equal_reason(product, reason) and 
                product['sellyear'] == year and product['sellmonth'] == month)
            result = get_products_by_range(items, int(offset), int(count))
        except Exception as ex:
            raise InternalServerError(ex)

        return result


def is_support_reason(reason):
    return True if reason in SUPPORT_REASON.keys() else False


def is_equal_reason(item, reason):
    return item['seltnstd'] == SUPPORT_REASON[reason]



SERVICE_NAME = 'DS_MND_PX_PARD_PRDT_INFO'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_JSON_PATH = os.path.join(BASE_DIR, 'data/products.json')


with open(PRODUCT_JSON_PATH, 'r') as f:
    product_json = json.load(f)


@cache.cached(timeout=60 * 60 * 24 * 30)
def filter_products_json(filter):
    items = product_json[SERVICE_NAME]['row']
    result = []

    for item in items:
        if filter(item):
            result.append(item)

    return result

# @cache.cached(timeout=60 * 60 * 24 * 30)
def get_products_by_range(items, offset, count):
    result = []
    tasks = []

    for i in range(offset, offset + count):
        if i >= len(items):
            break

        item = items[i]

        tasks.append(update_product_image_url(item['prdtnm'], item))
        result.append(item)

    if len(result) <= 0:
        return []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(asyncio.wait(tasks))

    return result


ELEVEN_OPEN_API_URL = 'https://openapi.11st.co.kr/openapi/OpenApiService.tmall'


async def update_product_image_url(product_name, item):
    item['100'] = item['200'] = ''

    openapi_key = current_app.config['ELEVEN_API_KEY']
    params = {
        'key': openapi_key, 
        'apiCode': 'ProductSearch', 
        'keyword': product_name
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(ELEVEN_OPEN_API_URL, params=params) as resp:
            text = await resp.text()

    xmlp = ET.XMLParser(encoding="iso-8859-5")
    xmlroot = ET.fromstring(text, parser=xmlp)
    
    products = xmlroot.find('Products')
    for product in products.iter('Product'):
        item['100'] = product.find('ProductImage100').text
        item['200'] = product.find('ProductImage200').text
        break