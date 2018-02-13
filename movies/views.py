from django.shortcuts import render,redirect
from django.contrib import messages
from airtable import Airtable
import os

AT= Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
            'Movies',
            api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
#     print(str(request.GET.get('query','')))
    user_query=str(request.GET.get('query',''))
    search_result=AT.get_all(formula="FIND('"+user_query.lower()+"',LOWER({Name}))")
    stuff_for_frontend={'search_result':search_result}

    return render(request,"movies/movies_stuff.html",stuff_for_frontend)


def create(request):
    try:
        if request.method == 'POST':
            data= {
                'Name': request.POST.get('name'),
                'Pictures': [{'url':request.POST.get('url') or 'https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.formica.com%2Fus%2F~%2Fmedia%2Fglobal-images%2Fui%2Fnoimageavailable.png&f=1'}],
                'Rating': int(request.POST.get('rating')),
                'Notes': request.POST.get('notes')
            }

            responce=AT.insert(data)

            messages.success(request,'New Movies added: {}'.format(responce['fields'].get('Name')))
    except Exception as e:
        messages.warning(request,'Error Occured on inserting movie details:{}'.format("Error contact support Team"))

    return redirect('/')

def edit(request,movie_id):
    try:
        if request.method == 'POST':
            data={
                'Name': request.POST.get('name'),
                'Pictures': [{'url':request.POST.get('url') or 'https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.formica.com%2Fus%2F~%2Fmedia%2Fglobal-images%2Fui%2Fnoimageavailable.png&f=1'}],
                'Rating': int(request.POST.get('rating')),
                'Notes': request.POST.get('notes')
            }

            responce= AT.update(movie_id,data)
            messages.success(request,'Updated Movie": {}'.format(responce['fields'].get('Name')))
    except Exception as e:
            messages.warning(request,'Error Occured on updating movie details:{}'.format("Error contact support Team"))
    return redirect('/')

def delete(request,movie_id):
    try:
        movie_name=AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request,'Delete Movie: {}'.format(movie_name))
    except Exception as e:
         messages.warning(request,'Error Occured on deleting movie details:{}'.format("Error contact support Team"))

    return redirect('/')

