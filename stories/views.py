import datetime

from django.template import loader,Context,RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import utc
from stories.models import Story

from stories.forms import StoryForm

def score(story, gravity=1.8, timebase=120):
	points = (story.points - 1)**0.8
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	age = int((now - story.created_at).total_seconds())/60

	return points/(age+timebase)**1.8

def top_stories(top=4, consider=4):
	latest_stories = Story.objects.all().order_by('-created_at')
	ranked_stories= sorted([(score(story), story) for story in latest_stories], reverse=True)
	return [story for _, story in ranked_stories][:top]

def index(request):
	stories = top_stories(top=4)
	# context = RequestContext(request,{
	# 	'stories':stories
	# })
	# context = {
	# 	"stories": stories, 
	# 	"title": "List"
	# }
	# template = loader.get_template('index.html')
	# context = Context({'stories': stories})
	# response = template.render(context)
	# response = '''
	# 	<html>
	# 		<head>
	# 			<title>News</title>
	# 		</head>
	# 		<body>
	# 			<ol>
	# 			  %s
	# 			</ol>
	# 		</body>
	# 	</html>
	# ''' % '\n'.join(['<li>%s</li>' %story.title for story in stories])
	#return HttpResponse(response)
	#return render(request, "index.html", context)

	return render_to_response('base/index.html', {'stories':stories, 'title': "List"})


def story(request):
	if request.method == 'POST':
		form = StoryForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = StoryForm()	

	return render_to_response('base/stories.html', {'form': form})

