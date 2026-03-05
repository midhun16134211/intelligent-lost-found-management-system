import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lost_and_found.settings'
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Message, LostItem

try:
    userA = User.objects.get(username='chatuser_a')
except:
    userA = User.objects.create_user('chatuser_a', 'a@test.com', 'pass123')
try:
    userB = User.objects.get(username='chatuser_b')
except:
    userB = User.objects.create_user('chatuser_b', 'b@test.com', 'pass123')

Message.objects.filter(sender__in=[userA, userB], recipient__in=[userA, userB]).delete()

item = LostItem.objects.first()
item_id = item.pk if item else None

clientA, clientB = Client(), Client()
clientA.force_login(userA)
clientB.force_login(userB)

if item_id:
    url_ab = '/chat/%d/%d/' % (userB.id, item_id)
    url_ba = '/chat/%d/%d/' % (userA.id, item_id)
else:
    url_ab = '/chat/%d/' % userB.id
    url_ba = '/chat/%d/' % userA.id

# UserA sends message
resp1 = clientA.post(url_ab, {'content': 'Hello! Can I get my item back?'}, HTTP_HOST='127.0.0.1')
print('UserA POST status:', resp1.status_code, '(302=success, 500=bug)')

msgs_ab = Message.objects.filter(sender=userA, recipient=userB)
print('Messages A->B in DB:', msgs_ab.count())
if msgs_ab.exists():
    print('  Content:', msgs_ab.first().content)
    print('  is_read (should be False):', msgs_ab.first().is_read)

# UserB inbox
inbox_resp = clientB.get('/inbox/', HTTP_HOST='127.0.0.1')
inbox_html = inbox_resp.content.decode('utf-8', errors='replace')
print('UserB inbox status:', inbox_resp.status_code)
print('chatuser_a appears in UserB inbox:', 'chatuser_a' in inbox_html)

# UserB opens thread
thread_b = clientB.get(url_ba, HTTP_HOST='127.0.0.1')
thread_html = thread_b.content.decode('utf-8', errors='replace')
msg_visible = 'Hello! Can I get my item back?' in thread_html
print('UserB sees UserA message in thread:', msg_visible)

# Check mark-as-read
msgs_after = Message.objects.filter(sender=userA, recipient=userB)
print('is_read after UserB views thread:', msgs_after.first().is_read if msgs_after.exists() else 'N/A')

# UserB replies
resp2 = clientB.post(url_ba, {'content': 'Yes, item is here for pickup!'}, HTTP_HOST='127.0.0.1')
print('UserB POST reply status:', resp2.status_code)
msgs_ba = Message.objects.filter(sender=userB, recipient=userA)
print('Messages B->A in DB:', msgs_ba.count())

# UserA sees B's reply
thread_a = clientA.get(url_ab, HTTP_HOST='127.0.0.1')
a_html = thread_a.content.decode('utf-8', errors='replace')
reply_visible = 'item is here for pickup' in a_html
print('UserA sees B reply:', reply_visible)

print()
print('=== FINAL RESULT ===')
if msgs_ab.count() and msgs_ba.count() and msg_visible and reply_visible:
    print('CHAT IS FULLY FUNCTIONAL - Messages reach both users correctly!')
else:
    print('ISSUES FOUND:')
    if not msgs_ab.count(): print('  - A->B messages not saving')
    if not msg_visible: print('  - UserB cannot see UserA messages')
    if not msgs_ba.count(): print('  - B->A messages not saving')
    if not reply_visible: print('  - UserA cannot see UserB reply')
