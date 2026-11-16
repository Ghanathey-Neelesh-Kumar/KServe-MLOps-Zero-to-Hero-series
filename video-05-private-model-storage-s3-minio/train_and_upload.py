import boto3
import joblib
from sklearn import datasets, svm

# 1. Train
X, y = datasets.load_iris(return_X_y=True)
model = svm.SVC(gamma="scale").fit(X, y)
joblib.dump(model, "model.joblib")

# 2. Upload to MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
)
s3.create_bucket(Bucket="models")
s3.upload_file("model.joblib", "models", "iris/model.joblib")
print("Uploaded to s3://models/iris/")
