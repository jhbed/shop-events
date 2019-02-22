from django.shortcuts import render
import shopify
import os
# Create your views here.

def test_view(request):
    API_KEY = os.environ.get('SHOPIFY_API_KEY')
    PASSWORD = os.environ.get('SHOPIFY_API_PW')
    shop_url = os.environ.get('SHOPIFY_STORE_URL') % (API_KEY, PASSWORD)
    shopify.ShopifyResource.set_site(shop_url)
    shop = shopify.Shop.current()

    #Create a new product
    new_product = shopify.Product()
    new_product.title = "Burton Custom Freestyle 151"
    new_product.product_type = "Snowboard"
    new_product.vendor = "Burton"
    success = new_product.save() #returns false if the record is invalid

    #access a customer
    cust = shopify.Customer.find()

    spec = shopify.Customer.search(query='first_name:Jane')
    #print('cust', cust)


    return render(request, 'shopify_con/test.html', {'cust' : cust, 'spec' : spec})

