apt-get update
apt-get install -y python3 python3-pip
pip3 install -r /app/requirements.txt
cd /app/
uvicorn main:app --reload --host 0.0.0.0 --port 8000