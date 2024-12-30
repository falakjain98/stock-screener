### Project Summary

This project will allow you to deploy your custom stock filtering pipeline to identify S&P500 stock tickers displaying strong value using fundamental data from quarterly and annual filings.

The following technologies are utilized in this project:
- [AWS Services](https://aws.amazon.com): *Cloud Platform*
  - [S3](https://aws.amazon.com/pm/serv-s3/?trk=20e04791-939c-4db9-8964-ee54c41bc6ad&sc_channel=ps&ef_id=CjwKCAiAg8S7BhATEiwAO2-R6mBKk1ekfVv4LYmwUAn62jHPMDM_HuiGWwe448qKcGNI6TwHCj8cchoCod8QAvD_BwE:G:s&s_kwcid=AL!4422!3!651751060962!e!!g!!aws%20s3!19852662362!145019251177&gbraid=0AAAAADjHtp8uGzbJhlK16CdVDpsDXt27U&gclid=CjwKCAiAg8S7BhATEiwAO2-R6mBKk1ekfVv4LYmwUAn62jHPMDM_HuiGWwe448qKcGNI6TwHCj8cchoCod8QAvD_BwE): *Input and Output Storage*
  - [Batch](https://aws.amazon.com/batch/): *Batch Jobs*
  - [ECR](https://aws.amazon.com/ecr/): *Docker Container Store*
  - [EventBridge](https://aws.amazon.com/eventbridge/): *Job Scheduling*
  - [Glue](https://aws.amazon.com/glue/): *Data Discovery and Cataloging*
  - [Athena](https://aws.amazon.com/athena/): *Data Integration*
- [Docker](https://www.docker.com): *Containerization*
- [Python (via Anaconda)](https://www.anaconda.com/products/distribution): *Programming Language*
- [Tableau](https://www.tableau.com): *Data Visualization and Analysis*

### Project Architecture

<img width="849" alt="image" src="https://github.com/user-attachments/assets/047d73c7-06fa-412b-b2f9-47c231621428" />

### Setup & Deploy
Please refer to [setup](setup.md) file for more details regarding infrastructure setup.

After setup, deploy the pipeline using steps on the [deploy](deploy.md) file.

