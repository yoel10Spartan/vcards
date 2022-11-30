import logging
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .exceptions import ErrorDetail
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(email: str, context: dict):
    try:
        template = get_template('email/index.html')
        
        content = template.render(context)
        
        email = EmailMultiAlternatives(
            'Mensaje de GACards',
            'Mensaje de GACards',
            settings.EMAIL_HOST_USER,
            [email]
        )
        email.attach_alternative(content, 'text/html')
        email.send()
    except:
        raise ErrorDetail(detail='Error when sending mail', code='400')


@api_view(['POST'])
def send(request):
    email = request.data['email']
    nameForm = request.data['nameForm']
    emailForm = request.data['emailForm']
    descriptionForm = request.data['descriptionForm']

    if not all([email, nameForm, emailForm, descriptionForm]):
        raise ErrorDetail(detail='Incomplete fields', code='400')

    context = {
        'email': email,
        'name': nameForm,
        'emailForm': emailForm,
        'description': descriptionForm
    }

    send_email(email, context)

    return Response({'ok': True})


@api_view(['GET'])
def getUsers(request):
    file = open(os.getcwd() + '/data.json', 'r')
    data = file.read()
    users = json.loads(data)
    file.close()
    return Response(users)


@api_view(['GET'])
def getLocations(request):
    file = open(os.getcwd() + '/locations.json', 'r')
    data = file.read()
    loc = json.loads(data)
    file.close()
    return Response(loc)