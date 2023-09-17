# Demo2-BE
## Steps
```bash
#create and run container
docker run -d --name VisualTon -e MYSQL_ROOT_PASSWORD=0505jo -e MYSQL_DATABASE=example -p 3390:3306 mysql:latest 

#(optional) 用phpmyadmin 觀察data
docker run --name myphpadminVisualTon -d --link VisualTon:db -p 8081:80 phpmyadmin/phpmyadmin

#連接container (pwd: 0505jo)
docker exec -it VisualTon mysql -u root -p

#open another terminal

#create DB
python scripts/create_DB.py

#get the block id(the start block)
python scripts/get_latest_basechain_height.py

#paste the result to cronjob.py 'prev_latest_block' variable

#run the cronjob
python cronjob.py

#observe the DB and debug...
```


## check DB
```bash
#顯示全部DB
SHOW DATABASES;

#創建DB
CREATE DATABASE Example;

#選擇DB
USE Example;

#查看當前DB
SELECT DATABASE();

#查看當前DB有哪些table
SHOW TABLES;

#查看DB的table
DESCRIBE transactions;

#從table拿資料
SELECT * FROM transactions;

# 刪除table
DROP TABLE transactions;
```