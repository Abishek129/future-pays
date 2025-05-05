from authentication.models import CustomerPool, Referral




def distribute_money(amount, start):
    distribute_amount = amount/(start-1)
    for i in range(1, start):
        customer_pool = CustomerPool.objects.get(token = i)
        if not customer_pool.is_active:
            admin_account = CustomerPool.objects.get(token = 1)
            admin_account.wallet += distribute_amount 
            admin_account.save()
            continue
        customer_pool.wallet += distribute_amount

    return

def add_refferal_money(user):
    referral = Referral.objects.get(user=user)
    customer_pool = CustomerPool.objects.get(owner=referral.referred_by)
    customer_pool.wallet += 200
    customer_pool.save

    return