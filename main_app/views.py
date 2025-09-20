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
from django.utils import timezone
# FOR CSRF Security
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    context_object_name = 'kid'
    template_name = 'main_app/kids_detail.html'  # تأكدي من المسار الصحيح

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # جلب الألعاب المرتبطة بالطفل
        context['kid_games'] = kids_games.objects.filter(fk_kid_id=self.object.id)
        return context

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



def dashboard(request):
    all_games = games.objects.all()
    all_kids_games = kids_games.objects.all()  

    return render(request, 'dashboard.html', {
        'games': all_games,
        'kids_games': all_kids_games
    })

# views.py

def game_dashboard(request, game_id):
    # Store the selected game id in session
    request.session['selected_game_id'] = game_id

    # جميع الألعاب
    all_games = games.objects.all()
    
    # اللعبة المحددة
    game = get_object_or_404(games, id=game_id)
    
    # جميع الأطفال المرتبطين بنفس اللعبة
    all_kids_games = kids_games.objects.filter(fk_game_id=game_id)
    
    # عدد الأطفال الذين يلعبون حاليًا (status 1 أو 2)
    playing_kids_number = all_kids_games.filter(status__in=[1]).count()
    
    # عدد جميع الأطفال المرتبطين بنفس اللعبة
    all_kids_number = all_kids_games.count()
    
    # الأطفال الذين يلعبون الآن (status 1 أو 2)
    kids_playing = all_kids_games.filter(status__in=[1])

    # الأطفال الذين تم تسجيلهم اليوم فقط
    today = timezone.now().date()
    kids_playing_today = all_kids_games.filter(create_date=today)
    
    return render(request, 'game_dashboard.html', {
        'game': game,
        'games': all_games,
        'kids_games': all_kids_games,
        'playing_kids_number': playing_kids_number,
        'all_kids_number': all_kids_number,
        'kids_playing': kids_playing,
        'kids_playing_today': kids_playing_today,
    })

@csrf_exempt
def update_kid_status(request, kid_game_id):
    """
    AJAX view to update the status of a kid_game to 2.
    """
    if request.method == 'POST':
        try:
            kid_game = kids_games.objects.get(id=kid_game_id)
            kid_game.status = 2
            kid_game.save()
            return JsonResponse({'success': True})
        except kids_games.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

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