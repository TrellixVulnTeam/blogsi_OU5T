# Imports some stuffs
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import  CommentForm

# Show Home Page
def home(request):
    context = {
        # Take all data from DB
        'posts': Post.objects.all()
    }
    # Return template with the DB data
    return render(request, 'blog/home.html', context)


# For better show in Home page als Python List
class PostListView(ListView):
    # The same as DB
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.order_by('-created_at')
    # Newest Post show at First
    ordering = ['-created_at']


# Only for Post Details
class PostDetailView(DetailView):
    # The same as DB
    model = Post


# LoginRequiredMixin inherit Login class, only Logged in can created new post
class PostCreateView(LoginRequiredMixin, CreateView):
    # The same as DB
    model = Post
    fields = ['title', 'content']

    # Before submit take the author id
    def form_valid(self, form):
        form.instance.author = self.request.user
        # Override base method with author and form validation
        return super().form_valid(form)


# UserPassesTestMixin only post owner can make actions
class PostUpdateView(LoginRequiredMixin,  UserPassesTestMixin, UpdateView):
    # The same as DB
    model = Post
    fields = ['title', 'content']

    # before submit take the author id
    def form_valid(self, form):
        form.instance.author = self.request.user
        # Override base method with author and form validation
        return super().form_valid(form)

    # Check if works
    def test_func(self):
        # Take Post
        post = self.get_object()
        # Check the current User is author from the post
        if self.request.user == post.author:
            return True
        return False


# Delete Post can only post owner
class PostDeleteView(LoginRequiredMixin,  UserPassesTestMixin, DeleteView):
    # The same as DB
    model = Post
    # Redirect URL
    success_url = '/'

    # Check if works
    def test_func(self):
        # Take Post
        post = self.get_object()
        # Check the current User is author from the post
        if self.request.user == post.author:
            return True
        return False


# Show Contact Page
def contact(request):
    return render(request, 'blog/contact.html')


# Show Impressum Page
def impressum(request):
    return render(request, 'blog/impressum.html')


#add blog
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
