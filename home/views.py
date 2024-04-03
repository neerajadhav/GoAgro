from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
import requests
from .models import Profile, Relationship
from .forms import ProfileModelForm
from posts.forms import PostModelForm, CommentModelForm
from posts.models import Post, Like
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.models import User
from posts.models import Comment
import os

API_KEY = os.environ.get("NEWS_APPI_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")


def home(request):
    if request.user.is_authenticated:
        qs = Post.objects.all()
        profile = Profile.objects.get(user=request.user)
        post_added = False

        # post form and comment form
        p_form = PostModelForm()
        c_form = CommentModelForm()

        if "p_form_submit" in request.POST:
            p_form = PostModelForm(request.POST, request.FILES)
            if p_form.is_valid():
                instance = p_form.save(commit=False)
                instance.author = profile
                instance.save()
                print("Done bro")
                p_form = PostModelForm()
                post_added = True
                return redirect("home")

        if "c_form_sumbit" in request.POST:
            c_form = CommentModelForm(request.POST)
            if c_form.is_valid():
                instance = c_form.save(commit=False)
                instance.user = profile
                instance.post = Post.objects.get(id=request.POST.get("post_id"))
                instance.save()
                print("Comment Posted")
                c_form = CommentModelForm()
                return redirect("home")

        context = {
            "qs": qs,
            "profile": profile,
            "p_form": p_form,
            "c_form": c_form,
            "post_added": post_added,
            "WEATHER_API_KEY": WEATHER_API_KEY,
        }
        return render(request, "home/home.html", context)

    else:
        return redirect("/")


def submit_comment(request):
    if request.method == "POST" and request.is_ajax():
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            # Assuming 'body' is the field name for the comment body in your Comment model
            body = c_form.cleaned_data.get("body")
            post_id = request.POST.get("post_id")
            post = Post.objects.get(id=post_id)
            user_profile = Profile.objects.get(user=request.user)
            comment = Comment.objects.create(body=body, post=post, user=user_profile)

            # Get the HTML for the updated comments section
            comments_html = ""
            for c in post.comment_set.all():
                comments_html += f"""
                    <div class="comment-widgets m-b-5 py-3">
                        <div class="d-flex flex-row comment-row">
                            <div class="p-2"><span class="round"><img src="{c.user.image.url}" alt="user" width="35"></span></div>
                            <div class="comment-text w-100">
                                <b>{c.user}</b>
                                <span class="m-b-5 m-t-10">
                                    <p>{c.body}</p>
                                </span>
                                <div> 
                                    <small class="text-muted">{c.created}</small> 
                                </div>
                            </div>
                        </div>
                    </div>
                """

            return JsonResponse({"success": True, "home/comments_html": comments_html})
        else:
            return JsonResponse({"success": False, "errors": c_form.errors})
    else:
        return JsonResponse({"success": False, "errors": "Invalid request"})


def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == "Like":
                like.value = "Dislike"
            else:
                like.value = "Like"

        else:
            like.value = "Like"

            post_obj.save()
            like.save()

        data = {
            "value": like.value,
            "likes": post_obj.liked.all().count(),
        }
        return JsonResponse(data, safe=False)

    return redirect("home")


def newspaper(request):
    if request.user.is_authenticated:
        query = request.GET.get("query")
        url = (
            f"https://newsapi.org/v2/everything?q=({query} AND india)&apiKey={API_KEY}"
        )
        response = requests.get(url)
        data = response.json()
        articles = data["articles"]
        context = {"articles": articles, "WEATHER_API_KEY": WEATHER_API_KEY}
        return render(request, "home/newspaper.html", context)
    else:
        return redirect("/")


def marketplace(request):
    if request.user.is_authenticated:
        context = {"WEATHER_API_KEY": WEATHER_API_KEY}
        return render(request, "home/marketplace.html", context)
    else:
        return redirect("/")


def notifications(request):
    if request.user.is_authenticated:
        context = {"WEATHER_API_KEY": WEATHER_API_KEY}
        return render(request, "home/notifications.html", context)
    else:
        return redirect("/")


def profile(request):
    if request.user.is_authenticated:
        obj = Profile.objects.get(user=request.user)
        post = Post.objects.filter(author=obj).all()
        c_form = CommentModelForm()

        if "c_form_sumbit" in request.POST:
            c_form = CommentModelForm(request.POST)
            if c_form.is_valid():
                instance = c_form.save(commit=False)
                instance.user = profile
                instance.post = Post.objects.get(id=request.POST.get("post_id"))
                instance.save()
                print("Comment Posted")
                c_form = CommentModelForm()
                return redirect("profile")

        context = {
            "obj": obj,
            "post": post,
            "c_form": c_form,
            "WEATHER_API_KEY": WEATHER_API_KEY,
        }

        return render(request, "home/profile.html", context)
    else:
        return redirect("/")


def logout_view(request):
    if request.method == "GET":
        auth.logout(request)
        return redirect("/")


def settings(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        form = ProfileModelForm(
            request.POST or None, request.FILES or None, instance=profile
        )
        done = False

        if form.is_valid():
            form.save()
            return redirect("/profile")

        context = {
            "form": form,
            "done": done,
            "WEATHER_API_KEY": WEATHER_API_KEY,
        }
        return render(request, "home/settings.html", context)
    else:
        return redirect("/")


def invited_received_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        qs = Relationship.objects.invitations_received(profile)

        context = {
            "qs": qs,
        }

        return render(request, "home/notifications.html", context)
    else:
        return redirect("/")


def profile_list_view(request):
    if request.user.is_authenticated:
        user = request.user
        qs = Profile.objects.get_all_profiles(user)

        context = {
            "qs": qs,
        }

        return render(request, "home/profile_list.html", context)
    else:
        return redirect("/")


def invite_profile_list_view(request):
    if request.user.is_authenticated:
        user = request.user
        qs = Profile.objects.get_all_profiles_to_invite(user)

        context = {
            "qs": qs,
        }

        return render(request, "home/invite_list.html", context)
    else:
        return redirect("/")
