from django.shortcuts import render, redirect
from cart.models import *
from cart.forms import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


def admin_required(function):
   def wrap(request, *args, **kwargs):
       if not request.user.groups.filter(name='Administrador').exists():
           return redirect('home')
       return function(request, *args, **kwargs)

   return wrap


def is_administrador(user):
   if user:
       return user.groups.filter(name='Administrador').exists() == 1
   return False


@user_passes_test(is_administrador)
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
       'productocount': productocount,
       'proveedorescount': Proveedores.objects.all().count(),
       'categoriacount': Category.objects.all().count(),
       'data': zip(ordered_products, ordered_bys, orders),
   }
   return render(request, 'admin/admin_principal.html', context=mydict)


#################### PRODUCTOS #################################

class Admin_ver_productos(ListView):
   model = Product
   template_name = 'admin/admin_ver_productos.html'

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_ver_productos, self).dispatch(request, *args, **kwargs)


class Admin_Agregar_productos(CreateView):
   # specify the model for create view
   model = Product
   form_class = ProductoForm
   # specify the fields to be displayed
   template_name = 'admin/admin_agregar_productos.html'  # templete for updating
   success_url = "/admin_ver_productos"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_Agregar_productos, self).dispatch(request, *args, **kwargs)


class Actualizar_producto(UpdateView):
   model = Product
   fields = "__all__"
   template_name = 'admin/admin_actualizar_productos.html'
   success_url = "/admin_ver_productos"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Actualizar_producto, self).dispatch(request, *args, **kwargs)


class Eliminar_producto(DeleteView):
   model = Product
   template_name = 'admin/admin_eliminar_producto.html'
   success_url = "/admin_ver_productos"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Eliminar_producto, self).dispatch(request, *args, **kwargs)


#################### CATEGORIAS #################################

class Admin_ver_categorias(ListView):
   model = Category
   template_name = 'admin/admin_ver_categorias.html'

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_ver_categorias, self).dispatch(request, *args, **kwargs)


class Admin_Agregar_categorias(CreateView):
   # specify the model for create view
   model = Category
   form_class = CategoriaForm
   # specify the fields to be displayed
   template_name = 'admin/admin_agregar_categoria.html'  # templete for updating
   success_url = "/admin_ver_categorias"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_Agregar_categorias, self).dispatch(request, *args, **kwargs)


class Actualizar_categoria(UpdateView):
   model = Category  # model
   fields = "__all__"  # fields / if you want to select all fields, use "__all__"
   template_name = 'admin/admin_actualizar_categorias.html'  # templete for updating
   success_url = "/admin_ver_categorias"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Actualizar_categoria, self).dispatch(request, *args, **kwargs)


class Eliminar_categoria(DeleteView):
   model = Category
   template_name = 'admin/admin_eliminar_categorias.html'
   success_url = "/admin_ver_categorias"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Eliminar_categoria, self).dispatch(request, *args, **kwargs)


###########################   PROVEEDORES ##################################################

class Admin_ver_proveedores(ListView):
   model = Proveedores
   template_name = 'admin/admin_ver_proveedores.html'

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_ver_proveedores, self).dispatch(request, *args, **kwargs)


class Admin_Agregar_proveedores(CreateView):
   # specify the model for create view
   model = Proveedores
   form_class = ProveedorForm
   # specify the fields to be displayed
   template_name = 'admin/admin_agregar_proveedores.html'  # templete for updating
   success_url = "/admin_ver_proveedores"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_Agregar_proveedores, self).dispatch(request, *args, **kwargs)


class Actualizar_proveedores(UpdateView):
   model = Product  # model
   fields = "__all__"  # fields / if you want to select all fields, use "__all__"
   template_name = 'admin/admin_actualizar_proveedores.html'  # templete for updating
   success_url = "/admin_ver_proveedores"

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Actualizar_proveedores, self).dispatch(request, *args, **kwargs)


###########################   ORDENES  ##################################################
@user_passes_test(is_administrador)
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

   @method_decorator(admin_required)
   def dispatch(self, request, *args, **kwargs):
       return super(Admin_ver_pagos, self).dispatch(request, *args, **kwargs)


###########################  USUARIOS  ##################################################
@user_passes_test(is_administrador)
def Admin_ver_usuarios(request):
   usuarios = User.objects.all().exclude(is_superuser=True)
   usuariosadmin = Administrador.objects.all()

   return render(request, 'admin/admin_ver_usuarios.html', {"usuarios": usuarios, "usuariosadmin": usuariosadmin})

@user_passes_test(is_administrador)
def administrador_signup_view(request):
   userForm = CustomerUserForm()
   customerForm = CustomerForm()
   mydict = {'userForm': userForm, 'customerForm': customerForm}
   if request.method == 'POST':
       userForm = CustomerUserForm(request.POST)
       customerForm = CustomerForm(request.POST)
       if userForm.is_valid() and customerForm.is_valid():
           user = userForm.save()
           user.set_password(user.password)
           user.save()
           customer = customerForm.save(commit=False)
           customer.user = user
           customer.save()
           my_customer_group = Group.objects.get_or_create(name='Administrador')
           my_customer_group[0].user_set.add(user)
       return HttpResponseRedirect('/admin_ver_usuarios')
   return render(request, 'admin/admin_registrar_usuarioadmin.html', context=mydict)

@user_passes_test(is_administrador)
def admin_acutalizar_administradores(request, pk):
   admin = Administrador.objects.get(id=pk)
   user = User.objects.get(id=admin.user.id)

   if request.method == "POST":
       user.username = request.POST.get('username')
       superuser = request.POST.get('superuser')
       user.is_superuser = superuser
       user.is_active = request.POST.get('active')
       user.is_staff = request.POST.get('staff')

       user.save()
       return redirect('admin_ver_usuarios')

   context = {'admin': admin, 'user': user}
   return render(request, 'admin/admin_actualizar_administradores.html', context)








