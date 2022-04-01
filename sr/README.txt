STEPS:
0) conda activate super-resolution
1) redis-server
2) python worker.py
3) flask run -p 5000
4) ngrok http --region=us --hostname=n1ddeh.ngrok.io 5000