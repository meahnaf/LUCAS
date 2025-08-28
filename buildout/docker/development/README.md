How to deploy the application to Azure cloud?
We use Azure container registry to push docker images and azure service app to run the image.

Steps to push image to ACR:
1. Git checkout origin main
2. Git pull
3. Login to the required tenant using `az login --tenant eff1c4dc-fab6-4b7b-a133-6f85f234331e --use-device-code`
4. Login to ACR cli using `az acr login --name kuberviztest` (make sure you have access to this from portal.)
5. Run this command to build the docker image: `docker compose -f buildout/docker/development/docker-compose.yml build --no-cache`
6. View docker images in your local usingL `docker images`
7. Tag the docker image appropriately using `docker tag chatrag-service kuberviztest.azurecr.io/chatrag:v0.0.0`
8. Push the docker image to ACR using `docker push kuberviztest.azurecr.io/chatrag:v0.0.0`
9. This should refelct on the portal.

Steps to run the docker container using above image:
1. Use ACR as source and deploy to container app on azure. 


Prerequisites:
1. Install AZ CLI (add the path in the environment variable)
