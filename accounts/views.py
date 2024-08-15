from django.shortcuts import render
import csv
from .forms import UploadCSVForm
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Consumer
from django.core.paginator import Paginator
from decimal import Decimal

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            try: 
                for row in reader:
                    consumer, created = Consumer.objects.get_or_create(
                        name=row['consumer name'],
                        address=row['consumer address'],
                        ssn=row['ssn']
                    )
                    status_val = 2 if row['status'] == 'IN_COLLECTION' else (1 if row['status'] == 'PAID_IN_FULL' else 0)
                    account, created = Account.objects.get_or_create(
                        client_reference_no=row['client reference no'],
                        balance=row['balance'],
                        status=status_val,
                    )
                    account.consumers.add(consumer)
                success = True
            except Exception as e:
                print(f"Error: {e}")  # Log the error to the console or a log file
                success = False
            return render(request, 'upload_file.html', {'form': form, 'success': success})  
    else:
        form = UploadCSVForm()
    return render(request, 'upload_file.html', {'form': form})

def get_accounts(request):
    # Filter Accounts based on request parameters
    accounts = Account.objects.all()
    min_balance = request.GET.get('min_balance')
    max_balance = request.GET.get('max_balance')
    consumer_names = request.GET.getlist('consumer_name')
    status = request.GET.get('status')

    if min_balance:
        min_balance = Decimal(min_balance)
        accounts = accounts.filter(balance__gte=min_balance)
    if max_balance:
        max_balance = Decimal(max_balance)
        accounts = accounts.filter(balance__lte=max_balance)
    if consumer_names:
        accounts = accounts.filter(consumers__name__in=consumer_names).distinct()
    if status:
        status_val = 2 if status == 'IN_COLLECTION' else (1 if status == 'PAID_IN_FULL' else 0)
        accounts = accounts.filter(status=status_val)
    
    status_list = ['INACTIVE','PAID_IN_FULL','IN_COLLECTION']
    # Combine Account and Consumer data for rendering
    combined_data = []
    for account in accounts:
        # Get related consumers
        client_reference_no = account.client_reference_no
        balance = account.balance
        status = status_list[account.status]
        for consumer in account.consumers.all():
            if consumer.name not in consumer_names:
                continue
            combined_data.append({
                'client_reference_no': client_reference_no,
                'balance': balance,
                'status': status,
                'consumers': consumer.name,
                'address': consumer.address,
                'ssn': consumer.ssn,
            })

    # Paginate the accounts
    paginator = Paginator(combined_data, 10)  # Show 10 accounts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'account_list.html', {'page_obj': page_obj})