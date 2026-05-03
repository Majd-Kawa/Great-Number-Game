import random
from django.shortcuts import render, redirect
from .models import LeaderboardScore

# Create your views here.
def index(request):
    if 'number' not in request.session:
        random_num = int(random.randint(1, 100))
        request.session['number'] = random_num
        print(request.session['number'])
    
    if 'attempts' not in request.session:
        request.session['attempts'] = 0

    if 'message' not in request.session:
        request.session['message'] = ''
    
    if 'player_name' not in request.session:
        request.session['player_name'] = ''

    if 'game_over' not in request.session:
        request.session['game_over'] = False

    context={
        'number' : request.session['number'],
        'attempts' : request.session['attempts'],
        'message' : request.session['message'],
        'player_name' : request.session['player_name'],
        'player_guess' : request.session.get('player_guess'),
        'game_over': request.session['game_over'],
    }

    return render (request , 'index.html', context)

def reset(request):
    request.session.flush()
    return redirect ('/')

def guess(request):
    if request.method == 'POST':
        if request.session['game_over']:
            return redirect('/')
        request.session['attempts'] += 1
        random_num = int(request.session['number'])
        player_guess = int(request.POST['number'])

        if player_guess > random_num:
            request.session['message'] = 'high'
        elif player_guess < random_num:
            request.session['message'] = 'low'
        else :
            request.session['message'] = 'correct'
            request.session['game_over'] = True
            request.session['player_guess'] = player_guess
            return redirect ('/')

        if request.session['attempts'] >= 5:
            request.session['message'] = 'lose'
            request.session['game_over'] = True

        return redirect('/')

def leaderboard(request):
    if request.method == 'POST':
        name = request.POST['player_name']
        attempts = request.session['attempts']

        if request.session.get('message') == 'correct' and name:
            score = LeaderboardScore(player_name=name, attempts=attempts)
            score.save_score()
        return redirect('/leaderboard/')

    top_players = LeaderboardScore.objects.order_by('attempts')[:10]
    context = {
        'top_players': top_players
    }

    return render(request, 'leaderboard.html', context)