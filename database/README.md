Creating a dynamodb table locally:

1. In 'database' directory: 'docker-compose up' to start the local dynamodb server
2. 'aws dynamodb create-table --cli-input-json file://tables.json --endpoint-url http://localhost:8000'

Adding an item to a table: 'aws dynamodb put-item --table-name system --item '{"pk": {"S": "ID#ryan"}, "sk": {"S": "VIDEO#1"}, "videoTitle": {"S": "CrazyCats"}}' --endpoint-url http://localhost:8000'

Scanning a table: 'aws dynamodb scan --table-name system --endpoint-url http://localhost:8000'
