# Gettting Started with Faust

Make sure you have Kafka running locally. If you don't already have a local cluster then you can use the docker compose in this repo.

```
docker-compose up
``` 

The dependencies are set up just using a dumb requirements.txt file.

```
pip install -r requirements.txt
```

Then to run the agent(s) use:

```
faust -A app.demo worker -l info
```


**Resources**

[Faust Documentation](https://faust.readthedocs.io/en/latest/playbooks/quickstart.html)
