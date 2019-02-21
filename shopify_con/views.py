from django.shortcuts import render
import shopify
# Create your views here.

def test_view(request):
    API_KEY = 'f8a254a58926ccb4069930006d9fe034'
    PASSWORD = '61145f93d4f6b6c6a4fd984e908dd5b6'
    shop_url = "https://%s:%s@jakeybdev.myshopify.com/admin" % (API_KEY, PASSWORD)
    shopify.ShopifyResource.set_site(shop_url)
    shop = shopify.Shop.current()

    # Create a new product
    # new_product = shopify.Product()
    # new_product.title = "Burton Custom Freestyle 151"
    # new_product.product_type = "Snowboard"
    # new_product.vendor = "Burton"
    # success = new_product.save() #returns false if the record is invalid

    #access a customer
    cust = shopify.Customer.find()

    spec = shopify.Customer.search(query='first_name:Jane')
    #print('cust', cust)


    return render(request, 'shopify_con/test.html', {'cust' : cust, 'spec' : spec})

