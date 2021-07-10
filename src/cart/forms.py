from django import forms
from .models import OrderItem, Product, Address, Proveedores, Administrador, Category
from django.contrib.auth import get_user_model

from django.forms import ModelForm

User = get_user_model()


# PARA AGREGAR AL CARRITO
class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label='Cantidad',)

    class Meta:
        model = OrderItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)
        super().__init__(*args, **kwargs)

# CREANDO LOS CAMPOS PARA EL ENVÍO DEL PRODUCTO
class AddressFrom(forms.Form):
    shipping_address_line_1 = forms.CharField(required=False,
        label='Dirección 1',  widget=forms.TextInput(attrs={
        'placeholder': "Ingrese su primera dirección de envio",

    },)
                                              )
    shipping_address_line_2 = forms.CharField(required=False, label='Dirección 2',  widget=forms.TextInput(attrs={
        'placeholder': "Ingrese su segunda dirección de envio",

    }))
    shipping_zip_code = forms.CharField(required=False, label='Codigo Postal' ,  widget=forms.TextInput(attrs={
        'placeholder': "Ingrese su Codigo postal",

    }))
    shipping_departament = forms.CharField(required=False,label="Departamento", max_length=7, disabled=True, widget=forms.TextInput(attrs={
        'placeholder': "Lima",

    }))

    shipping_city = forms.CharField(required=False, label='Ciudad',  widget=forms.TextInput(attrs={
        'placeholder': "Ingrese su ciudad de procedencia",

    }))



    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=False,label='Direcciones Guardadas'
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        if not user_id is None:
            user = User.objects.get(id=user_id)

            shipping_address_qs = Address.objects.filter(
                user=user,
                address_type='S'
            )

            self.fields['selected_shipping_address'].queryset = shipping_address_qs

    def clean(self):
        data = self.cleaned_data

        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('shipping_address_line_1', None):
                self.add_error("shipping_address_line_1", "Please fill in this field")
            if not data.get('shipping_address_line_2', None):
                self.add_error("shipping_address_line_2", "Please fill in this field")
            if not data.get('shipping_zip_code', None):
                self.add_error("shipping_zip_code", "Please fill in this field")
            if not data.get('shipping_city', None):
                self.add_error("shipping_city", "Please fill in this field")


class ProductoForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        help_texts = {
            'active': 'Group to which this message belongs to',
        }
        labels = {
            'active': 'Group to which this message belongs to',
        }


class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedores
        fields = "__all__"


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password','email', 'is_staff']
        widgets = {
            'password': forms.PasswordInput()
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['dirreccion']


class CategoriaForm(ModelForm):
   class Meta:
       model = Category
       fields = "__all__"
       help_texts = {
           'name': 'Por favor ingrese una categoria en texto',

       }
       labels = {
           'name': 'Categoria',

       }
