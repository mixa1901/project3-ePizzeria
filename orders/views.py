from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum

# import models
from .models import Dinner_platter, Salad, Pasta, Sub_addon, Sub, Topping, Reg_Pizza, Syc_Pizza, Order, Size




# Create your views here.
def index(request):
    # if user is not logged in 
    if not request.user.is_authenticated:
        return redirect('login')
    
    # get cart of particular user
    orders = Order.objects.filter(consumer_id=request.user.id)
    
    # and sum
    total = orders.filter(ordered=False).aggregate(Sum('price'))

    context = {'username': request.user.username,
               'first_name': request.user.first_name,
               'last_name': request.user.last_name,
               'reg_pizza': Reg_Pizza.objects.all(),
               'syc_pizza': Syc_Pizza.objects.all(),
               'dinner_platter': Dinner_platter.objects.all(),
               'salad': Salad.objects.all(),
               'pasta': Pasta.objects.all(),
               'sub_addon': Sub_addon.objects.all(),
               'sub': Sub.objects.all(),
               'topping': Topping.objects.all(),
               'orders': orders,
               'total': total,
               'error': request.session['error']}
        
    return render(request, "orders/index.html", context)


def registration(request):
    request.session['error'] = False
    if request.method == 'POST':
        #lets get user's input
        username, first_name, last_name, email = request.POST["username"], request.POST["f_name"], request.POST["l_name"], request.POST["email"]
        password, re_password = request.POST["password"], request.POST["re_password"]
        
        # make sure if user typed in every field
        if not username or not first_name or not last_name or not email or not password or not re_password:
            return render(request, "orders/register.html", {'message': "ERROR! You didn't fill all of the fields"})
        
        # make sure if passwords identical
        elif password != re_password:
            return render(request, "orders/register.html", {'message': "ERROR! You didn't repeat password correctly"})

        # create a user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        
        # if error is not unique return error
        except:
            return render(request, "orders/register.html", {'message': "ERROR! Username exists"})

        return redirect('index')
    else:
        return render(request, "orders/register.html", {'message': None})


def login_view(request):
    request.session['error'] = False
    if request.method == 'POST':
        # get user's input
        username, password = request.POST['username'], request.POST['password']
        
        # prevent blank fields
        if not username or not password:
            return render(request, "orders/login.html", {'message': "WARNING! You didn't fill all of the fields"})

        # check if user tells correct data
        user = authenticate(request, username=username, password=password)
        
        # login user
        if user is not None:
            login(request, user)
            return redirect('index')
        
        # render error if something went wrong
        else:
            return render(request, "orders/login.html", {'message': "WARNING! User doesn't exist or password doesn't match"})

    else:
        return render(request, "orders/login.html", {'message': None})


def logout_view(request):
    request.session['error'] = False
    logout(request)
    return render(request, "orders/login.html", {'message': "Logged out"})


def order(request, dish, kindid):
    request.session['error'] = False
    if dish == "Salad" or dish == "Pasta":
                
        # get info about salad from menus objects
        dish_object = Salad.objects.get(pk=kindid) if dish == "Salad" else Pasta.objects.get(pk=kindid)
        
        # order in particular object
        d = Order(consumer = request.user, dish = dish, kind = dish_object.name, price = dish_object.price)
        d.save()

        return redirect('index')

    elif dish == "Dinner_platter":
        # get info about dinner platter from menus objects
        dinner_platter = Dinner_platter.objects.get(pk=kindid)
        
        # fork when size matters
        if request.GET['size'] == "large":
            price = dinner_platter.price_large
            
            # set size given by user
            size = Size.objects.get(name=request.GET['size'])
        else:
            price = dinner_platter.price_small
           
            # set size given by user
            size = Size.objects.get(name=request.GET['size'])
        # add order objects into DB
        d = Order(consumer = request.user, dish = "Dinner platter", kind =  dinner_platter.name, price = price, size = size)
        d.save()

        return redirect('index')

    elif dish == "Sub":
        # get info about sub from menus objects
        sub = Sub.objects.get(pk=kindid)
        
        # get list of addonids  given by user
        sub_addons = request.GET.getlist('addon')
        
        # get addons via given ids
        sub_addons = [Sub_addon.objects.get(pk=i) for i in sub_addons]

        # get all prices of these addons
        sub_addons_prices = [i.price for i in sub_addons]

        # fork when size matters
        if request.GET['size'] == "large":
            price = sub.price_large + sum(sub_addons_prices)
            
            # set size given by user
            size = Size.objects.get(name=request.GET['size'])
        else:
            price = sub.price_small + sum(sub_addons_prices)
           
            # set size given by user
            size = Size.objects.get(name=request.GET['size'])
        # add order objects into DB
        d = Order(consumer = request.user, dish = dish, kind =  sub.name, price = price, size = size)
        d.save()
        
        # add addons to orders 
        d.addon.add(*sub_addons)
        d.save()

        return redirect('index')

    elif dish == "Syc_pizza" or dish == "Reg_pizza":
        # get info about sicilian pizza from menus objects
        if dish == "Syc_pizza":
            dish_name = "Sicilian pizza"
            pizza = Syc_Pizza.objects.get(pk=kindid)
        else:
            dish_name = "Regular pizza"
            pizza = Reg_Pizza.objects.get(pk=kindid)
        
        
        # set price and size of pizza
        if request.GET['size'] == "large":
            price = pizza.price_large
            
            # set size given by user
            size = Size.objects.get(name=request.GET['size'])
        else:
            price = pizza.price_small
        
            # set size given by user
            size = Size.objects.get(name=request.GET['size'])

        # next steps depend on kind of choosen pizza
        if pizza.amount_toppings == 0:
           
            d = Order(consumer = request.user, dish = dish_name, kind = pizza.kind, price = price, size = size)
            d.save()

            return redirect('index')
        else:
            # get all given toppings
            toppingsid = request.GET.getlist('topping')
            
            # in case if user haven't choosed all recquired toppings
            if '' in toppingsid:
                request.session['error'] = "You have to set all required toppings in order to get perfect pizza :3"
                return redirect('index')

            # prevent case when user chooses same toppoings
            if len(toppingsid) != len(set(toppingsid)):
                request.session['error'] = "You have to choose different toppings in order to get perfect pizza :3"
                return redirect('index')


            # get objects from given ids
            toppings_objects = [Topping.objects.get(pk=i) for i in toppingsid]

            # add order objects into DB
            d = Order(consumer = request.user, dish = dish_name, kind = pizza.kind, price = price, size = size)
            d.save()
            
            # add addons to orders 
            d.topping.add(*toppings_objects)
            d.save()

            return redirect('index')



def order_delete(request, orderid):
    request.session['error'] = False

    # delete choosen order
    order = Order.objects.get(id=orderid)
    order.delete()
    
    return redirect(request.GET['path'])

def purchase(request):
    if request.method == 'POST':
        orders = Order.objects.filter(consumer_id=request.user.id)
        ordered_orders = orders.filter(ordered=False)
        for i in ordered_orders:
            i.ordered = True
            i.save()

        request.session['error'] = "The order has been placed"
        return redirect('index')
    else:
        # get cart of particular user
        orders = Order.objects.filter(consumer_id=request.user.id)
        
        # and sum
        total = orders.filter(ordered=False).aggregate(Sum('price'))
        if total['price__sum'] == None:
            return redirect('index')

        context = {'username': request.user.username,
                   'orders': orders,
                   'total': total,
                   }
        return render(request, "orders/cart.html", context)

def myorders(request):
    orders = Order.objects.filter(consumer_id=request.user.id)
    context = {'username': request.user.username,
               'orders': orders}
    return render(request, "orders/orders.html", context)