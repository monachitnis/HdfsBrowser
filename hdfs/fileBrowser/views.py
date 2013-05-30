from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import pexpect
import os, sys, time, re, getopt, getpass
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django import template 
from django.template import Template, Context, RequestContext, loader

SSH_NEWKEY = '(?i)are you sure you want to continue connecting'

COMMAND_PROMPT = '[#$] '
user='siddharn'
host='mithril-gw.red.ygrid.yahoo.com'
password='281Laxman!'


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

def list_view(request):
	child = pexpect.spawn('ssh -l %s %s'%(user, host))
	COMMAND_PROMPT = '[#$] '
	TERMINAL_PROMPT = '(?i)terminal type\?'
	TERMINAL_TYPE = 'vt100'
    	i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, COMMAND_PROMPT, '(?i)password'])
    	if i == 0: # Timeout
        	print 'ERROR! could not login with SSH. Here is what SSH said:'
        	print child.before, child.after
        	print str(child)
        	sys.exit (1)
    	if i == 1: # In this case SSH does not have the public key cached.
        	child.sendline ('yes')
        	child.expect ('(?i)password')
    	if i == 2:
        # This may happen if a public key was setup to automatically login.
        # But beware, the COMMAND_PROMPT at this point is very trivial and
        # could be fooled by some output in the MOTD or login message.
        	pass
    	if i == 3:
        	child.sendline(password)
        # Now we are either at the command prompt or
        # the login process is asking for our terminal type.
       	 	i = child.expect ([COMMAND_PROMPT, TERMINAL_PROMPT])
        	if i == 1:
            		child.sendline (TERMINAL_TYPE)
            		child.expect (COMMAND_PROMPT)
    #
    # Set command prompt to something more unique.
    #
    	COMMAND_PROMPT = "\[PEXPECT\]\$ "
    	child.sendline ("PS1='[PEXPECT]\$ '") # In case of sh-style
    	i = child.expect ([pexpect.TIMEOUT, COMMAND_PROMPT], timeout=10)
    	if i == 0:
        	print "# Couldn't set sh-style prompt -- trying csh-style."
        	child.sendline ("set prompt='[PEXPECT]\$ '")
        	i = child.expect ([pexpect.TIMEOUT, COMMAND_PROMPT], timeout=10)
        	if i == 0:
            		print "Failed to set command prompt using sh or csh style."
            		print "Response was:"
            		print child.before
            		sys.exit (1)
	
	#Start sending commands
#	child.sendline ('ls -al')
#    	child.expect (COMMAND_PROMPT)
#    	ls = child.before

   	child.sendline ('kinit')
    	child.expect ('Password for siddharn@Y.CORP.YAHOO.COM: ')
   	child.sendline ('281Laxman!')
    	child.expect (COMMAND_PROMPT)
    	kinit = child.before

    # Run hadoop fs -ls.
    	child.sendline ('hadoop fs -ls')
    	child.expect (COMMAND_PROMPT)
    	hls = child.before
	
    	child.sendline ('hadoop fs -put config.yaml .')
    	child.expect (COMMAND_PROMPT)
    	hput = child.before
	
	return HttpResponse("<html> <body> Hello, World: \n <li>"+hls+"</li> </body></html>" )

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
