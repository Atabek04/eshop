from django.shortcuts import render
from main.models import *


def indexHandler(request):
	categories = Category.objects.all()

	context = {
		'categories':categories,
	}	
	return render(request, 'index.html', context)


def productsHandler(request):
	categories = Category.objects.all()
	active_category = None

	search_value = request.GET.get('q', '')
	category_id = int(request.GET.get('category_id', 0))
	print('='*100)
	print(category_id)

	if category_id:
		if search_value:
			products = Product.objects.filter(category__id=category_id).filter(title__contains = search_value)
		else:
			products = Product.objects.filter(category__id=category_id)

		active_category = Category.objects.get(id=category_id)
	else:
		if search_value:
			products = Product.objects.filter(title__contains = search_value)
		else:
			products = Product.objects.all()


	results = len(products)
	context = {
		'products':products,
		'categories':categories,
		'active_category':active_category,
		'results':results,
		'search_value':search_value
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
		arith_mean = int(comments_summa / comments_len *10)/10
		rating_1_progress = int((rating_1/comments_len)*100)
		rating_2_progress = int((rating_2/comments_len)*100)
		rating_3_progress = int((rating_3/comments_len)*100)
		rating_4_progress = int((rating_4/comments_len)*100)
		rating_5_progress = int((rating_5/comments_len)*100)


	context = {
		'product':product,
		'sizes':sizes,
		'colors':colors,
		'prod_img':prod_img,
		'comment_items':comment_items,
		'rating_1':rating_1,
		"rating_2":rating_2,
		"rating_3":rating_3,
		"rating_4":rating_4,
		"rating_5":rating_5,
		"arith_mean":arith_mean,
		"rating_1_progress":rating_1_progress,
		"rating_2_progress":rating_2_progress,
		"rating_3_progress":rating_3_progress,
		"rating_4_progress":rating_4_progress,
		"rating_5_progress":rating_5_progress,

	}
	return render(request, 'product.html', context)
