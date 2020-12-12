import multiprocessing
import gevent.monkey
gevent.monkey.patch_all()

preload_app = True

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 指定每个工作者的线程数
threads = multiprocessing.cpu_count() * 2

# 等待队列最大长度，超出丢弃
backlog = 2048

# 端口 5000
bind = '0.0.0.0:5000'

# 设置守护进程,将进程交给supervisor管理
daemon = 'false'

# 工作模式协程
worker_class = 'gevent'

# 设置最大并发量
worker_connections = 1000

# 设置进程文件目录
# pidfile = 'gunicorn.pid'

# 设置访问日志和错误信息日志路径
accesslog = "logs/access.log"
errorlog = "logs/debug.log"
loglevel = "debug"

# 设置日志记录水平
loglevel = 'warning'
