from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import *
from .forms import PostForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def about(request): # home page
    return render(request, 'blog/about.html', {})

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def cv(request):
    if request.method == 'POST':
        data = request.body.decode()
        
        # map to the correct model
        if not ('start_date' in data):
            Item.objects.create(title=request.POST['item_title'], text=request.POST['item_text'])
            return redirect('/mycv')
        else:
            if not ('place' in data):
                Intern.objects.create(start_date=request.POST['start_date'], end_date=request.POST['end_date'], text=request.POST['intern_text'])
                return redirect('/mycv')
            else:
                Project.objects.create(start_date=request.POST['start_date'], end_date=request.POST['end_date'], place=request.POST['place'], text=request.POST['intern_text'])
                return redirect('/mycv')

    items = Item.objects.all()
    interns = Intern.objects.all()
    projects = Project.objects.all()
    return render(request, 'blog/cv.html', {'items': items,'interns': interns,'projects': projects})

@csrf_exempt
def comment(request):
    if request.method == 'POST':
        Comment.objects.create(name=request.POST['nickname'],text=request.POST['text'])

    comments = Comment.objects.all()
    return render(request, 'blog/comment.html', {'comments': comments})

