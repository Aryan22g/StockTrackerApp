# StockTrackerApp
A realtime stock tracker app using Django channels, Celery, Redis, ASGI Server. The platform gives realtime regular stock updates using Django Channels, Celery, Redis, and ASGI Server like daphne and Uvicorn.

# Project workflow:
### 1. User selects the stocks from the available stock list
(on stockpicker.html)

### 2. Picked stocks are sent ,to fetch there stock info from the API
(fetching stock info acts as a task which is queued in the redis.)

### 3. Fetched info is sent to front end from celery via django channels.
(on stocktracker.html)

### 4. At every 10 seconds stock is updated 
(on stocktracker.html)
By using celery beats we can schedule the fetching stock update task at an interval of 10 seconds. Fetching is done asynchronously by using redis and celery.
