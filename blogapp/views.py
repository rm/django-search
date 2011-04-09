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
    query = request.GET.get('q')
    if query:
        entries = Entry.objects.raw(
            """
SELECT *, ts_rank_cd(search_tsv, query) rank
FROM blogapp_entry, plainto_tsquery('%(query)s') query
WHERE query @@ search_tsv
ORDER BY rank DESC
LIMIT 10;""" % dict(query=query))
    else:
        entries = Entry.objects.all().order_by('-date')
    return render_to_response(
        'list_entries.html', dict(entries=entries, query=query))

def list_tags(request):
    return render_to_response(
        'list_tags.html', dict(tags=Tag.objects.all().order_by('name')))
