from django.shortcuts import render, redirect
from cart.models import *
from cart.forms import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.decorators import user_passes_test

def adminprincipal(request):
    customercount = User.objects.all().count()
    productocount = Product.objects.all().count()
    # para tablas de pedidos recientes
    orders = OrderItem.objects.all()
    ordered_products = []
    ordered_bys = []
    for order in orders:
        ordered_product = Product.objects.all().filter(id=order.product.id)
        ordered_by = Order.objects.all().filter(id=order.order.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict = {
        'customercount': customercount,
        'productocount':productocount,
        'data': zip(ordered_products, ordered_bys, orders),
    }
    return render(request, 'admin/admin_principal.html', context=mydict)


class Admin_ver_productos(ListView):
    model = Product
    template_name = 'admin/admin_ver_productos.html'


class Admin_Agregar_productos(CreateView):
    # specify the model for create view
    model = Product
    form_class = ProductoForm
    # specify the fields to be displayed
    template_name = 'admin/admin_agregar_productos.html'  # templete for updating
    success_url = "/admin_ver_productos"


class Actualizar_producto(UpdateView):
    model = Product  # model
    fields = "__all__"  # fields / if you want to select all fields, use "__all__"
    template_name = 'admin/admin_actualizar_productos.html'  # templete for updating
    success_url = "/admin_ver_productos"


class Eliminar_producto(DeleteView):
    model = Product
    template_name = 'admin/admin_eliminar_producto.html'
    success_url = "/admin_ver_productos"

###########################   PROVEEDORES ##################################################

class Admin_ver_proveedores(ListView):
    model = Proveedores
    template_name = 'admin/admin_ver_proveedores.html'


class Admin_Agregar_proveedores(CreateView):
    # specify the model for create view
    model = Proveedores
    form_class = ProveedorForm
    # specify the fields to be displayed
    template_name = 'admin/admin_agregar_proveedores.html'  # templete for updating
    success_url = "/admin_ver_proveedores"


class Actualizar_proveedores(UpdateView):
    model = Product  # model
    fields = "__all__"  # fields / if you want to select all fields, use "__all__"
    template_name = 'admin/admin_actualizar_proveedores.html'  # templete for updating
    success_url = "/admin_ver_proveedores"


###########################   ORDENES  ##################################################
def Admin_ver_ordenes(request):
    customercount = User.objects.all().count()
    # para tablas de pedidos recientes
    orders = OrderItem.objects.all()
    ordered_products = []
    ordered_bys = []
    for order in orders:
        ordered_product = Product.objects.all().filter(id=order.product.id)
        ordered_by = Order.objects.all().filter(id=order.order.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict = {
        'customercount': customercount,
        'data': zip(ordered_products, ordered_bys, orders),
    }
    return render(request, 'admin/admin_ver_ordenes.html', context=mydict)

###########################  PAGOS  ##################################################
class Admin_ver_pagos(ListView):
    model = Payment
    template_name = 'admin/admin_ver_pagos.html'


###########################  USUARIOS  ##################################################
def Admin_ver_usuarios(request):
    usuarios = User.objects.all()
    usuariosadmin = Administrador.objects.all()

    return render(request,'admin/admin_ver_usuarios.html',{"usuarios":usuarios, "usuariosadmin":usuariosadmin })


def administrador_signup_view(request):
    userForm = CustomerUserForm()
    customerForm = CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = CustomerUserForm(request.POST)
        customerForm = CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='Administrador')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('admin_ver_usuarios')
    return render(request, 'admin/admin_registrar_usuarioadmin.html', context=mydict)