# SvintusCheck
В наше нелёгкое время, когда даже у жителей банановых республик есть доступ к интернету, встаёт вопрос о необходимости защищаться от атак со стороны людей с пятачком.<br> 
Эта библиотека создаёт локальный API для получения страны по IP.<br>

---
# Компиляция 
```bash
sudo apt install libmaxminddb-dev g++
g++ -shared -fPIC -O3 svino-pass.cpp -o svinocheck.so -lmaxminddb
```
---
# Запуск 
```bash
python svinochecker.py
```
---
# Пример
Заходя на http://localhost:6789/?ip=91.233.103.0, вам возвращается текст {"ip": "91.233.103.0", "country": "Ukraine"}
