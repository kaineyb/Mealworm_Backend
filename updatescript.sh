
mv -vi /home2/arkus/virtualenv/python/api_mealworm/3.8{,.bak}

bin/virtualenv --prompt '(app:3.8)' --python /opt/alt/python38/bin/python3 --system-site-packages /home2/arkus/virtualenv/python/api_mealworm/3.8/

source /home2/arkus/virtualenv/python/api_mealworm/3.8/bin/activate && cd /home2/arkus/python/api_mealworm


pip install --upgrade pip
pip install mysqlclient
pip list


# source /home2/arkus/virtualenv/python/api_mealworm/3.8/bin/activate && cd /home2/arkus/python/api_mealworm