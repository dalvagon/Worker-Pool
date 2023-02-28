Worker Pool is a project written in Python that consist of two scripts, master.py and worker.py. 

The master script pushes website addresses onto a RabbitMQ queue. Multiple workers read them and download the website pages.
