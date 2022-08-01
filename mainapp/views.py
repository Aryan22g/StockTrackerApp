from http.client import HTTPResponse
from threading import Thread
from tracemalloc import start
from django.http import HttpResponse
from django.shortcuts import render     #
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread
from asgiref.sync import sync_to_async
# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request,'mainapp/stockpicker.html',{'stockpicker':stock_picker})

@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True
    
def stockTracker(request):
    is_loginned = checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    
    stockpicker = request.GET.getlist('stockpicker')    #to select stocks selected by user 
    print(stockpicker)
    data = {}   #dictionary for data to be rendred to front end
    available_stocks = tickers_nifty50()
    for i in stockpicker:       ##check whether stock details are available
        if i in available_stocks:
            pass
        else:
            return HTTPResponse("Error")
    
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    print(start)
    # for i in stockpicker:
    #     result = get_quote_table(i)    #WEBSCRAPING yahoo data
    #     data.update({i:result})
    
    #use multithreading to call apis
    for i in range(n_threads):
        #create threadlist
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        #start threads
        thread_list[i].start()
        
    for thread in thread_list:
        thread.join()   #join threads after completion of thread task
    
    while not que.empty():
        result = que.get()
        data.update(result)
    end = time.time()
    time_taken = end-start
    print(time_taken)
    
    print(data)
    return render(request,'mainapp/stocktracker.html',{'data': data, 'room_name': 'track'})
                                                    # {'data': data, 'room_name': 'track'}--Meaning-->pass data using context