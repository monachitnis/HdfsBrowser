#!/usr/bin/env python
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import pexpect
import os, sys, time, re, getopt, getpass
import traceback
import httplib, subprocess
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django import template 
from django.template import Template, Context, RequestContext, loader

COMMAND_PROMPT = '[#$] '

@csrf_protect
def login_user(request):
    print "in Logn_user"
    username = password = state = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'a' and password == 'a':
            grid_list = get_grid_list()
            return render_to_response('fileBrowser/gridListing.html',{'grid_list':grid_list,'username': username}, context_instance=RequestContext(request))
        else:
            state = "Incorrect username & password"
            return render_to_response('fileBrowser/login.html',{'state':state},context_instance=RequestContext(request))
    else:
        state = "Please log in below..."
        return render_to_response('fileBrowser/login.html', {'state':state}, context_instance=RequestContext(request))

def get_grid_list():
    print 'in grid Listing'
    grid_list = ['files.py', 'abc.txt']
    return grid_list

def grid_listing(request):
	return render_to_response('fileBrowser/gridListing.html')
 
def hdfs_proxy(request):
	
	username='chitnis'
	realm='DS.CORP.YAHOO.COM'
	principal = username + '@' + realm
	password='Eelix!r01'
   	child = pexpect.spawn ('kinit', [principal])
    	child.expect ('Password for ' + principal + ': ')
   	child.sendline (password)
	COMMAND_PROMPT = "\[PEXPECT\]\$ "
        child.sendline ("PS1='[PEXPECT]\$ '")
    	#child.expect (COMMAND_PROMPT) # EOF exception!!
	
	curl = '/usr/bin/curl'
	cert = '/home/y/conf/ygrid_cacert/ca-cert.pem'
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
	operation = 'status'
	ws_url = proxy_server + 'user/' + username + '?op=' + operation
	curl_args = [ curl, '-c', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
	process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#curl = subprocess.Popen(curl_args, shell=True)
	out, err = process.communicate()
	#curl.terminate();
	print(out)

	operation = 'mkdir'
	newdir = 'newdir'
        ws_url = proxy_server + 'user/' + username + '/newdir?op=' + operation
        curl_args = [ curl, '-X', 'PUT', '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)

	file = 'mona.txt'
	operation = 'stream'
        ws_url = proxy_server + 'user/' + username + '/' + file + '?op=' + operation
        curl_args = [ curl, '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url, '--header', 'Range: bytes=0-1000' ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)

	return HttpResponse("<html> <body><li>"+out+"</li> </body></html>" )

	dest = 'dest.file'
	src = 'views.py.OLD'
	operation = 'create'
        ws_url = proxy_server + 'user/' + username + '/' + dest + '?op=' + operation + '&overwrite=true'
        curl_args = [ curl, '-X', 'PUT', '-b', 'proxycookie.txt', '--cacert', cert, '-T', src, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(dest)

	return HttpResponse("<html> <body><li>"+dest+"</li> </body></html>" )
	#curl = pycurl.Curl()
	#curl.setopt(curl.VERBOSE, 1)
	#curl.setopt(pycurl.URL, proxy)
        #curl.setopt(pycurl.CAINFO, certdir)
	#curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_GSSNEGOTIATE)
	#curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
	#curl.perform()
	#curl.close()

def browser_view(request):
	template = loader.get_template('fileBrowser/browse.html')
	context = Context({})
        return HttpResponse(template.render(context))

@csrf_exempt		
def api_view(request):
	r=['	<ul class="jqueryFileTree" style="display: none;">\
		    <li class="directory collapsed"><a href="#" rel="/this/folder/">Folder Name</a></li>\
		    <li class="file ext_txt"><a href="#" rel="/this/folder/filename.txt">filename.txt</a></li>\
		</ul>']
   
	return HttpResponse(''.join(r))
