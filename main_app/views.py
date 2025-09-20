# views.py
import pytz
import uuid
from datetime import datetime, timedelta
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import games, kids , kids_games , cards
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from .forms import FeedingForm
from django.contrib import messages
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
class KidForm(forms.ModelForm):
    class Meta:
        model = kids
        fields = ['kid_name', 'parent_name', 'parent_phone', 'kid_image', 'credit', 'fk_card_id']

    # Override fk_card_id to be a dropdown of cards
    fk_card_id = forms.ModelChoiceField(
        queryset=cards.objects.all(),
        empty_label="Select Card",
        label="Card Type"
    )

    # Optional: dropdown for credit
    CREDIT_CHOICES = [
        (0, '0'),
        (10, '10'),
        (20, '20'),
        (50, '50'),
        (100, '100'),
    ]
    credit = forms.ChoiceField(choices=CREDIT_CHOICES, label="Credit")

class KidCreate(LoginRequiredMixin, CreateView):
    model = kids
    form_class = KidForm
    success_url = '/kids/'

    def form_valid(self, form):
        # Force unique hash and token for this kid
        form.instance.hash = uuid.uuid4().hex
        form.instance.token = uuid.uuid4().hex
        # Optionally assign current user
        form.instance.user = self.request.user
        return super().form_valid(form)


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


def nfc_generate(request, hash, token):
    # ✅ 1. Check session
    game_id = request.session.get('selected_game_id')
    if not game_id:
        messages.error(request, "You are not choosing the game id")
        return redirect('home')  # غيريها للصفحة المناسبة

    # ✅ 2. Check kid availability
    kid = kids.objects.filter(hash=hash, token=token).select_related('fk_card_id').first()
    if not kid:
        messages.error(request, "This user is not available in our website")
        return redirect('home')  # غيريها للصفحة المناسبة

    # ✅ 3. Fetch kid info + card info
    kid_id = kid.id
    kid_credit = kid.credit
    card_duration_time = kid.fk_card_id.card_duration_time if kid.fk_card_id else 0

    # ✅ 4. Check game price
    game = get_object_or_404(games, id=game_id)
    game_price = game.game_price

    # ✅ 5. Balance validation
    if kid_credit < game_price:
        messages.error(request, "You don't have balance to play this game, please recharge it.")
        return redirect('home')  # غيريها للصفحة المناسبة

    # ✅ Deduct balance
    kid.credit -= game_price
    kid.save()

    # ✅ Insert into kids_games
    bahrain_tz = pytz.timezone("Asia/Bahrain")
    start_time = datetime.now(bahrain_tz).time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=card_duration_time)).time()

    kids_games.objects.create(
        fk_kid_id=kid,
        fk_game_id=game,
        start_time=start_time,
        end_time=end_time,
        status=1,
        user=request.user if request.user.is_authenticated else None
    )

    # ✅ Redirect to game_dashboard
    return redirect(f'/game_dashboard/{game_id}/')