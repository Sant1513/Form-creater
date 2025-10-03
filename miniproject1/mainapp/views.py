from django.shortcuts import render,redirect
from django.http import HttpResponse
# from templates import prac.html
from similarity import similar
from mainapp.models import User_details,SubjectChoices
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
import os
# Create your views here.
import datetime
import logging

from extract_text import basic_extracting 


logger = logging.getLogger(__name__)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def current_datetime(request):
    now=datetime.datetime.now()
    obj=similar("dbms1")
    obj.retrieve("1")
    html="<html><body><h1>It is now %s.</h1></body></html>"%now
    return HttpResponse(html)

def show_html(request):
    return render(request,"prac.html")

import random
import string
def send_email(sender_email, sender_password, receiver_email, subject, body):
    
    try:
        # Set up the MIME structure
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to the server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Usage
def generate_otp():
    length=6
    characters = string.digits + string.ascii_letters
    otp = ''.join(random.sample(characters, length))
    return otp


def check_email(request):
    if request.method=="POST":
        data = json.loads(request.body)
        email = data.get('email', None)
        name=data.get('name',None)
        role=data.get('role')
        if not email:
            return JsonResponse({"error": "Email not provided"}, status=400)
        # File reading example
        if User_details.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            print("repeat")
            # return render(request, 'signup.html', {
            #     'name': name,
            #     'email': email,
            #     'user_type': role,
            # })
            return JsonResponse({"messages":"existed"})
        else:
            otp=generate_otp()
            send_email(
                sender_email="varunreddyvvr@gmail.com",
                receiver_email=email,
                subject="email verification by VTU QPRS",
                body=f"the code is '{otp}'",
                sender_password="yyag vghx plxn ylym"
            )
            return JsonResponse({"messages":"open","code":otp})
        
        
        #add the content here to pass to front end
    return JsonResponse({"error": "Invalid request method"}, status=405)
def view_forget(request):
    return render(request,"forgetinterface.html")
def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('userType')

        # Basic validation or logic for handling sign-up
        
        
        if User_details.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            print("repeat")
            return render(request, 'signup.html', {
                'name': name,
                'email': email,
                'user_type': user_type,
            })
        else:
        # Creating user (this is a simple example, you may need to handle user type better)
            user = User_details(name=name, email=email, password=password,role=user_type)
            user.save()

        # Redirect to login after successful signup
        return redirect('login')
        # return redirect('signup')

    return render(request, 'signup.html')

def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type=request.POST.get('userType')
        print(email,password,user_type)
        if User_details.objects.filter(email=email,role=user_type,password=password).exists():
            # print(User_details.objects.filter(email=email))
            row = User_details.objects.get(email=email)  # Replace '1' with the desired ID
            if row.role=="admin" and row.status=="unaccept":
                messages.error(request, 'Not Approved.')
                print("repeat")
                return render(request, 'login.html', {
                    'email': email,
                    'password':password,
                    'user_type':user_type,                
                })
            if user_type=="admin":
                return render(request,"admindashboard.html")
            elif user_type=="student":
                return render(request,"studentinterface.html")
        else:
            messages.error(request, 'Invalid credentials.')
            print("repeat")
            return render(request, 'login.html', {
                'email': email,
                'password':password,
                'user_type':user_type,                
            })
    return render(request,'login.html')
def email_presence(request):
    if request.method=="POST":
        data = json.loads(request.body)
        email = data.get('email', None)
        if not email:
            return JsonResponse({"error": "Email not provided"}, status=400)
        # File reading example
        if User_details.objects.filter(email=email).exists():
            print("repeat")
            otp=generate_otp()
            row = User_details.objects.get(email=email)  # Replace '1' with the desired ID

            # Get the value of the 'name' column
            password = row.password
            send_email(
                sender_email="varunreddyvvr@gmail.com",
                receiver_email=email,
                subject="email verification by VTU QPRS for password",
                body=f"the code is '{otp}'",
                sender_password="yyag vghx plxn ylym"
            )
            return JsonResponse({"messages":"open","code":otp,"password":password})
        else:
            return JsonResponse({"messages":"not_present"})
        
        
        #add the content here to pass to front end
    return JsonResponse({"error": "Invalid request method"}, status=405)
def landingpage_view(request):
    return render(request,'landingpage.html')
def admindashboard_view(request):
    return render(request,"admindashboard.html")
def extraction_view(request):
    
    if request.method=="POST":
        data = json.loads(request.body)
        name = data.get('subject', None)
        if not name:
            return JsonResponse({"error": "subject name not provided"}, status=400)
        request.session['subject']=name
        print(f"in extraction {name}")
        return JsonResponse({"messages":"open"})
        #add the content here to pass to front end
    return JsonResponse({"error": "Invalid request method"}, status=405)
def view_extraction(request):
    return render(request,"extractquestions.html")   

def upload_pdf(request):
    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'upload':
            if 'pdfFile' in request.FILES:
                pdf = request.FILES['pdfFile']

                # Check if the uploaded file is a PDF
                if pdf.content_type != 'application/pdf':
                    return JsonResponse({'error': 'Please upload a valid PDF file'}, status=400)

                subject_name = request.session.get("subject")
                if not subject_name:
                    return JsonResponse({'error': 'Subject not found in session'}, status=400)

                # Save the file using FileSystemStorage
                upload_directory = os.path.join('C:/Users/Public/miniproject1/', f"{subject_name}_pdf_files")
                os.makedirs(upload_directory, exist_ok=True)
                fs = FileSystemStorage(location=upload_directory)

                try:
                    # Save the file and generate the URL
                    file_name = fs.save(pdf.name, pdf)
                    # file_path = fs.url(file_name)
                    file_path = os.path.join(upload_directory, file_name)
                    full_path = os.path.normpath(file_path)
                except Exception as e:
                    logger.error(f"Error saving file: {str(e)}")
                    return JsonResponse({'error': 'Failed to save file'}, status=500)

                # Return success message
                # full_path = os.path.join('C:', 'Users', 'Public', 'miniproject1', f"{subject_name}_pdf_files", file_path)
                print(f" in upload {full_path}")
                request.session['filepath']=full_path
                return JsonResponse({'file_path': full_path, 'message': 'File uploaded successfully','action_per':"upload"})
            else:
                return JsonResponse({'error': 'No file uploaded'}, status=400)

        elif action == 'extract':
            subject_name = request.session.get("subject")
            full_path=request.session.get("filepath")
            if not (subject_name and full_path):
                print("no subject or path name")
            print(full_path)
            extracted_text=extract_func(subject_name,full_path)
            # extracted_data = "Extracted text from the PDF \n next line of text \n third line text"  # Placeholder for actual extraction logic
            return JsonResponse({'message': 'Extraction complete', 'data': extracted_text,'action_per':"extract"})

        elif action == 'store':
            # Handle the store functionality here
            # You could save the extracted data to the database, for example:
            
            # store_func()
            subject_name = request.session.get("subject")
            new_data = request.POST.get('new_data')
            print(new_data)
            store_func(new_data,subject_name)
            return JsonResponse({'message': 'Data stored successfully','action_per':"store"})

    else:
        return render(request, 'extractquestions.html')
    

def extract_func(subject_name,path):
    extract_obj=basic_extracting(subject_name)
    extracted_text=extract_obj.extract_text_modulewise(path)
    return extracted_text
import json  

def store_func(new_data,subject_name):
    # subject_name="dbms_main"
    store_obj=basic_extracting(subject_name)
    store_obj.store_in_temp(new_data)
def view_imp_questions(request):
    if request.method=="POST":
        data = json.loads(request.body)
        subject = data.get('subject', None)
        if not subject:
            return JsonResponse({"error": "Subject not provided"}, status=400)
        # File reading example
        file_path = f"C:/Users/Public/miniproject1/{subject}module_wise/important_questions" # Path to your text file
        if not os.path.exists(file_path):
            print("no path exists")
            return JsonResponse({"error": "path is not correct"}, status=400)
        # Open the file and read its contents
        with open(file_path, "r") as file:  # Use "r" mode to read the file
            content = file.read()  # Read the entire content of the file

        imp_question=content
        context = {"imp_question": imp_question}
        print(context["imp_question"][:10])
        # return render(request, "viewquestions.html")
        return JsonResponse(context,status=200)
        
        #add the content here to pass to front end
    return JsonResponse({"error": "Invalid request method"}, status=405)#add the content here to pass to front end
def similarity_func(request):
    if request.method == "POST":
        data = json.loads(request.body)
        subject = data.get('subject', None)
        if not subject:
            return JsonResponse({"error": "Subject not provided"}, status=400)
        subject_name=subject#just for sample actually take from front end through request
        similar_obj=similar(subject_name)# add subject name
        subject_folder=f"C:/Users/Public/miniproject1/{subject_name}module_wise/important_questions"
        if os.path.exists(subject_folder):
            with open(subject_folder, 'w') as file:
                pass 
        for i in range(1,6):
            similar_obj.retrieve(str(i))
        return JsonResponse({"messages":"Done"})

def view_questions(request):
    return render(request,"viewquestions.html") 
def get_choices(request):
    query = request.GET.get('q', '')  # Get the query from the request
    print(f"Received query: {query}") 
    choices = SubjectChoices.objects.filter(subject_code__icontains=query).values_list('subject_code', flat=True)
    print(f"Filtered choices: {list(choices)}") 
    return JsonResponse(list(choices), safe=False) 
def view_dropdown(request):
    return render(request,"dropdowntest.html")
def addsub_details(request):
    if request.method=="POST":
        data = json.loads(request.body)
        name = data.get('name', None)
        code=data.get('code',None)
        
        if not name and not code:
            return JsonResponse({"error": "Details not provided"}, status=400)
        # File reading example
        if SubjectChoices.objects.filter(subject_name=name,subject_code=code).exists():
            messages.error(request, 'subject details already exists.')
            print("repeat")
            return JsonResponse({"messages":"existed"})
        else:
            details=SubjectChoices(subject_name=name,subject_code=code)
            details.save()
            return JsonResponse({"messages":"saved"})
        
        
        #add the content here to pass to front end
    return JsonResponse({"error": "Invalid request method"}, status=405)
def view_addsub(request):
    return render(request,"addsubjects.html")
def checking_code(request):
    if request.method=="POST":
        data = json.loads(request.body)
        code=data.get('code',None)
        
        if not code:
            return JsonResponse({"error": "Details not provided"}, status=400)
        # File reading example
        if SubjectChoices.objects.filter(subject_code=code).exists():
            print("repeat")
            row = SubjectChoices.objects.get(subject_code=code)  # Replace '1' with the desired ID

            # Get the value of the 'name' column
            subjectname = row.subject_name
            return JsonResponse({"messages":"present","name":subjectname})
        else:
            return JsonResponse({"messages":"not_present"})
        
        
        #add the content here to pass to front end
    return JsonResponse({"error": "Invalid request method"}, status=405)



from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import json
from django.http import JsonResponse, HttpResponse

from reportlab.lib.pagesizes import letter

def wrap_text(text, max_width, pdf_canvas, start_x):
    """
    Wrap text to fit within a specified width on the PDF.
    Args:
        text: The input text to wrap.
        max_width: Maximum width (in points) for each line.
        pdf_canvas: The canvas object for measuring text width.
        start_x: The starting X position for text placement.
    Returns:
        A list of lines that fit within the specified width.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if pdf_canvas.stringWidth(test_line, "Helvetica", 12) + start_x > max_width:
            lines.append(current_line.strip())
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line.strip())

    return lines

def generate_pdf(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        questions = data.get('questions', None)
        if not questions:
            return JsonResponse({"error": "questions not provided"}, status=400)

        # Create a response object with a PDF content type
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="important_questions.pdf"'

        # Create the PDF object using reportlab
        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        max_width = 500  # Maximum width for text
        start_x = 100  # Starting X coordinate
        pdf_canvas.drawString(start_x, 750, "Important Questions:")
        y_position = 730

        for i, question in enumerate(questions.split('\n'), start=1):  # Assuming questions are newline-separated
            wrapped_lines = wrap_text(f"{question}", max_width, pdf_canvas, start_x)
            for line in wrapped_lines:
                if y_position <= 50:  # Check for page overflow
                    pdf_canvas.showPage()
                    y_position = 750
                    pdf_canvas.drawString(start_x, 750, "Continued Questions:")
                pdf_canvas.drawString(start_x, y_position, line)
                y_position -= 20  # Move down for the next line

            y_position -= 10  # Add extra spacing after each question

        # Finalize the PDF file
        pdf_canvas.save()
        return response
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)






    
from django.http import JsonResponse
import json
import plotly.express as px
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
import hdbscan
from sklearn.metrics import silhouette_score

def visualize_embeddings(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        tsne_graphs = {}
        hdbscan_cosine_graphs = {}
        scores = {}

        try:
            body = json.loads(request.body)
            subject_name = body.get('subject_name', None)
        except json.JSONDecodeError:
            subject_name = None

        if not subject_name:
            return JsonResponse({'error': 'No subject name provided'}, status=400)

        for i in range(1, 6):
            similar_obj = similar(subject_name)
            embeddings = similar_obj.send_embeddings(str(i))
            org_embedd = embeddings
            embeddings = np.array(embeddings)
            n_samples = len(embeddings)
            perplexity_value = min(30, max(1, n_samples - 1))  # Ensuring it's within a valid range

            tsne = TSNE(n_components=2, perplexity=perplexity_value, random_state=42)
            reduced_embeddings = tsne.fit_transform(embeddings)
            data = pd.DataFrame(reduced_embeddings, columns=['t-SNE1', 't-SNE2'])

            fig_tsne = px.scatter(
                data,
                x='t-SNE1',
                y='t-SNE2',
                title=f"Module {i} Data Points",
                labels={"t-SNE1": "Dimension 1", "t-SNE2": "Dimension 2"}
            )
            tsne_graphs[f"Module {i}"] = fig_tsne.to_html(full_html=False)

            # HDBSCAN Clustering
            clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
            hdbscan_labels = clusterer.fit_predict(embeddings)
            data['HDBSCAN_Cluster'] = hdbscan_labels
            data['HDBSCAN_Cluster'] =data['HDBSCAN_Cluster'].astype(str)
            fig_hdbscan = px.scatter(
                data,
                x='t-SNE1',
                y='t-SNE2',
                color='HDBSCAN_Cluster',
                title=f"Module {i} HDBSCAN Clusters",
                labels={"HDBSCAN_Cluster": "Cluster Label", "t-SNE1": "Dimension 1", "t-SNE2": "Dimension 2"},
                color_discrete_map={"-1": "gray"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            # hdbscan_score = silhouette_score(embeddings, hdbscan_labels) if len(set(hdbscan_labels)) > 1 else None


            valid_indices = hdbscan_labels != -1
            hdbscan_score = (
                silhouette_score(embeddings[valid_indices], hdbscan_labels[valid_indices])
                if np.sum(valid_indices) > 1 else None
            )
            # Cosine Similarity Clustering
            cosine_labels = similar_obj.cosine_graph(org_embedd, len(org_embedd))
            data['Cosine_Cluster'] = cosine_labels
            data['Cosine_Cluster'] = data['Cosine_Cluster'].astype(str)
            fig_cosine = px.scatter(
                data,
                x='t-SNE1',
                y='t-SNE2',
                color='Cosine_Cluster',
                title=f"Module {i} Cosine Similarity Clusters",
                labels={"Cosine_Cluster": "Cluster Label", "t-SNE1": "Dimension 1", "t-SNE2": "Dimension 2"},
                color_discrete_map={"-1": "gray"},
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            cosine_valid_indices=cosine_labels != -1
            # cosine_score = silhouette_score(embeddings, cosine_labels) if len(set(cosine_labels)) > 1 else None
            cosine_score = (
                silhouette_score(embeddings[cosine_valid_indices], cosine_labels[cosine_valid_indices])
                if np.sum(valid_indices) > 1 else None
            )
            hdbscan_cosine_graphs[f"Module {i}"] = {
                'HDBSCAN': fig_hdbscan.to_html(full_html=False),
                'Cosine_Similarity': fig_cosine.to_html(full_html=False)
            }

            scores[f"Module {i}"] = {
                'HDBSCAN_Score': hdbscan_score,
                'Cosine_Similarity_Score': cosine_score
            }

        return JsonResponse({
            'tsne_graphs': tsne_graphs,
            'hdbscan_cosine_graphs': hdbscan_cosine_graphs,
            'scores': scores
        })
    else:
        return render(request, 'visualize_page.html')
