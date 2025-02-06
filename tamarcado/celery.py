from celery import Celery


from celery import Celery

app = Celery(
    'tamarcado',
    broker='redis://default:0PKAZEkzurJg5aRpjSf3JiGhRDZQQg8Y@redis-13162.c241.us-east-1-4.ec2.redns.redis-cloud.com:13162/0',
    backend='redis://default:0PKAZEkzurJg5aRpjSf3JiGhRDZQQg8Y@redis-13162.c241.us-east-1-4.ec2.redns.redis-cloud.com:13162/0'
)

@app.task
def soma(a,b):
    import time
    time.sleep(20)
    return a + b