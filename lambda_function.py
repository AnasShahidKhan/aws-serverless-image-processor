import boto3
import os
from PIL import Image
import io

# We get our S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    # 1. Get the bucket and key (filename) from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # 2. Get the destination bucket name from an Environment Variable
    # We will set this in the console later.
    dest_bucket_name = os.environ['DEST_BUCKET']
    
    # 3. Download the original image from S3
    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the image data into memory
        image_data = response['Body'].read()
        
        # Use PIL to open the image from memory
        image = Image.open(io.BytesIO(image_data))
        
        # 4. Create the thumbnail (max 200x200)
        image.thumbnail((200, 200))
        
        # 5. Save the thumbnail back to a new in-memory buffer
        # We need to save it in the same format (e.g., JPEG, PNG)
        buffer = io.BytesIO()
        image_format = image.format if image.format else 'JPEG'
        image.save(buffer, format=image_format)
        
        # Reset the buffer's position to the beginning
        buffer.seek(0)
        
        # 6. Upload the new thumbnail to the destination bucket
        # We'll create a new name for it, e.g., "thumbnails/my-image.jpg"
        new_key = f"thumbnails/{os.path.basename(file_key)}"
        
        s3_client.put_object(
            Bucket=dest_bucket_name,
            Key=new_key,
            Body=buffer,
            ContentType=f'image/{image_format.lower()}'
        )
        
        print(f"Successfully resized {file_key} and saved to {dest_bucket_name}/{new_key}")
        
    except Exception as e:
        print(f"Error processing image {file_key}: {str(e)}")
        raise e