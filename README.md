# WorkerPool

<h1>11. WorkerPool</h1>
<p>
Develop a website downloader consisting of a master script which will push the links of pages containig
info about countries (https://www.infoplease.com/countries/{country_name}) onto a Rabbitmq queue
and a worker script which will download the pages.
</p>
<p>
Master.py will push onto the Rabbitmq queue the links of the pages than need to be downloaded and the download locations for each of them. 
</p>
<p>
Worker.py (multiple instances) will read the information from the queue and download the pages.
</p>
<p>
For each page that need to be downloaded, master.py will save in the queue a json object containing the link to the page and the disk location(the directory where the page will be downloaded)
</p>
<p>
<b>INPUT:</b>\
The Rabbitmq queue\
<b>OUTPUT:</b>\
The files downloaded in the specified locations\
The logs for worker.py si master.py and the handling for exceptions\
</p>
