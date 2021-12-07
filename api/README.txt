1) install sam cli: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html
2) install docker-compose: https://docs.docker.com/compose/install/
3) in 'database' directory: docker-compose up
4) in 'api' directory: 
5) sam build
6) sam local start-api --docker-network sam-backend -p 3001