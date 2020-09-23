# HW1 (Static Web Server)
Architecture of this static web server - prefork + coroutines.

At start it spawns certain amount of processes which separately accept connections and then start coroutines handling each request 

## Testing
1.Start web server (by default utilizes port 8080)
```
python3 src/main.py
```
2.First of all check the functional test
```bash
./tests/http-test-suite/httptest.py localhost 8080
```
2.Start nginx server (see the config in tests/nginx.conf)
3.Run next commands to compare performance
```bash
ab -n 10000 -c 100 http://localhost:8080/httptest/wikipedia_russia.html
ab -n 10000 -c 100 http://localhost:8081/httptest/wikipedia_russia.html
```
You may also want to change the amount of cores utilized by server. You can do it by modifying CORES in [config file](src/config.py)

## Docker
It's also possible to start both servers in docker (but I won't recommend this since docker may slow them down in order of magnitudes)

```bash
docker build -t server-4-cores .
docker run --detach -p 8080:8080 --name server-4-cores -t server-4-cores
cd tests
docker build -t nginx.test .
docker run --detach -p 8081:8081 --name nginx.test -t nginx.test  
```
Proceed with your tests as in step 3.
