# Basketball Stats Backend

Used to scrape NBA statistics from the popular site https://www.basketball-reference.com/

This project is capable of scraping player info/statistics and then writting to a AWS DynamoDB database. It also can query the database and return results in JSON format for use as a REST API.

Project is built to be used as a [AWS lambda layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).
