from threading import current_thread
from django.http import HttpResponseGone, HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import  User 
from django.contrib.auth import logout, authenticate,login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# from .application import validate_emails
# from home.functions import handle_uploaded_file
# password for test user is atul$$$***000
# Create your views here.
import csv, io, os
import markdown
from smtplib import SMTP


def get_msg(csv_file, message):
    

    headers = ['Email Address']

    data_set = csv_file
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        required_string = message
        current_email = column[0]
        if check_email(current_email):
            
            for header in headers:
                value = current_email
                required_string = required_string.replace(f'${header}', value)
            yield current_email, required_string


        else:
            print(current_email, " : Not valid")   
   

        
   

def confirm_attachments():
    file_contents = []
    file_names = []
    try:
        for filename in os.listdir('ATTACH'):

            entry = 'N'
            confirmed = False if entry == 'Y' else False
            if confirmed:
                file_names.append(filename)
                with open(f'{os.getcwd()}/ATTACH/{filename}', "rb") as f:
                    content = f.read()
                file_contents.append(content)

        return {'names': file_names, 'contents': file_contents}
    except FileNotFoundError:
        print('No ATTACH directory found...')
  

def send_emails(csv_file, server: SMTP, message, subject, name, sender_email):
    attachments = confirm_attachments()
    sent_count = 0

    for receiver, message in get_msg(csv_file, message):

        multipart_msg = MIMEMultipart("alternative")

        multipart_msg["Subject"] = subject
        multipart_msg["From"] = name + f' <{sender_email}>'
        multipart_msg["To"] = receiver

        text = message
        html = markdown.markdown(text)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        multipart_msg.attach(part1)
        multipart_msg.attach(part2)

        if attachments:
            for content, name in zip(attachments['contents'], attachments['names']):
                attach_part = MIMEBase('application', 'octet-stream')
                attach_part.set_payload(content)
                encoders.encode_base64(attach_part)
                attach_part.add_header('Content-Disposition',
                                       f"attachment; filename={name}")
                multipart_msg.attach(attach_part)

        try:
            server.sendmail(sender_email, receiver,
                            multipart_msg.as_string())
        except Exception as err:
            print(f'Problem occurend while sending to {receiver} ')
            print(err)
            input("PRESS ENTER TO CONTINUE")
        else:
            sent_count += 1

    print(f"Sent {sent_count} emails")


def sendmail(csv_file, sender_email, password, subject, message, name):
    host = "smtp.gmail.com"
    port = 587  # TLS replaced SSL in 1999

    try: 
       
        server = SMTP(host=host, port=port)
        server.connect(host=host, port=port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user=sender_email, password=password)
        send_emails(csv_file, server, message, subject, name, sender_email)
        server.quit()
    except Exception as e:
        print(e)





    


def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')
    # return HttpResponse("this is home page")

def about(request):
    return render(request, 'about.html')
    #return HttpResponse("this is about page")

def services(request):
    
    return render(request, 'services.html')
    # return HttpResponse("this is service page")

def contact(request):
    # messages.success(request, 'Your email has been sent.')
    return render(request, 'contacts.html')
    # return HttpResponse("this is contact page")

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)

        # check if user has correct credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")


def check_email(email):
    print("Checking....", email)
    try:
        validate_email(email)
        return True
    except ValidationError as e:
        return False

def send_email(request):
    sender_email=request.POST.get('sender_email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    password = request.POST.get('password')
    name = request.POST.get('name')
    try: 
        csv_file = request.FILES["csv_file"].read().decode("utf-8")
    except Exception as e:
        print(e)
    
    # print(sender_email, subject, message, password)

    sendmail(csv_file, sender_email, password, subject, message, name)


 
    messages.success(request, 'Your email has been sent!')
    return render(request, 'services.html')

#Method specified by url with ajax
# def call_validate_emails(req):
    # if req.method == 'POST':
    #     csv_file=req.POST.get('csv_file')
    #     # write_data.py write_csv()Call the method.
    #     #Of the data sent by ajax"input_data"To get by specifying.
    #     validate_emails.csv_file(req.POST.get("csv_file"))
    #     return HttpResponse()