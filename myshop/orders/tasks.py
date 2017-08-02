#-*- coding:utf-8 -*-
from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    order=Order.objects.get(id=order_id)
    subject='Order nr. {}'.format(order.id)
    message='情爱的{}, \n\n 您已经成功提交一个订单。\您的订单号是{}。'.format(order.first_name,order.id)
    mail_sent=send_mail(subject,
                        message,
                        'admin@myshop.com',
                        [order.email])
    return mail_sent

