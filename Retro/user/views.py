
### in views.py #####
from django.shortcuts import render,redirect

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate,login as auth_user,logout
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from . import token as token_
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail

# Create your views here.

####### Fonction de recuperation et de traitement des données en cas de post ###############
def email_is_valide(email):
    '''
        Retourne True si l'email est correct sinon False
    '''
    try:
        validate_email(email)
    except:
        return False
    else:
        return True


def register(request):
    message, is_post, success = "", False, False
    if request.method == 'POST':
        is_post = True
        # récupération des données (les valeurs entre parenthèses 
        # correspondent au name de nom input dans le html ##
        
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('name')
        email = request.POST.get('email')
        passe = request.POST.get('pass')
        repass = request.POST.get('repass')
        
        ### Verifie d'abord que les premiers champs sont correctement renseignés
        if not first_name or first_name.isspace() or not last_name or last_name.isspace() :
            message = 'Veuillez renseigner correctement les champs'
        
        # Verifie l'email avec une fonction externe pour plus de lisibilité
        elif not email_is_valide(email):
            message = 'Email incorrect'
    
        elif passe != repass:
            message = "mot de passe incorrect "

        else:
            # Verifie si un utilisateur possede le meme username ou email
            # En retournant le premier utilisateur qui possede ce username ou cette email
            # NB: Cette methode ne leve pas d'exception donc pas besoin de {try:except}
            exist_user_by_username = User.objects.filter(username=username).first()
            exist_user_by_email = User.objects.filter(email=email).first()

            if exist_user_by_username:
                message = 'Un utilisateur possede deja ce username'
            if exist_user_by_email:
                message = 'Adresse email deja utilise'
            else:
                # Maintenant que tout est ok on peut enregistrer l'utilisateur
                success = True

                # Enregistrement de l'utilisateur
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    # desactivation du compte en attendant la confirmation par mail
                    is_active=False
                )
                user.password = passe
                user.set_password(user.password)
                user.save()

                user.user_profil.email = email
                user.save()

                ####### debut de l'envoie de mail de confirmation

                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_.account_activation_token.make_token(user),
                })

                send_mail(subject, message, 'retroproject01@gmail.com', [user.email])

                message = "Merci de vérifier votre email pour la confirmation de votre compte"
                
                ### NB il faut spécifier l'email_backend dans le settings
                ### EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' [Affichage dans la console]
                ### EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' [Envoie reel]

    print('\nMESSAGE:', message, end='\n\n')

    datas = {
        "message":message,
        "success": success
    }
    return render(request,"registration/register.html",datas)

###### connexion de l'utilisateur
def login(request):
    message = ""
    if request.method == 'POST': 
        username = request.POST.get("name")
        password = request.POST.get("password")
        user = authenticate(username=username ,password=password)
        print('PROFILE', user, username, password)
        if user is not None and user.is_active:
            auth_user(request,user)
            
            #### redirection si les infos sont correctes
            return redirect('index')
        else:
            print("login échoué")
            message = "Merci de vérifiez vos informations"

    datas = {
      'message': message
    }
    return render(request,"registration/login.html",datas)


##### déconnexion
def is_deconnexion(request):
    logout(request)
    return redirect('login')



##### activation du mail
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_.account_activation_token.check_token(user, token):
        user.is_active = True
        user.user_profil.email_confirmed = True
        user.save()
        auth_user(request, user)
        return redirect('index')
    else:
        return render(request, 'invalide_token.html')
        
