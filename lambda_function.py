import boto3
import os
from PIL import Image
import io
import datetime

# We get our clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb') ### NEW ###

def lambda_handler(event, context):
    
    # 1. Get the bucket and key (filename) from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # 2. Get environment variables
    dest_bucket_name = os.environ['DEST_BUCKET']
    db_table_name = os.environ['DB_TABLE'] ### NEW ###
    
    # Connect to the DynamoDB table
    table = dynamodb.Table(db_table_name) ### NEW ###
    
    # 3. Download the original image from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        image_data = response['Body'].read()
        image = Image.open(io.BytesIO(image_data))
        
        # 4. Create the thumbnail (max 200x200)
        image.thumbnail((200, 200))
        
        # 5. Save the thumbnail back to a new in-memory buffer
        buffer = io.BytesIO()
        image_format = image.format if image.format else 'JPEG'
        image.save(buffer, format=image_format)
        buffer.seek(0)
        
        # 6. Upload the new thumbnail to the destination bucket
        new_key = f"thumbnails/{os.path.basename(file_key)}"
        
        s3_client.put_object(
            Bucket=dest_bucket_name,
            Key=new_key,
            Body=buffer,
            ContentType=f'image/{image_format.lower()}'
        )
        
        print(f"Successfully resized {file_key} and saved to {dest_bucket_name}/{new_key}")
        
        # 7. Log the successful job to DynamoDB
        try:
            timestamp = str(datetime.datetime.now())
            table.put_item(
                Item={
                    'original_key': file_key,
                    'thumbnail_key': new_key,
                    'timestamp': timestamp,
                    'status': 'SUCCESS'
                }
            )
            print("Successfully logged to DynamoDB")
        except Exception as e:
            # Don't fail the whole function if logging fails
            print(f"Error logging to DynamoDB: {str(e)}")
        
    except Exception as e:
        print(f"Error processing image {file_key}: {str(e)}")
        
        # Log the failure to DynamoDB
        try:
            timestamp = str(datetime.datetime.now())
            table.put_item(
                Item={
                    'original_key': file_key,
                    'thumbnail_key': 'N/A',
                    'timestamp': timestamp,
                    'status': 'FAILED',
                    'error': str(e)
                }
            )
            print("Successfully logged FAILURE to DynamoDB")
        except Exception as e_db:
            print(f"Error logging FAILURE to DynamoDB: {str(e_db)}")
        
        raise e
