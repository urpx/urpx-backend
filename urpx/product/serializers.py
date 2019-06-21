from flask_restplus import fields

class ProductSerializers():
    def __init__(self, api):
        self.product_dao = api.model("Product DAO", { 
            'id': fields.String(
                description='Id of product', 
                attribute='rowno'
            ),
            'name': fields.String(
                description='Name of product',
                attribute='prdtnm'
            ),
            'create_year': fields.String(
                description='판매 년도',
                attribute='sellyear'
            ),
            'create_month': fields.String(
                description='판매 월',
                attribute='sellmonth'
            ),
            'image_100px': fields.String(
                description='image 100px',
                attribute='100'
            ),
            'image_200px': fields.String(
                description='image 200px',
                attribute='200'
            ),
        })
