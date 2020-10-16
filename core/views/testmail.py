from django.http import HttpResponse
from core.utils import Emails
from django.template import loader

def send_test_mail(request):

    #send single recipient

    # Emails(
    #     subject = "My Subject",
    #     message = "My Subject",
    #     from_email = "from@example.com",
    #     recipient_list = "to@example.com",
    #     html_message = "<div> HTML MSG </div>"
    #     ).send()
  

    #send multiple recipient
    # Emails(
    #     subject = "My Subject",
    #     message = "My Subject",
    #     from_email = "from@example.com",
    #     recipient_list = ["to@example.com","to2@example.com"],
    #     html_message = "<div> HTML MSG </div>"
    #     ).send()
    

    #send without from
    # Emails(
    #     subject = "My Subject",
    #     message = "My Subject",
    #     recipient_list = "to@example.com",
    #     html_message = "<div> HTML MSG </div>"
    #     ).send()


    email = Emails(subject = "My Subject",recipient_list = "to@example.com",)
    # email.set_message('test.txt',{ 'username': 'Malkesh' })
    email.set_html_message('welcome/user.html',{ 'username': 'Malkesh' })
    email.send()

    
    
    context = { 'username': 'Malkesh' }
    
    template = loader.get_template('core/emails/html/welcome/user.html')
    return HttpResponse(template.render(context, request))

 
    return HttpResponse('Send Mail is working')