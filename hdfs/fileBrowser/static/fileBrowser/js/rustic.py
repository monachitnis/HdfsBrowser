#
# jQuery File Tree
# Python/Django connector script
# By Martin Skou
#
import os
import urllib

def dirlist(request):
   r=['	<ul class="jqueryFileTree" style="display: none;">\
	    <li class="directory collapsed"><a href="#" rel="/this/folder/">Folder Name</a></li>\
	    <li class="file ext_txt"><a href="#" rel="/this/folder/filename.txt">filename.txt</a></li>\
	</ul>']
   
   return HttpResponse(''.join(r))
