#!/usr/bin/env python
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import pexpect
import urllib
import os, sys, time, re, getopt, getpass
import traceback
import httplib, subprocess
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django import template 
from django.template import Template, Context, RequestContext, loader

COMMAND_PROMPT = '[#$] '
curl = '/usr/bin/curl'
cert = '/home/y/conf/ygrid_cacert/ca-cert.pem'
username = ''

@csrf_protect
def login_user(request):
    username = password = state = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if kinit_auth(username, password) == 0:
            grid_list = get_grid_list(username)
            return render_to_response('fileBrowser/browse.html',{'grid_list':grid_list,'username': username}, context_instance=RequestContext(request))
        else:
            state = "Incorrect username & password"
            return render_to_response('fileBrowser/login.html',{'state':state},context_instance=RequestContext(request))
    else:
        state = "Please log in below..."
        return render_to_response('fileBrowser/login.html', {'state':state}, context_instance=RequestContext(request))

def get_grid_list(username):
	grid_list = []
	all_clusters = ['AxoniteBlue-nn1-pxy.blue',
		 	'AxoniteRed-nn1-pxy.red',
			'BassniumRed-nn1-pxy.red',
			'BassniumTan-nn1-pxy.tan',
			'CobaltBlue-nn1-pxy.blue',
			'DilithiumBlue-nn1-pxy.blue',
			'DilithiumRed-nn1-pxy.red',
			'KryptoniteRed-nn1-pxy.red',
			'LuxBlue-nn1-pxy.blue',
			'LuxRed-nn1-pxy.red',
			'MithrilBlue-nn1-pxy.blue',
			'MithrilRed-nn1-pxy.red',
			'DilithiumBlue-nn1-pxy.blue',
			'NitroBlue-nn1-pxy.blue',
			'OxiumBlue-nn1-pxy.blue',
			'OxiumTan-nn1-pxy.tan',
			'PhazonTan-nn1-pxy.tan',
			'TiberiumTan-nn1-pxy.tan',
			'ReluxTan-nn1-pxy.tan',
			'UraniumTan-nn1-pxy.tan',
			'UraniumBlue-nn1-pxy.blue',
			'ZaniumTan-nn1-pxy.tan']
    	for c in all_clusters:
		url = 'https://' + c + '.ygrid.yahoo.com:4443/fs/user/' + username
		curl_args = [ curl, '--cacert', cert, '--negotiate', '-u', 'login:key', url ]
        	process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        	out, err = process.communicate()
		#if not parseHdfsProxyOutput(out).__len__() == 0:
		if "FileNotFound" in out:
			continue
		grid_list.append(c.split('-',1)[0])
    	return grid_list

def grid_listing(request):
	return render_to_response('fileBrowser/gridListing.html')
 
def kinit_auth(username, password):
        realm='DS.CORP.YAHOO.COM'
        principal = username + '@' + realm
	child = pexpect.spawn ('kinit', [principal])
        child.expect ('Password for ' + principal + ': ')
        child.sendline (password)
	#print child.before
        #COMMAND_PROMPT = "\[PEXPECT\]\$ "
        #child.sendline ("PS1='[PEXPECT]\$ '")
	i = child.expect([pexpect.EOF, COMMAND_PROMPT, "kinit(v5): Preauthentication failed while getting initial credentials"])
	return i
        #curl = pycurl.Curl()
        #curl.setopt(curl.VERBOSE, 1)
        #curl.setopt(pycurl.URL, proxy)
        #curl.setopt(pycurl.CAINFO, certdir)
        #curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_GSSNEGOTIATE)
        #curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        #curl.perform()
        #curl.close()

def list(request,dir):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
        operation = 'status'
        relative_path = dir
        ws_url = proxy_server + relative_path + '?op=' + operation
        curl_args = [ curl, '-c', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)
	return parseHdfsProxyOutput(out)
        #return HttpResponse("<html> <body><li>LIST "+relative_path+"</li> </body></html>" )

def mkdir(request,dir):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
        operation = 'mkdir'
        dirname = 'newdir'
        ws_url = proxy_server + 'user/' + username + '/' + dirname + '?op=' + operation
        curl_args = [ curl, '-X', 'PUT', '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)
        return HttpResponse("<html> <body><li>MKDIR "+dirname+"</li> </body></html>" )

def delete(request,dir):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
        filename = 'mona.txt'
        operation = 'stream'
        ws_url = proxy_server + 'user/' + username + '/' + filename + '?op=' + operation
        curl_args = [ curl, '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url, '--header', 'Range: bytes=0-1000' ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)
        return HttpResponse("<html> <body><li>DELETED "+filename+"</li> </body></html>" )

def upload(request):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
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
        return HttpResponse("<html> <body><li>UPLOADED "+dest+"</li> </body></html>" )

def move(request):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
        operation = 'move'
        src = 'srcdir'
        dst = 'dstdir'
        ws_url = proxy_server + 'user/' + username + '/' + src + '?op=' + operation + '&dest=' + dst
        curl_args = [ curl, '-X', 'PUT', '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)
        return HttpResponse("<html> <body><li>MOVED "+src+" to "+dst+"</li> </body></html>" )

def chmod(request):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
        operation = 'chmod'
        permission = '644'
        relative_path = ''
        ws_url = proxy_server + 'user/' + username + '/' + relative_path + '?op=' + operation + '&permission=' + permission + '&recursive=true'
        curl_args = [ curl, '-X', 'PUT', '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)
        return HttpResponse("<html> <body><li>CHMOD "+dirname+"</li> </body></html>" )

def chown(request):
        proxy_server = 'https://axoniteblue-nn1-pxy.blue.ygrid.yahoo.com:4443/fs/'
        operation = 'chown'
        owner = 'user'
        relative_path = ''
        ws_url = proxy_server + 'user/' + username + '/' + relative_path + '?op=' + operation + '&owner=' + owner + '&recursive=true'
        curl_args = [ curl, '-X', 'PUT', '-b', 'proxycookie.txt', '--cacert', cert, '--negotiate', '-u', 'login:key', ws_url ]
        process = subprocess.Popen(curl_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #curl = subprocess.Popen(curl_args, shell=True)
        out, err = process.communicate()
        #curl.terminate();
        print(out)
        return HttpResponse("<html> <body><li>CHOWN "+relative_path+" to "+owner+"</li> </body></html>" )


def browser_view(request):
	template = loader.get_template('fileBrowser/browse.html')
	context = Context({})
        return HttpResponse(template.render(context))

#ANUs function to fetch listing for given dir 
def get_dir_list(request,dir):
	#d = ['/user/chitnis:d', '/user/chitnis/.Trash:d', '/user/chitnis/.staging:d', '/user/chitnis/examples:d', '/user/chitnis/oozie-wrkf:d', '/user/chitnis/proxycookie.txt:f'] 
	request = '' #get request with more details
	array = list(request,dir)
	return array  


#to find
def is_dir(dir):
        if dir.split(':')[1] == 'd':
                return True
        return False

@csrf_exempt
def api_view(request):
        r=['<ul class="jqueryFileTree" style="display: none;">']
        try:
                r=['<ul class="jqueryFileTree" style="display: none;">']
		dir = request.POST.get('dir')
                d=urllib.unquote(request.POST.get('dir','/var'))
                dir_list = get_dir_list(request,dir)
                for obj in dir_list:
                        ff = obj.split(':')[0]
                        f =  ff.rpartition('/')[2]
                        if is_dir(obj):
                                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
                        else:
                                e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                                r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
                r.append('</ul>')
        except Exception,e:
                r.append('Could not load directory: %s' % str(e))
                r.append('</ul>')
        return HttpResponse(''.join(r))

@csrf_exempt		
def dir_view(request):
	r=['	<ul class="jqueryFileTree" style="display: none;">\
		    <li class="directory collapsed"><a href="#" rel="/this/folder/">Folder Name</a></li>\
		    <li class="file ext_txt"><a href="#" rel="/this/folder/filename.txt">filename.txt</a></li>\
		</ul>']
   
	return HttpResponse(''.join(r))

def parseHdfsProxyOutput(listContents):
        root = ET.fromstring(listContents)
        dirListing= []
        for dir in root.findall('directory'):
                dirListing.append(dir.get('path')+':d')
        for f in root.findall('file'):
                dirListing.append(f.get('path')+':f')
        #if not dirListing.__len__() == 0:
	dirListing.pop(0)
        return dirListing

