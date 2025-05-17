# NexaBank45

NexaBank45 is a Python-based banking application designed to manage user accounts, transactions, and provide essential banking functionalities. This README documents the setup, usage, and development process for the project.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Project Overview
NexaBank45 is designed to support the development of a machine learning model for customer churn prediction. The project focuses on building a robust data engineering pipeline that ingests real-time, multi-source customer data, cleans and integrates it, and prepares high-quality datasets for predictive analytics. This enables the marketing team to proactively identify and retain at-risk customers through targeted interventions.

## Features

- **Real-time Data Ingestion**  
    Supports continuous intake of data in various file formats including CSV, JSON, and Parquet.
- **Schema Validation**  
    Automatically validates incoming data against predefined schemas to ensure consistency and integrity. Files with invalid schemas are moved to an unprocessed directory.
- **ETL Pipeline**  
    Extracts, processes, and transforms data before loading it into HDFS for scalable storage. Files are loaded into directories partitioned by date and hour.
- **File Management**  
    After processing, files are removed from the incoming data directory and moved to an archive directory to prevent reprocessing.
- **Hive Integration**  
    Loads data into a structured Hive schema for efficient querying and analysis.
- **Step-by-Step Logging**  
    Logs each stage of the pipeline to provide transparency and aid in debugging.
- **Failure Monitoring and Alerts**  
    Detects pipeline failures in real time and sends automated email notifications to alert stakeholders.


## Project Structure
```
NexaBank45/
├── ETL/                   # Contains extractors, transformers, and loaders for the ETL 
│   ├── extractors/
│   ├── transformers/
│   └── loaders/
├── generator/             # Generates files in the incoming data directory
├── hadoop/                # Sets up Hadoop requirements and Dockerfile
├── utils/                 # Utility modules
│   ├── FileProcessor.py      # Handles file processing tasks
│   ├── email_notifier.py     # Sends email alerts on pipeline failure
│   ├── logger.py             # Logging functionality
│   ├── registry.py           # Maps data and defines file schemas for validation
│   ├── encryption.py         # Handles encryption logic
│   └── ValidWords.py         # List of valid words for the encryptor
├── hiveschema.sql          # SQL script to create Hive schema and tables reading from HDFS files
├── main.py                 # Entry point with the pipehandler method to orchestrate the pipeline flow
└── README.md               # Project documentation
```
- `ETL/`: Modular ETL components for data extraction, transformation, and loading.
- `generator/`: Scripts to generate incoming data files.
- `hadoop/`: Hadoop setup and Docker configuration.
- `utils/`: Helper modules for processing, notifications, logging, schema mapping, and encryption.


## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yomnaafifi/NexaBank45.git
    cd NexaBank45
    ```

2. **Start the Hadoop container:**
    ```bash
    docker compose up -d
    ```
    This command sets up the Hadoop environment and installs all required dependencies as specified in the Dockerfile.

3. **Access the application container:**
    ```bash
    docker exec -it hadoop-python bash
    ```


## Usage

Follow these steps to run NexaBank45:

1. **Generate Sample Data**
    ```bash
    cd generator
    python3 generator.py
    cd ..
    ```

2. **Run the Main Application**
    ```bash
    python3 main.py
    ```

This will start the ETL pipeline and process the generated data.


## License
This project is licensed under the MIT License.
