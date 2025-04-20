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

### Project Dashboard

<img width="1072" alt="image" src="https://github.com/user-attachments/assets/7612846d-257c-4e0a-a39d-1a42734f3f7d" />

You can view the above Tableau dashboard using [this link](https://public.tableau.com/views/SP500-Stock-Screener_17451228916630/StockScreener?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

### Project Description

1. The aim of the project is to identify S&P500 stocks that filter strong investment opportunities based on fundamentals on a weekly basis.
2. The stocks are evaluated on several metrics and criteria which are loosely based on the [Warren Buffet and the Interpretation of Finanicial Statements](https://www.youtube.com/watch?v=lBBXmim527A&t=685s) video by [@TheSwedishInvestor](https://www.youtube.com/@TheSwedishInvestor).
3. The yfinance python module is used to pull the most up to date fundamentals data for S&P500 stocks.
4. In the dashboard you will be able to see several details regarding each stock in the Fundamentals section. You can click on one of the stock tickers and then scroll down to find quarterly and annual earnings, revenue, debt and several other metrics for the selected ticker
5. The symbol on the right in the Fundamentals section is green when all of the below conditions are met:
  * P/E Ratio is between 0 and 50
  * P/B Ratio is less than the industry average or less than 10
  * Gross margin is more than 20% and net margin is more than 10%
  * Return on equity is more than 5% and return on assets is more than 5% too.
6. If some of the above conditions are met, the symbol to the right is yellow and if none of the conditions are met then it is red!
7. A reader can view this dashboard on a weekly basis to make investment decisions.

### Setup & Deploy
Please refer to [setup-and-deploy](setup-and-deploy.md) file for more details regarding infrastructure setup and project deployment.

