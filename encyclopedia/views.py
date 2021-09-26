
from cProfile import label
from pickle import FALSE
import re
from turtle import tilt
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from . import util
import markdown
from django import forms
from django.urls import reverse
from django.contrib import messages
import random


x = markdown.Markdown(extensions=['extra'])

class NewTaskForm(forms.Form):
    search= forms.CharField(label = "",widget=forms.TextInput(attrs={ "class": "search", "placeholder": "Search Encyclopedia"}))


class NewTextForm(forms.Form):
    data_input= forms.CharField(label="", widget=forms.Textarea(attrs={ "class": "form-control mb-4", "placeholder": "Please enter the markdown content for the new page","id":"data_input","rows":"6", "cols":"50"} ))

def index(request):

    return render(request, "encyclopedia/main.html", {
        "entries": util.list_entries(),
        "form" : NewTaskForm()     
    })


def entry_page(request, entry):
    return render(request, "encyclopedia/index.html", {
        "entry": entry.capitalize(),
        "form" : NewTaskForm()
       

    })

def get_page(request, entry):

    if util.get_entry(entry):
            return render(request, "encyclopedia/index.html", {
            "entry": x.convert(util.get_entry(entry)),
            "title": entry.capitalize(),
            "form" : NewTaskForm()
            })       
    elif (entry != 'search'):
          return render(request, "encyclopedia/index.html", {
         "entry":util.get_entry(entry),
         "title": entry.capitalize(),
         "form" : NewTaskForm()
    })


def find_page(request):
    list =[]
    indicator = True
    if request.method == 'POST': # If the form has been submitted...
        form = NewTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data

            search =  form.cleaned_data["search"].lower()        
            

            if util.get_entry(search):
                return render(request, "encyclopedia/index.html", {
                "entry": x.convert(util.get_entry(search)),
                "title": search.capitalize(),
                "form" : NewTaskForm()
                })
            else:
                all_entries = util.list_entries()
                
                for i in all_entries:
                    if( i is None ):
                        list = ["Page does not exist"]
                    elif (search in i.lower()):
                        list.append(i)
                
                if list == []:
                    list = ["Page does not exist"]
                    indicator = False

        else:
            return render(request, "encyclopedia/main.html", {
                "form": form
            })    
        
    
        return render(request, "encyclopedia/test.html", {
                    "text":list,
                    "indicator":indicator
        })


def dd(request):    #to test the sessions 
    if "input_data" not in request.session:
        request.session["input_data"] = []
    
    return render(request, "encyclopedia/dd.html",{
        "text":request.session["input_data"]
        })



def session(request):

    if request.method == "POST": # If the form has been submitted...
        
        form = NewTextForm(request.POST) # A form bound to the POST data
        title = NewTaskForm(request.POST)
       
        if form.is_valid() : # All validation rules pass
            new_page =  form.cleaned_data["data_input"]
            
            if title.is_valid():
                search =  title.cleaned_data["search"]

                combined =search +" " + new_page   


            request.session["input_data"] += [combined]  
      
            return HttpResponseRedirect(reverse("dd"))  # renders the new page.
        else: 
            return render(request, "encyclopedia/add.html",{"textform":form,"title": title }) #displays the wrong input


    return render(request, "encyclopedia/add.html", {
                    "textform" : NewTextForm(), # loads the create page with just textarea in it. 
                    "title": NewTaskForm()

        })


def add_page(request):

    if request.method == "POST": # If the form has been submitted...
        
        form = NewTextForm(request.POST) # A form bound to the POST data
        title = NewTaskForm(request.POST)
       
        if form.is_valid() : # All validation rules pass
            new_page =  form.cleaned_data["data_input"]
            
            if title.is_valid():
                search =  title.cleaned_data["search"]

               
        if util.save_entry(search,new_page) == FALSE: 
            messages.error(request, 'Page Already Exists')
            return render(request, "encyclopedia/add.html",{"textform":form,"title": title })
        elif util.save_entry(search,new_page)  : 
             messages.success(request, 'Page has been created successfully')
             return render(request,"encyclopedia/message.html")
            
        else: 
            return render(request, "encyclopedia/add.html",{"textform":form,"title": title }) #displays the wrong input


    return render(request, "encyclopedia/add.html", {
                    "textform" : NewTextForm(), # loads the create page with just textarea in it. 
                    "title": NewTaskForm()

        })



def edit_page_data(request):
    if request.method == "POST":
        page_title =  request.POST['subject']  #get the value of the title of the page of edit. This will be used to read the file data.
        
        data = util.get_entry(page_title)
        form =NewTextForm(initial={'data_input': data})



    return render(request, "encyclopedia/edit.html", {
                    "title":page_title,
                    "form1": form

                    })

                  

def save_edit_changes(request): #will get the tiile when save is clicked
    if request.method == "POST": # If the form has been submitted...
        
        form = NewTextForm(request.POST) # A form bound to the POST data
        title = NewTaskForm(request.POST)
        
       

        if form.is_valid() : # All validation rules pass
            new_page =  form.cleaned_data["data_input"]
            page_title =  request.POST['save_entry']
            split = str(page_title).split("_")
            print(split[0])

               
            util.save_edit(split[0],new_page) 
            messages.success(request, 'Entry has been upadted successfully')

            return redirect("get_page",split[0])
          
        else: 
            return render(request, "encyclopedia/add.html",{"form1":form,"title": title }) #displays the wrong input




def entry_random(request):

    entries_count = util.list_entries()  
    random_entry = random.randint(0,len(entries_count)-1)
    random_page = entries_count[random_entry]
    return redirect("get_page",random_page)