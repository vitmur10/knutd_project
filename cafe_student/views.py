from datetime import datetime
from asgiref.sync import sync_to_async
from .models import Order


# Create your views here.
def add_order(func: callable):
    async def add(callback_query):
        from Infotron.Const import order
        if callback_query.data == 'confirm_order':
            user_id = callback_query.data.from_user.id
            u = Order.objects.all()
            await sync_to_async(u.create)(
                positions=order,
                cost=sum(order.values()),
                data=datetime.now(),
                user_id=user_id,
            )
            order.clear()
        return await func(callback_query),

    return add