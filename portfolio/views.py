from django.shortcuts import render
from django.http import HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Avg, Count, Min, Sum, Max, Q, Case, When, F, Value
from .models import Stock, Position, Quote, Balance
import datetime, time
import pandas
from django.utils import timezone
from django.utils.timezone import make_aware
import json

# import json
import finnhub

alpha_vantage_key = 'GSG7BQGSGDY9PASO'
finnhub_key = 'buhih2748v6seskai4n0'

# https://www.alphavantage.co/support/#api-key

# https://finnhub.io/api/v1/quote?symbol=BB&token=buhih2748v6seskai4n0
# https://github.com/Finnhub-Stock-API/finnhub-python

# pk_658d5ee229fe4c09a75a846c8777ad08 

def get_stock_quote(symbol):

    # set finnhub api_key
    finnhub_client = finnhub.Client(api_key=finnhub_key)

    # request symbol quote
    finnhub_quote = finnhub_client.quote(symbol)

    # return close price
    return finnhub_quote['c']

#https://stackoverflow.com/questions/57761722/get-database-table-data-older-then-10-days-in-django
def update_quote():

    # get all stock on file
    stocks = Stock.objects.all().values("id", "symbol")

    # loop thought all stock on file
    for stock in stocks:

        # set a delay such that it complies with finnhub 60 request per minute rule
        time.sleep(5)

        # insert new quote into the database
        Quote.objects.create(symbol=stock, price=get_stock_quote(stock.symbol))

    print('update quote')


def calculate_balance_chart():
        
    stocks = Stock.objects.values("id", "symbol")

    # get todays date and remove tzinfo data
    today_date = datetime.datetime.now().replace(tzinfo=None)
    
    # https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python
    # find the oldest record on file, the first ever postion placed with this portfolio

    positions_all = Position.objects.all()
    quotes_all = Quote.objects.all()

    # remove tzinfo from date of oldest record
    start_date = positions_all.earliest('datetime').datetime.replace(tzinfo=None)

    # https://stackoverflow.com/questions/52329322/pandas-date-range-with-only-hours-minutes-and-seconds/52329578
    # get date range
    date_range = pandas.date_range(start=start_date,end=today_date, freq='5T', tz='Europe/Berlin')

    # create an array to store portfoilo value realtive to frequency
    chart_position = []

    # initialize previous balance
    previous_balance = 0

    for date in (date_range):

        # remove tzinfo from date 
        date = date.replace(tzinfo=None)

        open_postions = 0

        for stock in stocks:

            """ initalise total postion to zero this will hold the number of postions held of a specific relaive to date
                where a stock sold is denoted with as a negative number and a buy being denoted as a positive number """
            total_position = 0

            # get positions relaive to date
            positions = positions_all.filter(datetime__lt=make_aware(date), symbol_id=stock)
            for position in positions:
                # sequentially add postions size to total positions
                total_position+=position.size

            # get most recent quote relative to date
            quotes = quotes_all.filter(datetime__lt=make_aware(date), symbol_id=stock)
            # order_by('-datetime')

            # if one or more price quotes are on file set quote to most recent quote else set quote to zero
            if(quotes.exists()):
                quote = quotes.latest('datetime').price
            else:
                quote = 0

            # compute total value of stock holding relative to quote price on a specific time interval
            open_postions+= float(quote) * total_position

        if(previous_balance != open_postions):
            # round up and append balance on a specific time interval to chart position 
            chart_position.append({
                'balance':round(open_postions, 2)
            })

        # update previous balance 
        previous_balance = open_postions

    try:
        # delete all existing records
        Balance.objects.all().delete()

        #  insert json object to Balance model
        Balance.objects.create(json=chart_position)
    except Balance.DoesNotExist:
        pass
    
    print('update balance')

    # return chart postions json
    return chart_position



# https://docs.djangoproject.com/en/3.1/topics/db/aggregation/
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields

# Create your views here.
def main_view(request):

    # request all stock stored on file
    # https://stackoverflow.com/questions/10040143/how-to-do-a-less-than-or-equal-to-filter-in-django-queryset
    # https://stackoverflow.com/questions/30752268/how-to-filter-objects-for-count-annotation-in-django
    stocks = Stock.objects.annotate(total_position=Sum("position__size"))

    """ instatiae active postions, this will be used to store all active poistions
        where the sum of all the postions to date is greater or less then 0, where less then zero donates a sell
        and a value greater then zero denotes a buy """ 
    active_positions = []

    positions_all = Position.objects.all()
    quotes_all = Quote.objects.all()

    # loop through all stocks
    for stock in stocks:

        # initiate total cost and total positions 
        total_cost = 0
        if stock.total_position == None:
            total_position = 0
        else:
            total_position =  stock.total_position

        # request all positions realtive to the stock
        positions = positions_all.filter(symbol_id=stock)

        """ loop through all postions, where postions size is  multiplied the positon, this will compute the baseline cost
            this will help to determine the average cost per share, given all stock purchased sold and brought in the past,
            where any realised profit will reduce the accumulative average buying and selling price """

        for position in positions:
            # sequentially add postions cost to total cost
            total_cost+=float(position.price) * position.size
        
        # if total cost or total postion is equal to zero it can be assumed that no positions is currently open realtive to stock
        if(total_cost == 0 or total_position == 0):
            # if true set average price to zero 
            average_price = 0
        else:
            """ compute average cost relative to total cost divided absolute total postions
                since the direction of the sum of the postions does not affect the average price, 
                the absolute of the total positions can be taken, 
                round the result by 2 decimal points """
            average_price = round(total_cost/abs(total_position),2)

        # get the most recent quote on file relative to stock
        quotes = quotes_all.filter(symbol_id=stock)

        # if number of quotes on file is greater then zero and average price is greater then zero
        if(quotes.exists() and average_price > 0):

            # set most recent price on file as the quote
            quote = quotes.latest('datetime')

            # determine the unrealised profit relative to average price and quote price, rounds result by two  decimal points

            # calculate change in of dollars
            change = round((float(quote.price)-float(average_price)),2)

            # calculate change in percentage
            percentage = round(((float(quote.price)/float(average_price)-1) * 100), 2)

            # set current price to most recent quote
            price = quote.price

        elif average_price > 0:
            # else if avarage price is greater then zero
            # set change to zero 
            change = 0
            percentage = 0

            # set current price to average price
            price = 0
        else:
            # else set change to zero 
            change = 0
            percentage = 0

            # set price to zero
            price = 0

        # if total postions is not equal to zero append position to active position
        if(total_position != 0):
            active_positions.append({
                'price':average_price,
                'symbol': stock.symbol,
                'companyName':stock.companyName,
                'description':stock.description,
                'exchange':stock.exchange,
                'size':total_position,
                'quote':price,
                'change':change,
                'percentage':percentage
            })

    # retrieve most recent balance chart
    try:
        balance = Balance.objects
        balance = balance.latest('datetime')
        json_list = json.dumps(balance.json)
    except Balance.DoesNotExist:
        json_list = {}

    # convert json to a json string dump

    # render html page, with json_list and active_postions being the context
    return render(request, "pages/index.html", context={
        'positions': active_positions, 
        'chart':json_list,
    })


def start():
    shedule = BackgroundScheduler()

    # https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html
    # Runs from Monday to Friday at 2.30 (pm) until 9:00 (pm) every 5 minutes
    shedule.add_job(update_quote, 'cron', day_of_week='mon-fri', hour='14-21', minute='*/5')

    shedule.add_job(calculate_balance_chart, 'cron', day_of_week='mon-fri', hour='14-21', minute='*/5')

    # https://github.com/agronholm/apscheduler/issues/348

    # shedule.add_job(my_jobs, trigger='interval', minutes=5)
     
    shedule.start()


start()
# calculate_balance_chart();

#https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6
# https://www.nasdaq.com/solutions/nasdaq-data-on-demand

# https://www.codegrepper.com/code-examples/delphi/python+run+function+every+5+minutes