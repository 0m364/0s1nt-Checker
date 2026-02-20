from rq import Worker, Queue, Connection
import redis

listen = ['default']
redis_conn = redis.Redis(host='localhost', port=6379)

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
