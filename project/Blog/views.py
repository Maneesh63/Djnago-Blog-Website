from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .forms import LoginForm,Userform,postform,Edituserform,Commentform,Updatepostform,SearchForm,likeform,UserProfileForm
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from .models import Post,CustomUser,UserProfile,Comment
from django.core.paginator import Paginator
from django.shortcuts import render
 



#This search Functionality doesnot require as seperate but to get a good understanding of how search Functionality works
def search(request):
      
    search=SearchForm()
    
    if request.method=='GET':
      
      search=SearchForm(request.GET)
      
      if search.is_valid():
         
         query = search.cleaned_data['query']

         fig =Post.objects.filter(title__icontains=query)

    return render(request,'search.html',{'search':search , 'fig':fig})



def home(request):
    #Making a request to Post Model to get the Blog posts
    # And To list the Blog posts according to date created 
    posts=Post.objects.all().order_by('-date')

    if request.method=='GET':

     #search functionality code   
        search=SearchForm(request.GET)
        
        if search.is_valid():
            
            query=search.cleaned_data['query']
             
            search=posts.filter(title__icontains=query)
            
           
  #pagination codes
    paginator=Paginator(posts,6)
    
    #to getting the page number
    page_num=request.GET.get('page')
    
    #processing the page number contents
    page_obj=paginator.get_page(page_num)

   

    return render(request,'home.html',{'page_obj':page_obj ,'search':search})


def signup(request):
    
    if request.method=='POST':
        #getting form which i created in forms.py and passing which HTTP method to use
        form=Userform(request.POST)

        #validating the form according to our default or custom validation in forms.py file
        if form.is_valid():
           
           #saving the form details to database
           sv=form.save()
           #loging in the user while signup proccess with required credentials
           #here i used auth_login instead of login due to name conflict which i taken as alias name while importing the module
           auth_login(request,sv)
           messages.success(request,'REGISTERED SUCCESSFULLy',extra_tags='suc')
           return redirect('home')
        
    else:
         
        form=Userform()
        
    return render(request,'signup.html',{'form':form})


 

def login(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            
            #Getting the cleaned credentials from form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            #authenticate function is used to verify a set of credentials and return a user object if the credentials are valid. 
            user = authenticate(request, email=email, password=password)
            
            #if user is found in databse 
            if user is not None:
               
               #login the user 
               auth_login(request,user)
           
               return redirect('home')  
            else:
               
               form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')


def create(request):
    form=postform()
    if request.method=='POST':
        form=postform(request.POST,request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            #in here im setting commit=false to get the current user_id before saving the post in database
            post.user = request.user  
            post.user_id = request.user.user_id  
            post.save()
            return redirect('home')
        
    return render(request,'create.html',{'form':form})


def update_post(request, post_id):
  # Get the Post object with the specified post_id or return a 404 response
    post = get_object_or_404(Post, post_id=post_id)

    # Check if the form is submitted (method is POST)
    if request.method == 'POST':
        # Initialize the form with the submitted POST data and link it to the existing Post instance
        form = Updatepostform(request.POST, instance=post)
        
        # Check if the form is valid after submitting the data
        if form.is_valid():
            # If the form is valid, save the updated Post instance and redirect to the 'list' view
           
            form.save()
            return redirect('list')

    # If the method is not POST, initialize the form with the existing Post instance
    else:
        form = Updatepostform(instance=post)

    # Render the 'update_post.html' template with the form and the Post instance
    return render(request, 'update_post.html', {'form': form, 'post': post})

def post_list(request):
    
    posts=Post.objects.all().order_by('-date')

    paginator = Paginator(posts,6) 

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)
    

    if request.method=='GET':
         
         search_form=SearchForm(request.GET)

         if search_form.is_valid():
             
             query=search_form.cleaned_data['query']

             search_form=posts.filter(title__icontains=query)

    return render(request, "list.html", {"page_obj": page_obj,'search_form':search_form})
    

def individual_post(request,post_id):

    user=request.user

    form=Post.objects.get(post_id=post_id)

    return render(request,'ind_post.html',{'form':form,'user':user})


def delete_post(request,post_id):

    form=Post.objects.get(post_id=post_id)

    form.delete()
    return redirect('list')


def dashboard(request,user_id):

    user=CustomUser.objects.get(user_id=user_id)

    post=Post.objects.filter(user=user).order_by('-date')

    return render(request,'dashboard.html',{'user':user , 'post':post})


 
def post_like(request, post_id):
    #getting id of post
    post = get_object_or_404(Post, post_id=post_id)

    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')

    # Check if the user has already liked the post
    if request.user in post.post_likes.all():
        #if liked it will remove the like 
         post.post_likes.remove(request.user)
    else:
        #it will increment the like
        post.post_likes.add(request.user)

    if request.method == 'POST':
        like_form = likeform(request.POST)
    
        if like_form.is_valid():
            #Below lines are requesting id of User and post table
        
            like_form.instance.user = request.user
            like_form.instance.post = post
            like_form.save()
        
     
           
        
    return redirect('individual_post',post_id=post_id)




#def edit_profile(request,user_id):
    
    user=get_object_or_404(CustomUser,user_id=user_id)

    if request.method=='POST':

        form=dashboardform(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()

            return redirect('dashboard',user_id=user_id)
        
    return render(request,'edit_profile.html',{'form':form})

 

def edit_profile(request,user_id):
    #exception handling to catch the error
    try:
        #making a request to userprofile model
        profile_instance = request.user.userprofile
    except UserProfile.DoesNotExist:
        #getting the existing information from database
        profile_instance = UserProfile(user_id=user_id)

    if request.method == 'POST':
        #in here i just want to edit username ,email ,profile picture ,bio in 1 function(as like instagram)
        # instead of creating 2 functions so I would used 2 model forms in order to get the both existing information(instance=profile_instance)

        user_form = Edituserform(request.POST,request.FILES, instance=request.user)
        
        profile_form = UserProfileForm(request.POST,request.FILES, instance=profile_instance)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard',user_id=user_id) 

    else:
        
        user_form = Edituserform(instance=request.user)
        profile_form = UserProfileForm(instance=profile_instance)

    return render(
        request,
        'edit_profile.html',
        {'user_form': user_form, 'profile_form': profile_form}
    )



 #comment functionality to posts
def comment(request, post_id):
    # Ensure you import the Commentform model
    

    # Initialize the form with an instance of the Commentform model
    commentform = Commentform()

    # Retrieve the post using the provided post_id
    post = Post.objects.get(post_id=post_id)

    if request.method == 'POST':
        # Create an instance of the Commentform with the POST data
        commentform = Commentform(request.POST)

        if commentform.is_valid():
            # Save the form data to the database
            comment = commentform.save(commit=False)
            
            # Associate the comment with the current post
            comment.post = post
            comment.user=request.user
            comment.profile = request.user.userprofile
            comment.save()

            # Redirect to the individual post
            return redirect('individual_post', post_id=post_id)
        # If the form is not valid, re-render the comment form
        else:
           
            pass

    return render(request, 'comment.html', {'commentform': commentform, 'post': post})


def delete_comment(request,pk):
    
     comment = get_object_or_404(Comment, pk=pk)

    # Check if the user is the owner of the comment
     if request.user == comment.user:

        comment.delete()
        return redirect('individual_post', post_id=comment.post.post_id)
     else:
        
        return HttpResponse('not authorized')
 
     

#dummy functionality to test new functionality(not required)
def test(request):
    return render(request,'test.html')
    
