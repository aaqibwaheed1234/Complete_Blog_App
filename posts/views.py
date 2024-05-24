from django.shortcuts import render, HttpResponseRedirect
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, TemplateView, DeleteView, UpdateView, View, DetailView, FormView
from .models import Post, Comment, Like
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import CustomUser
from accounts.forms import CustomUserForm
# Create your views here.


class BaseView(LoginRequiredMixin, CreateView): 
    model = Post
    template_name = 'base.html'
    fields = ['title', 'slug', 'intro', 'body']

class GetPosts(LoginRequiredMixin, ListView):
    model=Post
    template_name='frontpage.html'
    context_object_name= 'posts_list'

class BlogHomeView(TemplateView):
    template_name='home.html'

class CreatePost(CreateView):
    model=Post
    template_name="home.html"
    fields=['title', 'body', 'image']
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetail(TemplateView):
    def get(self, request, id):
        post = Post.objects.get(pk=id)
        # total_likes=post.total_likes()
        # print(total_likes)
        form=CommentForm()
        comments = post.comments.all()
        comment = Comment()
        username=comment.user = request.user
        return render(request, "detail.html", {"post": post, 'form':form, 'comments':comments, 'username': username})

class DeletePost(DeleteView):
    model=Post
    success_url=reverse_lazy('posts')
    template_name='confirm_delete.html'


class UpdatePost(UpdateView):
    model = Post
    fields = ['title', 'intro', 'body']
    template_name = 'update_post.html' 
    success_url=reverse_lazy('posts')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class StoreComment(View):
    def get(self, request):
        return render(request, 'detail.html', {'form': CommentForm()})

    def post(self, request):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        comment = Comment()
        comment.body=request.POST.get("body")
        comment.post = post
        username=comment.user = request.user
        comment.save()
        comments = post.comments.all()
        return render(request, 'detail.html', {'post': post, 'form': CommentForm(), 'comments': comments, 'username': username})


class DeleteComment(DeleteView):
    model=Comment
    template_name='comment_confirm_delete.html'
    context_object_name='object'

    def get_success_url(self):
        post_id = self.object.post.id
        return reverse_lazy('post-details', kwargs={'id': post_id})
    

class LikePost(View):
    def post(self, request, post_id, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        return JsonResponse({'success': True, 'liked': liked})


# like button functionality wihout fetch
# class LikePost(View):
#     def get(self, request, post_id, *args, **kwargs):
#         post = get_object_or_404(Post, id=post_id)
#         context = {
#             'post': post,
#             'like_count': post.total_likes(),
#         }
#         return render(request, 'frontpage.html', context)
    
#     def post(self, request, post_id, *args, **kwargs):
#         user = request.user
#         post = get_object_or_404(Post, id=post_id)
        
#         if post.likes.filter(id=user.id).exists():
#             post.likes.remove(user)
#         else:
#             post.likes.add(user)

#         return HttpResponseRedirect(reverse('posts'))

# class LikePost(View):
#     def get(self, request, post_id, *args, **kwargs):
#         post = get_object_or_404(Post, id=post_id)  
#         context = {
#             'post': post,
#             'like_count': post.like_set.count(),
#         }
#         return render(request, 'frontpage.html', context)
#     def post(self, request, post_id, *args, **kwargs):
#         user = request.user
#         print("Inside like_post view ", user)
#         post = get_object_or_404(Post, id=post_id)
#         # print(post)
#         # likes=post.total_likes()
#         # Like.objects.create(user=user, post=post)
#         # Like.save(self)
#         # print(likes)
#         current_likes = Like.objects.filter(post=post).count()
#         likes = Like.objects.filter(post=post)
#         print("Post likes: ",current_likes)
#         liked = Like.objects.filter(user=user, post=post).count()
#         if not liked:
#             Like.objects.create(user=user, post=post)
#             current_likes += 1
#             # print(current_likes)
#             # args[post_id]
#         else:
#             Like.objects.filter(user=user, post=post).delete()
#             current_likes -= 1
#         return HttpResponseRedirect(reverse('posts'))
#         # return render(request,'frontpage.html', {'likes':likes})
        

class UserProfileView(TemplateView):
    template_name = 'profile.html'
    form_class = CustomUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = post.user
        print(f"Post: {post}, User: {user}")
        form = self.form_class(instance=user)
        context.update({
            'form': form,
            'user': user,
        })
        return context
    
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = post.user
        # print(user)
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            import pdb;pdb.set_trace()
            user.save()
            return render(request, self.template_name, {'form': form, 'user': user})
        else:
            # return render(request, self.template_name, {'form': form, 'user': user})
            return self.form_invalid(form)



class SharePost(View):
    def get(self, request, post_id, *args, **kwargs):
        original_post = get_object_or_404(Post, id=post_id)
        original_post.shares+=1
        original_post.save()

        shared_post = Post.objects.create(
            user=request.user,
            title=original_post.title,
            slug=f"{original_post.slug}-shared-{original_post.id}",
            intro=original_post.intro,
            body=original_post.body,
            image=original_post.image,
        )
        # Redirect to the post details page of the new shared post
        return HttpResponseRedirect(reverse('post-details', kwargs={'id': shared_post.id}))

    def post(self, request, post_id, *args, **kwargs):
        return self.get(request, post_id, *args, **kwargs)
    

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '') 
        search_results = Post.objects.filter(title=query)
        serialized_results = [{
            'title': post.title,
            'intro': post.intro,
            'body': post.body,
        } for post in search_results]
        return JsonResponse({'results': serialized_results})


class Back(View):
    def get(self, request):
        return render(request, 'details.html')



