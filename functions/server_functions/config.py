############################################################################
# Azure keys
############################################################################
azureStorageConnectString = "DefaultEndpointsProtocol=https;AccountName=cs5412finalproject;AccountKey=IY/FhO+zJy+jui2TmIcHKp3uyWEZ/9eAxx/DnSsa0edvVOFIJnJrSiEKLYxUCXUBy8HRieupaXfg+AStBlMzjg==;EndpointSuffix=core.windows.net"
azureFaceKey = "76ee4fb193164c268cbc04de33df7054"
azureFaceEndpoint = "https://cs5412-final-project-face.cognitiveservices.azure.com/"
cosmosDBString = "mongodb://cs5412-final-project-cosmosdb:7NTur9WLYF1d61UlU16shuaEDi2WJwBI78tvwhpVidrqXl83p2qBSchBAOVE1jYKCkgTNiHoe9hHHuhaLHxKvw==@cs5412-final-project-cosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cs5412-final-project-cosmosdb@"

localMongoString = "mongodb://127.0.0.1:27017"


############################################################################
# MongoDB configuration
############################################################################
mongoDatabaseName = "cs5412-cl2228"


############################################################################
# Blob configuration
############################################################################
blobDefaultContainer = "cs5412-cl2228"


############################################################################
# JWT configuration
############################################################################
jwtSecretKey = "cs5412-cl2228"
jwtExpireMinutes = 180
jwtGuestExpireMinutes = 30
jwtAlgorithm = "HS256"


############################################################################
# Email configuration
############################################################################
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "cs5412.cl2228@yahoo.com"
SMTP_PASSWORD = "jwmavztrdbudzxgb"
EMAIL_FROM = "cs5412.cl2228@yahoo.com"
