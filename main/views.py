from math import prod
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from main.models import *
from django.http import JsonResponse





def indexHandler(request):
    categories = Category.objects.all()

    cart = {
        'info': {},
        'product_count': 0,
        'products': [],
        'price': 0
    }

    open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
    if open_carts:
        open_cart = open_carts[0]
        cart_items = CartItem.objects.filter(cart__id=open_cart.id).filter(status=0)
        cart['info'] = open_cart
        if cart_items:
            cart['product_count'] = len(cart_items)
            cart['products'] = cart_items

    context = {
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'index.html', context)


def productsHandler(request):
    categories = Category.objects.all()
    active_category = None

    search_value = request.GET.get('q', '')
    category_id = int(request.GET.get('category_id', 0))

    if category_id:
        if search_value:
            products = Product.objects.filter(category__id=category_id).filter(title__contains=search_value)
        else:
            products = Product.objects.filter(category__id=category_id)

        active_category = Category.objects.get(id=category_id)
    else:
        if search_value:
            products = Product.objects.filter(title__contains=search_value)
        else:
            products = Product.objects.all()
    results = len(products)

    cart = {
        'info': {},
        'product_count': 0,
        'products': [],
        'price': 0
    }

    open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)

    if open_carts:
        open_cart = open_carts[0]
        cart_items = CartItem.objects.filter(cart__id=open_cart.id).filter(status=0)
        cart['info'] = open_cart
        if cart_items:
            cart['product_count'] = len(cart_items)
            cart['products'] = cart_items

    
    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'results': results,
        'search_value': search_value,
        'cart': cart
    }
    return render(request, 'products.html', context)


def productHandler(request, product_id):
    product = Product.objects.filter(id=int(product_id))
    sizes = Size.objects.all()
    colors = Color.objects.all()
    prod_img = ProductImage.objects.filter(product__id=product_id)
    comment_items = CommentItem.objects.filter(product__id=product_id)

    comments_len = 0
    comments_summa = 0
    rating_1 = 0
    rating_2 = 0
    rating_3 = 0
    rating_4 = 0
    rating_5 = 0

    rating_1_progress = 0
    rating_2_progress = 0
    rating_3_progress = 0
    rating_4_progress = 0
    rating_5_progress = 0
    arith_mean = 0

    for comment in comment_items:
        comments_len += 1
        comments_summa += comment.rating
        if comment.rating == 1:
            rating_1 += 1
        elif comment.rating == 2:
            rating_2 += 1
        elif comment.rating == 3:
            rating_3 += 1
        elif comment.rating == 4:
            rating_4 += 1
        elif comment.rating == 5:
            rating_5 += 1

    if comments_len > 0:
        arith_mean = int(comments_summa / comments_len * 10) / 10
        rating_1_progress = int((rating_1 / comments_len) * 100)
        rating_2_progress = int((rating_2 / comments_len) * 100)
        rating_3_progress = int((rating_3 / comments_len) * 100)
        rating_4_progress = int((rating_4 / comments_len) * 100)
        rating_5_progress = int((rating_5 / comments_len) * 100)

    cart = {
        'info': {},
        'product_count': 0,
        'products': [],
        'price': 0
    }
    open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
    if open_carts:
        open_cart = open_carts[0]
        cart_items = CartItem.objects.filter(cart__id=open_cart.id).filter(status=0)
        cart['info'] = open_cart
        if cart_items:
            cart['products'] = cart_items

    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'prod_img': prod_img,
        'comment_items': comment_items,
        'rating_1': rating_1,
        "rating_2": rating_2,
        "rating_3": rating_3,
        "rating_4": rating_4,
        "rating_5": rating_5,
        "arith_mean": arith_mean,
        "rating_1_progress": rating_1_progress,
        "rating_2_progress": rating_2_progress,
        "rating_3_progress": rating_3_progress,
        "rating_4_progress": rating_4_progress,
        "rating_5_progress": rating_5_progress,
        'cart': cart

    }
    return render(request, 'product.html', context)

def cartHandler(request):
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add_to_cart':
            # product_id = int(request.POST.get('product_id', 0))
            if request.POST.get('product_id') != '':
                product_id = int(request.POST.get('product_id'))
            else:
                product_id = 0
            amount = int(request.POST.get('amount', 0))
            open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
            if not open_carts:
                new_cart = Cart()
                new_cart.session_id = request.session.session_key
                new_cart.save()
            else:
                new_cart = open_carts[0]

            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(product__id=product_id).filter(status=0)
            if cart_items:
                new_cart_item = cart_items[0]
                new_cart_item.amount += amount
                new_cart_item.save()
            else:
                new_cart_item = CartItem()
                new_cart_item.product = Product.objects.get(id=product_id)
                new_cart_item.cart = Cart.objects.get(id=new_cart.id)
                new_cart_item.amount = amount
                new_cart_item.product_price = new_cart_item.product.new_price
                new_cart_item.save()

        elif action == 'remove_from_cart':
            product_id = int(request.POST.get('product_id', 0))
            open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
            if open_carts:
                new_cart = open_carts[0]
            if new_cart:
                cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(product__id=product_id)
                for ci in cart_items:
                    ci.status = -1
                    ci.save()

        elif action == 'checkout':
            open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
            if open_carts:
                new_cart = open_carts[0]
                new_cart.last_name = request.POST.get('last_name', '')
                new_cart.first_name = request.POST.get('first_name', '')
                new_cart.email = request.POST.get('email', '')
                new_cart.address = request.POST.get('city', '')
                new_cart.city = request.POST.get('city', '')
                new_cart.country = request.POST.get('country', '')
                new_cart.zip_code = request.POST.get('zip_code', '')
                new_cart.phone = request.POST.get('phone', '')

                new_cart.status = 1
                new_cart.save()


        if action in ['add_to_cart', 'remove_from_cart']:
            open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
            if open_carts:
                new_cart = open_carts[0]
                cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

                all_sum = 0
                items_count = 0
                for ci in cart_items:
                    all_sum += ci.amount * ci.product_price
                    items_count += ci.amount
                new_cart.orig_price = all_sum
                new_cart.price = all_sum
                new_cart.amount = items_count
                new_cart.save()

        return JsonResponse({'success':True, '_success':True})

    else:
        cart = {}
        cart_items = []

        open_carts = Cart.objects.filter(session_id=request.session.session_key).filter(status=0)
        if open_carts:
            open_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=open_cart.id).filter(status=0)
            cart = open_cart

    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        })