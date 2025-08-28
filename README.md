# ChatRAG

# pre requisites:
1. docker
2. python
3. pip

### Running the application on docker
Since this needs to be deployed to cloud, it is needed to containerize the application. docker is being used for this project to containerize the whole application. to run locally using docker, follow these steps:
1. Run the docker deamon (launch docker desktop)
2. Build your container with the following command: `docker compose -f buildout/docker/development/docker-compose.yml build --no-cache`.
3. Run your container: `docker compose -f buildout/docker/development/docker-compose.yml up -d`.
4. Created images can be viewed with the command: `docker images`.
5. open docker host / desktop to see if the docker instance. 
6. launch the web url from the docker image / console logs. (which would be on port specified in docker compose e.g: 3001)

## New dev setup
#### Pre requisites:
1. python runtime.
2. pip
#### Steps:
1. Python modules should have a virtual env to run the code  in isolated environment. Run `python -m venv .venv` to create a venv.
2. To Activate the venv, Run `.\.venv\Scripts\Activate`
3. Run the following command `pip install --upgrade --force-reinstall --no-cache-dir -r requirements.txt` to install all dependencies without cache or `pip install -r Requirements.txt` for normal cases.
2. To launch the application `python -m streamlit run main.py`