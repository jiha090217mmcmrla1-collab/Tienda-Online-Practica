from django.shortcuts import render, redirect
#importar un modulo
from django.http import HttpResponse
from .models import Store, Product
from .forms import newstoreform
from .forms import newproductform
from .forms import newcontactform
from email.message import EmailMessage
import smtplib




#Función saludar 

def saludar(request):
    return render(request, 'home.html')


#Función info
def info(request):
    nombre = ['alondra']
    return render(request, 'info.html', {
        'name': nombre
    })


#Función stores
def Stores_view(request):
    s=Store.objects.all()
    return render (request, 'stores.html',{
       'stores': s
    })
def Products_view(request):
    p=Product.objects.all()
    return render(request, 'products.html',{
        'products':p
    })

def create_store(request):
    if request.method=='GET':
        return render(request, 'create_store.html',{
        'forms':newstoreform()
    })
    else:
        name = request.POST.get('name')
        description = request.POST.get('description')

        Store.objects.create(
            name=name,
            description=description 
        )
        return redirect('store')


from django.http import HttpResponse

def create_product(request):
    if request.method == 'GET':
        return render(request, 'create_product.html', {
            'forms': newproductform()   
        })
    else:
        print(request.POST)

        try:
            a = Store.objects.get(name=request.POST['store'])
        except Store.DoesNotExist:
            return HttpResponse("La tienda no existe", status=400)

        Product.objects.create(
            title=request.POST['title'],
            price=request.POST['price'],
            store_id=a.id
        )

        return redirect('products')

    
def details(request, id):
    store = Store.objects.get(id=id)
    products = Product.objects.filter(store_id=id)

    return render(request, 'details.html', {
        'store': store,
        'products': products
    })

def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': newcontactform()})
    else:
        try:
            print("=== INICIANDO ENVÍO DE CORREO ===")
            remitente = "alondrajinenez462@gmail.com"
            destinatario = request.POST['email']
            password_app = "123456789"  

            mensaje = """Saludos, gracias por contactarnos. Nuestros productos son los siguientes"""

            for i in Product.objects.all():
                mensaje = mensaje + ' - $' + str(i.price) +'\n'
            
            print(f"Remitente: {remitente}")
            print(f"Destinatario: {destinatario}")
            print(f"Longitud contraseña: {len(password_app)}")
            
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = "Prueba Django"
            email.set_content("Buen día le enviamos nuestros productos")
            
            print("Conectando a Gmail...")
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            
            print("Intentando login...")
            smtp.login(remitente, password_app)
            print("✅ Login exitoso!")
            
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()
            print("✅ Correo enviado exitosamente!")
            
            return redirect('home')
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return render(request, 'contact.html', {
                'form': newcontactform(),
                'error': f'Error: {str(e)}'
            })

#Función despedirse
def despedirse(request):
    return HttpResponse('<h2>¡Adios!</h2>')


# Create your views here.
