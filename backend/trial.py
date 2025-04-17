# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#     .appName("Test") \
#     .master("local[*]") \
#     .getOrCreate()

# df = spark.range(5).toDF("numbers")
# df.show()


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend

# # Load CSV into Pandas DataFrame
# df = pd.read_csv("jobs_in_data.csv")  # Make sure this file exists locally

# @app.route('/api/jobs_in_data', methods=['GET'])
# def get_salary_data():
#     job_title = request.args.get('job_title')
#     job_category = request.args.get('job_category')
#     salary = request.args.get('salary', type=int)

#     filtered_df = df.copy()

#     if job_title:
#         filtered_df = filtered_df[filtered_df['job_title'] == job_title]
#     if job_category:
#         filtered_df = filtered_df[filtered_df['job_category'] == job_category]
#     if salary:
#         filtered_df = filtered_df[filtered_df['salary_in_usd'] <= salary]

#     # Group by employee_residence and get average salary
#     salary_summary = (
#         filtered_df.groupby("employee_residence")["salary_in_usd"]
#         .mean()
#         .reset_index()
#         .rename(columns={"salary_in_usd": "average_salary"})
#     )

#     return jsonify(salary_summary.to_dict(orient="records"))

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

import os
os.environ['HADOOP_HOME'] = 'C:\\hadoop'  # replace with your actual path

from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("ReadFromS3") \
    .getOrCreate()

# Replace with your actual S3 path
s3_path = "s3a://mrunalproject/jobs_in_data.csv"

# Read the CSV file from S3
df = spark.read.csv(s3_path, header=True, inferSchema=True)

# Show the data
df.show(5)

# Stop the SparkSession
spark.stop()
