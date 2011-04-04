from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from blog.blogapp.models import Author, Tag, Entry

def author(request, email):
    author = get_object_or_404(Author, email=email)
    return render_to_response('author.html', dict(author=author))

def entry(request, slug):
    entry = get_object_or_404(Entry, slug=slug)
    return render_to_response('entry.html', dict(entry=entry))

def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render_to_response('tag.html', dict(tag=tag))



def list_authors(request):
    return render_to_response(
        'list_authors.html', dict(authors=Author.objects.all().order_by('name')))

def list_entries(request):
    return render_to_response(
        'list_entries.html', dict(entries=Entry.objects.all().order_by('-date')))

def list_tags(request):
    return render_to_response(
        'list_tags.html', dict(tags=Tag.objects.all().order_by('name')))
