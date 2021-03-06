#coding: utf-8
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
from PIL import Image
import time
MEDIA_ROOT = '/home/frank/kotori/myproject/media'
SITE_URL = 'kotori.app.nyan.im'
ourl = 'http://'+SITE_URL+'/media/documents/kotori.png'
scale = 0
cn = 0
def merge(fn):
    #MEDIA_ROOT = '/home/frank/kotori/myproject/media' 
    y = time.strftime("%Y")
    m = time.strftime("%m")
    d = time.strftime("%d")
    h = time.strftime("%H")
    mi = time.strftime("%M")
    s = time.strftime("%S")
    try:
        bg = Image.open(MEDIA_ROOT+'/documents/'+y+'/'+m+'/'+d+'/'+fn)
    except:
        bg = Image.open(MEDIA_ROOT+'/documents/err.png')
    (bgx,bgy) = bg.size
    fg = Image.open(MEDIA_ROOT+'/documents/kotori.png')
    (fgx,fgy) = fg.size
    xyc = fgx/fgy
    fgyn = bgy*(scale+5)/100
    fgxn = fgyn*xyc
    fg = fg.resize((fgxn,fgyn))
    len = bgy - fgyn
    bg.paste(fg,(0,len),fg)
    outf = y+m+d+h+mi+s+'.jpg'
    bg.save(MEDIA_ROOT+'/done/'+outf)
    outurl = 'http://'+SITE_URL+'/media/done/'+outf
    return outurl

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            global scale
            scale = form.cleaned_data['scale']
            if scale >120:
                scale = 100
            elif scale <1:
                scale = 1
            newdoc = Document(docfile = request.FILES['docfile'])
            docfile = request.FILES['docfile']
            fn = docfile.name
            newdoc.save()
            global ourl
            global cn
            ourl = merge(fn)
            cn = 1
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form
    
    if cn == 0:
        ourl = 'http://'+SITE_URL+'/media/documents/kotori.png'
    else:
        cn = 0
    # Load documents for the list page
    documents = Document.objects.all()
    # Render list page with the documents and the form
    
    return render_to_response(
        'myapp/list.html',
        {'documents': documents, 'form': form,'ourl':ourl,'scale':scale},
        context_instance=RequestContext(request)
    )




