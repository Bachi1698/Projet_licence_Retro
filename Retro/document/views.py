from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from transcription.manager import set_image_line
from . import models
import pytesseract as tess

from django.contrib.auth.decorators import user_passes_test


# def admin_required(user):  
#     if user.is_authenticated and not user.is_staff:
#         return True
#     else:
#         return False


# @user_passes_test(admin_required, login_url='/admin')
def index(request):
    projet = models.Projet.objects.filter(status=True)
    datas = {
        'projet':projet ,
    }
    return render(request,'pages/index.html',datas)


def cluster(request, id_project):
    projet_doc = get_object_or_404(models.Projet, pk=id_project)
    imgs = projet_doc.image_projet.all().order_by('date_add')

    _paginator = Paginator(imgs, 1)
    page = request.GET.get('p')
    try:
        imgs = _paginator.page(page)
    except PageNotAnInteger:
        imgs = _paginator.page(1)
    except EmptyPage:
        imgs = _paginator.page(_paginator.num_pages)

    return render(request,'pages/clustering-avance-2.html', locals())


def cluster_bilan(request, id_project):
    projet_doc = get_object_or_404(models.Projet, pk=id_project)
    imgs = projet_doc.image_projet.all().order_by('date_add')

    _paginator = Paginator(imgs, 1)
    page = request.GET.get('p')
    try:
        imgs = _paginator.page(page)
    except PageNotAnInteger:
        imgs = _paginator.page(1)
    except EmptyPage:
        imgs = _paginator.page(_paginator.num_pages)
    return render(request,'pages/clustering-avance.html', locals())


def doc(request): 
    return render(request,'pages/doc.html', locals())


def single_doc(request, pk):
    projet_doc = get_object_or_404(models.Projet, pk=pk)
    return render(request,'pages/document.html', locals())


@csrf_exempt
def post_datas(request):
    success, message = False, "Echec d'enregistrement"
    nom = request.POST.get("nom")
    images = request.FILES.getlist("image")

    projet = models.Projet(nom=nom)
    projet.save()

    for im in images:
        img = models.Images(image=im, projet=projet)
        img.save()
    
    success, message = True, "Enregistrement effectué"

    datas = {
        'success': success,
        'message': message
    }
    return JsonResponse(datas, safe=False)


@csrf_exempt
def post_image(request):
    # Identifiant de l'image à transcrire
    idt = request.POST.get("idt")

    # Recuperation de l'image correspondante 
    new_image = models.Images.objects.filter(id=idt).first()
    
    if not new_image:
        # Au cas ou l'image n'existe plus dans la BD
        datas = {
            'success': False,
            'message': 'Aucune image trouvé',
        }
    else:
        number = new_image.image_transcription.all().count()
        # verifier si l'image n'a pas deja ete traité
        if number < 1:
            # Transformation de l'image en text
            # et enregistrement du resultat sous forme de lignes
            set_image_line(new_image)

        # récupération des lignes de l'image
        lines = [
            {
                'id': line.id,
                'content': line.contente,
                'checked': line.checked
            } for line in new_image.image_transcription.all().order_by('line_number')
        ]
        datas = {
            'success': True,
            'result': lines
        }
    return JsonResponse(datas, safe=False)


@csrf_exempt
def valider_line(request):
    message = ""
    idt = request.POST.get("idt")
    content = request.POST.get("content")
    print(idt,content)
    line = models.Transcription.objects.filter(id=idt).first()
    if line:
        line.contente = content
        line.checked = True
        line.save()
        success = True
    else:
        message = "une erreur c'est produite"
        success = False

    datas = {
          "success":success,
          "message":message,

    }
    return JsonResponse(datas, safe=False)