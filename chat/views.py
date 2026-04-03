from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from .models import Conversation, Message
import json


@login_required
def conversation_list_view(request):
    employer_convs = Conversation.objects.filter(employer=request.user).select_related('job', 'worker', 'worker__profile')
    worker_convs = Conversation.objects.filter(worker=request.user).select_related('job', 'employer', 'employer__profile')
    conversations = list(employer_convs) + list(worker_convs)
    conversations.sort(key=lambda c: c.created_at, reverse=True)
    # Attach unread count as attribute so template can access it without calling method with user arg
    for conv in conversations:
        conv.unread = conv.unread_count(request.user)
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_detail_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.employer, conversation.worker]:
        return redirect('conversation_list')

    # Mark messages as read
    conversation.messages.exclude(sender=request.user).update(is_read=True)

    messages_qs = conversation.messages.select_related('sender').all()
    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'chat_messages': messages_qs,
    })


@login_required
def send_message_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.employer, conversation.worker]:
        return JsonResponse({'error': 'Ruxsat yo\'q'}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        body = data.get('body', '').strip()
        if body:
            msg = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=body
            )
            return JsonResponse({
                'id': msg.pk,
                'body': msg.body,
                'sender': request.user.get_full_name() or request.user.username,
                'sender_id': request.user.pk,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'is_own': True,
            })
    return JsonResponse({'error': 'Noto\'g\'ri so\'rov'}, status=400)


@login_required
def get_messages_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.employer, conversation.worker]:
        return JsonResponse({'error': 'Ruxsat yo\'q'}, status=403)

    after_id = request.GET.get('after', 0)
    messages_qs = conversation.messages.filter(pk__gt=after_id).select_related('sender')
    # Mark as read
    messages_qs.exclude(sender=request.user).update(is_read=True)

    data = [{
        'id': m.pk,
        'body': m.body,
        'sender': m.sender.get_full_name() or m.sender.username,
        'sender_id': m.sender.pk,
        'timestamp': m.timestamp.strftime('%H:%M'),
        'is_own': m.sender == request.user,
    } for m in messages_qs]

    return JsonResponse({'messages': data})
