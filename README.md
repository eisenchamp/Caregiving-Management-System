# Caregiving Management System

## Overview

The Caregiving Management System is a comprehensive database and application system designed to manage and analyze caregiver and job application data. This project includes the creation of SQL database schema, data manipulation, and analysis using Python. The system supports functionalities such as updating user information, managing caregiver rates, and generating insightful reports based on job applications and appointments.

## Features

- **Database Schema**: Defined tables for `USER`, `MEMBER`, `CAREGIVER`, `ADDRESS`, `JOB`, `JOB_APPLICATION`, and `APPOINTMENT`.
- **Data Manipulation**: Executed SQL queries to update user phone numbers, adjust caregiver rates, and delete records.
- **Data Analysis**: Performed queries to analyze accepted appointments, calculate total costs, and determine average pay and caregiver earnings.
- **Integrity Constraints**: Maintained relationships between tables using primary and foreign keys to ensure data consistency.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eisenchamp/Caregiving-Management-System
   ```
2. **Setup the Database**:

- Ensure you have PostgreSQL installed.
- Run the provided SQL scripts to create the necessary tables in your PostgreSQL database.
3. **Configure the Connection**:

- Update the database connection settings in your Python script or configuration file as needed.
4.  **Run the Python Scripts**:

- Execute the Python scripts to perform data manipulation and analysis.

## Usage
1. **Update User Information**:

- Modify phone numbers of users by running the provided Python script.
2. **Adjust Caregiver Rates**:

- The script adjusts caregiver hourly rates based on specified conditions.
3. **Generate Reports**:

- Run the Python script to generate reports on job applications, caregiver earnings, and appointment statistics.

## SQL Schema
The following SQL scripts define the database schema:

- CREATE_TABLE_ADDRESS.sql
- CREATE_TABLE_APPOINTMENT.sql
- CREATE_TABLE_CAREGIVER.sql
- CREATE_TABLE_JOB.sql
- CREATE_TABLE_JOB_APPLICATION.sql
- CREATE_TABLE_MEMBER.sql
- CREATE_TABLE_USER.sql
  
These scripts create tables with appropriate constraints and relationships.

## Python Scripts
- Data Manipulation: Includes updates and deletions based on specified conditions.
- Data Analysis: Queries for generating insights and reports.
