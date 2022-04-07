
######################################################
# CosmosDB Database Configuration
######################################################
cosmosDBString = "mongodb://cs5412-final-project-cosmosdb:7NTur9WLYF1d61UlU16shuaEDi2WJwBI78tvwhpVidrqXl83p2qBSchBAOVE1jYKCkgTNiHoe9hHHuhaLHxKvw==@cs5412-final-project-cosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cs5412-final-project-cosmosdb@"
localMongoString = "mongodb://127.0.0.1:27017"
mongoDatabaseName = "cs5412-cl2228"


######################################################
# Azure Blob Storage Configuration
######################################################
azureStorageConnectString = "DefaultEndpointsProtocol=https;AccountName=cs5412finalproject;AccountKey=IY/FhO+zJy+jui2TmIcHKp3uyWEZ/9eAxx/DnSsa0edvVOFIJnJrSiEKLYxUCXUBy8HRieupaXfg+AStBlMzjg==;EndpointSuffix=core.windows.net"
blobDefaultContainer = "cs5412-cl2228"


######################################################
# Azure Face Configuration
######################################################
azureFaceEndpoint = "https://cs5412-final-project-face.cognitiveservices.azure.com/"
azureFaceKey = "76ee4fb193164c268cbc04de33df7054"


######################################################
# Email Configuration
######################################################
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "cs5412.cl2228@yahoo.com"
SMTP_PASSWORD = "jwmavztrdbudzxgb"
EMAIL_FROM = "cs5412.cl2228@yahoo.com"


######################################################
# JWT Configuration
######################################################
jwtExpireMinutes = 180
jwtLoginExpireMinutes = 30
jwtGuestExpireMinutes = 30
jwtSecretKey = "cs5412-cl2228"
jwtAlgorithm = "HS256"
