from util import get_client
import io

def upload_s3(bucket, file_prefix, filename, df):
    s3_client = get_client()

    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        response = s3_client.put_object(
            Bucket=bucket, Key=f'{file_prefix}/{filename}', Body=csv_buffer.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")