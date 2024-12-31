# Project setup details

## Steps to create infrastructure and set up project (I used a Linux VM running on EC2)

### 1. Clone this git repo.
- You can add your own custom stock picking logic to the [main.py](scripts/main.py) python file

### 2. Build a docker container named stock-screener, tag it and push to ECR.
  - Navigate to the scripts folder to locate the python scripts and docker container definition file (Dockerfile)
  - Install docker on the VM using the follow commands if not already installed:
  ```
  sudo yum update -y
  sudo amazon-linux-extras install docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  ```
  - Build the docker container using ```docker build -t stock-screener```.
  - Create a new repository on AWS ECR. I named my repository as ```finance/stock-screener```.
  - Tag the docker container using ```docker tag stock-screener:<ECR Repository URI>```.
  - Authenticate AWS ECR ```aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <ECR Repository URI>```
  - Push the tagged image to the ECR repository ```docker push <ECR Repository URI>:latest```

### 3. Set up AWS Batch environment.
  - Create IAM role for S3 access
  - Create a compute environment:
    - Go to the AWS Batch console.
    - Click Compute Environments > Create.
    - Choose Managed Compute Environment.
    - Name the compute environment (e.g., stock-info-compute-env).
    - Choose On-Demand or Spot Instances.
    - Set vCPUs and instance types based on your expected workload.
    - Click Create.
  - Create a job queue:
    - In the AWS Batch console, click Job Queues > Create.
    - Name the queue (e.g., stock-info-job-queue).
    - Set priority and associate the compute environment you created.
    - Click Create.
  - Create a job definition:
    - Go to AWS Batch console.
    - Click Job Definitions > Create.
    - Provide a name like stock-info-fetcher-job.
    - Select the compute environment (EC2 or Fargate).
    - Image URI: Provide the URI of your Docker image from ECR.
    - Set resources like vCPUs and memory (based on your job's needs).
    - Choose the IAM role created in step 2.
    - Click Create.
  - Submit a job:
    - Go to AWS Batch console.
    - Click Jobs > Submit Job.
    - Provide a name (e.g., fetch-stock-data-job).
    - Choose the job definition (stock-info-fetcher-job) and job queue (stock-info-job-queue).
    - Specify parameters if your script takes any (e.g., tickers, S3 output path).
    - Click Submit.
  - Monitor job and verify output:
    - Use the AWS Batch console to track the job's status (from SUBMITTED to RUNNING and SUCCEEDED).
    - View logs in Amazon CloudWatch to ensure there are no errors during execution.
    - Once the job completes, verify the output in your S3 bucket to ensure the stock data is written correctly.

### 4. Create an EventBridge rule for AWS Batch job scheduling
  - Create or Modify an IAM Role for EventBridge Scheduler with the following managed policies:
    - AWSBatchSubmitJob: This policy allows EventBridge to submit jobs to AWS Batch.
    - CloudWatchLogsFullAccess: (Optional) If you want EventBridge to log the job output to CloudWatch, this permission is useful for debugging and monitoring.
  - Name the role something descriptive, like EventBridgeBatchJobRole.
  - Search for EventBridge in the console and select it.
  - Create a Rule:
    - In the EventBridge dashboard, click Create rule.
  - Configure Rule Details:
    - Name: Enter a name for your rule, such as BatchJobFriday3PM.
    - Description: (Optional) Add a description, like "Run Batch job every Friday at 3 PM PT."
    - Event bus: Choose the default event bus unless you are using a custom one.
    - Rule type: Choose Schedule.
    - Assign the IAM Role to EventBridge Scheduler
  - Define Schedule Pattern:
    - In the Schedule pattern section, choose Cron expression.
    - Use the following Cron expression to run every Friday at 3 PM PT: ```0 22 ? * 6 *```
  - Choose Target:
    - Under Select a target, choose AWS service.
    - From the Target dropdown, select Batch job queue.
  - Configure Target (AWS Batch Job Queue):
    - Job queue: Select the AWS Batch job queue you created for your job.
    - Job definition: Select the appropriate Batch job definition.
    - Job name: Enter a job name, like FridayStockDataFetch.
    - Job attempts: Optionally, specify the number of retry attempts if the job fails.
    - Array size: Keep this at 1 unless you're running an array job.
  - If your job needs any input parameters (like specific stock tickers or S3 paths), you can pass them as JSON in the Constant (JSON text) field.
  - Create the Rule:
    - After configuring the target, click Create to save the rule.
  - Monitoring and Logs:
    - You can monitor your scheduled jobs using AWS CloudWatch. Go to the CloudWatch console and check the Logs for your Batch jobs.
    - Each execution of the job will generate logs that you can view for troubleshooting or verification.
  - Check EventBridge Rule Execution:
    - Go back to the EventBridge console and navigate to Rules to see your rule's status.
    - You can see the next scheduled execution and verify if the rule triggers the job at the right time.

### 5. Create input and output S3 paths as defined in the scripts
  - Here are the S3 buckets and folders I have used for my project. The same details can be found in the scripts/main.py file and should be updated by you during project setup
    - bucket = 'fin-fj'
    - input_file_prefix = 'input'
      - the input file is stored in fin-fj/input/sp500_tickers.csv
      - the input file used can be found on [Kaggle](https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks?resource=download)
      - I have only retained the ticket symbol, the stock's long name, its sector and its industry and saved the file as sp500_tickers.csv
    - output_file_prefix = 'output'
      - the output file is stored in fin-fj/output/sp500/<YYY-MM-DD>/sp500_tickers.csv
      - in the above path <YYYY-MM-DD> implies the date of the project run

### 6. Allow the batch job to run on a weekly cadence and save the output to the S3 folder specified above
- For testing purposed, you can also clone wht batch job and trigger it manually

### 7. Use AWS Glue crawlers to create data catalog
- Set Up AWS Glue Job:
  - Create an AWS Glue ETL job to extract data from the S3 bucket and load it into the RDS database.
  - Glue can handle a variety of file formats like CSV, Parquet, and JSON.
- Use Glue Data Catalog:
  - Catalog your S3 files using a Glue Crawler to define the schema.
  - Set up a Glue Job to read from the S3 location, perform transformations (if necessary), and write the data to the RDS instance.
- Schedule the Glue Job:
  - Schedule the Glue job to run at regular intervals using Amazon EventBridge or manually trigger it based on new file uploads.
- This data catalog can be used to query the S3 data from AWS Athena

### Connect Tableau to output data using Athena connector
- Open Tableau and choose Amazon Athena as your data source.
- Enter Connection Details:
  - AWS Region: Select the region where your Athena tables and S3 data are located.
  - S3 Staging Directory: Provide the full S3 path to the bucket where query results will be temporarily stored.
  - Authentication:
    - Use either Access Key & Secret Key or the AWS Profile.
  - Database: Select the database you wish to query from Athena.
- Sign In: After entering the necessary details, click Sign In to establish the connection.
- Choose Tables or Write Custom Queries:
  - Once connected, you will be able to select tables or write custom SQL queries to query your S3 data via Athena.
- You can view and replicate the Tableau dashboard that I have connected using [this link](https://public.tableau.com/views/SP500-Stock-Screener/StockScreener?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)