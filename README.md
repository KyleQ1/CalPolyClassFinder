# CalPolyClassFinder
Finds open/waitlisted classes and tells you what's available using the chrome browser.

## Running
Must have python installed in order to run this. I'm using version 3.9.13.
### Locally
```
pip install -r requirements.txt
cd src
python setup.py
python main.py
```

### Docker
Currently doesn't work.
```
cd Docker
docker build -t cal-poly-class-search .
docker run docker run --rm -d -p 4444:4444 -p 7900:7900 --shm-size="2g" cal-poly-class-search
```
Visit WebDriver tests at http://localhost:4444/

See what's happening inside http://localhost:7900/?autoconnect=1&resize=scale&password=secret
