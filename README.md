# Fast API

```
pip install "fastapi[all]"
pip install openapi
uvicorn main:app --reload           this command only for dev env 
fastapi dev main.py --reload        this is for production env
python .\main.y             using python command to run
```

# set env variable in power shell
```
$env:OPENAI_API_KEY = 'dssgfasghsd'
```


```
#clone this repo in ec2-instance and then run below commands
git clone https://github.com/gonesai4/llm_project1.git
cd llm_project1
docker build -t p1 .  
docker run -d -p 80:80 -e OPENAI_API_KEY="gdasgasg" p1

then use instance publicip:80 in your laptop to check the app running or not. 

```

