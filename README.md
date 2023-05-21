# Notification Application

A Micro Application that allows Client to send notification (messages) including email and sms to patients (in this context).

## Tech Stack

**Server:** Python, FastAPI (web framework).

**Database:** MySQL.

**Project Management and Version Control:** BitBucket, Jira, Confluence.

**Task Scheduling System:** RabbitMQ, Celery.


## Installation

To install the project to your local computer or server.

1 Clone into a directory in your computer using:

```bash
git clone git@bitbucket.org:detechnovate/notification-app.git
```

2 change directory to the project folder created after cloning.
For window users use the command provided below.
For other Operating System Users, Kindly follow online documentation or guide on how to change directory.

```bash
cd <directoryname>
```

3 Creating a virtual environment (this is optional but advisable).

- For window users use the command below. If created successfully, activate the virtual environment.
For other Operating System Users, kindly follow online documentation or guide on how to install and activate your virtual environment.

```bash
virtualenv <virtualenvironmentname>
```

4 Install the required packages, using:

```bash
pip install -r requirements.txt

or

pip3 install -r requirements.txt
```

5 Run migrations to prepare the models or table to be added to the database, using:

```bash
alembic revision --autogenerate -m "migration name"
```

6 Migrate your tables to the database, using:

```bash
alembic upgrade head
```

7 install rabbitmq server, to do this, download the executable software from the official 
(https://www.rabbitmq.com/download.html)

Run RabbitMQ, celery and flower using:

- For RabbitMQ:
```bash
Rabbitmq-server start
```
For both celery and flower, you need to activate the virtual environment you created initially to run both. It is important to run the celery, however running flower is optional. The essence of flower is to have a graphic display of all tasks. 

- For Celery:
```bash
celery -A celery_config worker -l info --pool=solo
```

- For Flower (optional):
```bash
celery flower -A celery_config --port=port_number
```

8 Finally, you can run your server using:
```bash
python main.py

or

python3 main.py
```

## Features

NOTE: A majority of features provided by the API requires an Authorization header. All endpoints requires an Authorization header except;
```bash
PATCH /client/reactivate/client_id
POST /client/create
GET /client/
```

The Authorization header should be included in the request as follows:
```bash
Client-Authorization: client_key_value
```

## License
Project idea was inspired by [INTUITIVE]
