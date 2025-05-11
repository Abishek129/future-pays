from authentication.models import CustomerPool, Referral




def distribute_money(amount, start):
    distribute_amount = amount/(start-1)
    #admin = CustomerPool.objects.filter(token = 1).first()
    amount = 0
    print(distribute_amount)
    for i in range(1, start):
        customer_pool = CustomerPool.objects.filter(token = i).first()
        if not customer_pool or not customer_pool.is_active:
            
            amount += distribute_amount 
            
            continue
        print(customer_pool.wallet, "before")
        customer_pool.wallet += distribute_amount
        print(customer_pool.wallet, "after")
        print(customer_pool.owner)
        customer_pool.save()
    #admin.save()

    return

def add_refferal_money(user):
    referral = Referral.objects.get(user=user)
    customer_pool = CustomerPool.objects.get(owner=referral.referred_by)
    customer_pool.wallet += 200
    customer_pool.save

    return