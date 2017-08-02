from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    def __init__(self,request):

        '''
        Initialize the cart
        '''
        self.session=request.session
        cart=self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        self.cart=cart

    def add (self,product,quantity=1,update_quantity=False):
        """
        Add a product to the cart or update its quantity
        """
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0,
                                   'price':str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity']=quantity
        else:
            self.cart[product_id]['quantity']+=quantity
        self.save()

    def save(self):
        #更新购物车
        self.session[settings.CART_SESSION_ID]=self.cart
        #mark the session as 'modified' ro make sure it is saved
        self.session.modified=True

    def remove(self,product):
        """
        从购物车删除物品
        """
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        从数据中迭代的方式展示购物车中的物品
        """
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price']=item['price']*item['quantity']
            yield item
    def __len__(self):
        """
        统计购物车中物品总数
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

        self.session.modified=True




