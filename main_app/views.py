from django.shortcuts import render, redirect
from .models import games, kids , kids_games , cards
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404


class GameCreate(LoginRequiredMixin, CreateView):
  model = games
  fields = ['game_name', 'description', 'game_image', 'game_price']
  # success_url = '/cats/'

  def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)




class GameUpdate(LoginRequiredMixin, UpdateView):
  model = games
  fields = ['game_name', 'description', 'game_price']

class GameDelete(LoginRequiredMixin, DeleteView):
  model = games
  success_url = '/games/'

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def games_index(request):
   
   game = games.objects.all()
   return render(request, 'games/index.html', {'game': game})

@login_required
def games_detail(request, game_id):
  game = games.objects.get(id=game_id)
  # kids_game ()
  kid_list = kids_games.objects.filter(fk_game_id=game.id, )
  return render(request, 'games/detail.html', {'game': game})

  #Get the toys, cat dosent have
#   toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
#   feeding_form = FeedingForm()
#   return render(request, 'cats/detail.html', 
#                 {'cat': cat, 
#                 'feeding_form': feeding_form,
#                 'toys': toys_cat_doesnt_have
#                 })

# @login_required
# def add_feeding(request, cat_id):
#   form = FeedingForm(request.POST)
#   if form.is_valid():
#     new_feeding = form.save(commit=False)
#     new_feeding.cat_id = cat_id
#     new_feeding.save()
#   return redirect('detail', cat_id)


class KidList(LoginRequiredMixin ,ListView):
  model = kids

class KidDetail(LoginRequiredMixin, DetailView):
  model = kids

class KidCreate(LoginRequiredMixin, CreateView):
  model = kids
  fields = ['kid_name', 'parent_phone','kid_image', 'credit' ]
  success_url = '/kids/'


class KidUpdate(LoginRequiredMixin, UpdateView):
  model = kids
  fields = ['kid_name', 'parent_phone']

class KidDelete(LoginRequiredMixin, DeleteView):
  model = kids
  success_url = '/kids/'

@login_required
def assoc_kid(request, kid_id, game_id):
    kid = get_object_or_404(kids, pk=kid_id)
    game = get_object_or_404(games, pk=game_id)

 

@login_required
def unassoc_kid(request, kid_id, game_id):
    """
    إلغاء ربط الطفل باللعبة: حذف السجل من kids_games
    """
    kid_game = get_object_or_404(kids_games, fk_kid_id=kid_id, fk_game_id=game_id)
    kid_game.delete()
    
    return redirect('game_detail', game_id=game_id)



def signup(request):
  error_message=''
  #if post
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid signup - Please try again later'
  #if get  
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)   