# AWS Serverless Image Processor

A simple, event-driven, serverless application built on AWS to automatically create thumbnails for uploaded images.

This project was built as part of my portfolio to demonstrate skills in cloud computing, serverless architecture, and Python.

## 🚀 How It Works

This application uses a pure serverless architecture:

1.  A user uploads an original image to an S3 bucket (`anas-shahid-su-uploads-2025`).
2.  The S3 bucket (using an S3 Event Notification) triggers an AWS Lambda function.
3.  The Lambda function (written in Python) downloads the image, uses the `Pillow` library to create a 200x200px thumbnail.
4.  The function then uploads the new thumbnail to a separate S3 bucket (`anas-shahid-su-thumbnails-2025`).



## 🛠️ Tech Stack

* **AWS Lambda:** For serverless compute (Python 3.13 runtime).
* **AWS S3:** For object storage (one bucket for uploads, one for thumbnails).
* **AWS IAM:** To create a secure execution role, granting the Lambda function specific, least-privilege permissions to read/write to the correct buckets.
* **AWS CloudWatch:** For logging and debugging.
* **AWS Lambda Layers:** To package and provide the `Pillow` (PIL) library to the function.
* **Python:** The core logic.
* **Boto3:** The AWS SDK for Python used within the Lambda function.

## 🐛 Challenges & Debugging

The main challenge was correctly packaging the `Pillow` library in a Lambda Layer. The initial build failed with a `Runtime.ImportModuleError (_imaging)` because the library was compiled for the wrong architecture.

**Solution:** I rebuilt the layer using a `pip install` command with specific flags (`--platform manylinux2014_x86_64`, `--implementation cp`) to build a binary compatible with the Amazon Linux 2 (x86_64) Lambda environment.
