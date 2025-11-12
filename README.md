# AWS Serverless Image Processor

A simple, event-driven, serverless application built on AWS to automatically create thumbnails for uploaded images.

This project was built as part of my portfolio to demonstrate skills in cloud computing, serverless architecture, and Python.

## 🚀 How It Works

This application uses a full-stack serverless pattern:

1.  A user uploads an image to an S3 bucket (`anas-shahid-su-uploads-2025`).
2.  The S3 `ObjectCreated` event triggers an AWS Lambda function.
3.  The Lambda function (Python) downloads the image, resizes it using the Pillow library, and uploads the new thumbnail to a separate S3 bucket.
4.  Finally, the function logs the job details (original filename, new thumbnail key, timestamp, and status) to a **DynamoDB** table for persistence and tracking.



## 🛠️ Tech Stack

* **AWS Lambda:** For serverless compute (Python 3.13).
* **AWS S3:** For object storage and event triggers.
* **AWS DynamoDB:** As a NoSQL database for logging and data persistence.
* **AWS IAM:** To create secure, least-privilege execution roles.
* **AWS CloudWatch:** For logging and debugging.
* **AWS Lambda Layers:** To package and provide the `Pillow` (PIL) library to the function.
* **Python:** The core logic.
* **Boto3:** The AWS SDK for Python used within the Lambda function.

## 🐛 Challenges & Debugging

The main challenge was correctly packaging the `Pillow` library in a Lambda Layer. The initial build failed with a `Runtime.ImportModuleError (_imaging)` because the library was compiled for the wrong architecture.

**Solution:** I rebuilt the layer using a `pip install` command with specific flags (`--platform manylinux2014_x86_64`, `--implementation cp`) to build a binary compatible with the Amazon Linux 2 (x86_64) Lambda environment.
