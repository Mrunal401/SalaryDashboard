# from flask import Flask, request, jsonify
# from pyspark.sql import SparkSession

# app = Flask(__name__)
# spark = SparkSession.builder.appName("SalaryData").getOrCreate()

# df = spark.read.csv("dataset/jobs_in_data.csv", header=True, inferSchema=True)

# @app.route('/filter', methods=['POST'])
# def filter_data():
#     data = request.json
#     job_field = data['job_field']
#     job_profile = data['job_profile']
#     salary_range = data['salary_range']

#     filtered = df.filter((df['job_field'] == job_field) & 
#                          (df['job_profile'] == job_profile) & 
#                          (df['salary_range'] == salary_range))

#     result = filtered.groupBy("location").avg("salary").orderBy("avg(salary)", ascending=False)
#     return jsonify(result.toPandas().to_dict(orient='records'))

# app.run(debug=True)

#Basic spark job gets started...............

# # quick_test.py
# from pyspark.sql import SparkSession
# spark = SparkSession.builder.appName("Test").getOrCreate()
# print(spark.version)

from pyspark.sql import SparkSession
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.sql.functions import col, avg
#from pyspark.ml.feature import VectorAssembler
#from pyspark.ml.regression import RandomForestRegressor
#from pyspark.ml import Pipeline
#from pyspark.ml.evaluation import RegressionEvaluator
#import pyspark.sql.functions as func
#from pyspark.sql.functions import when, count, lit

#S3_DATA_SOURCE_PATH = "s3://mrunalproj/jobs_in_data.csv"
S3_DATA_SOURCE_PATH = "jobs_in_data.csv"
#S3_DATA_OUTPUT_PATH = "s3://advancedbmrunu/output_model"

spark = SparkSession.builder.appName("SalaryAnalysis").getOrCreate()

df = spark.read.csv(S3_DATA_SOURCE_PATH, header=True, inferSchema=True)
df.show()

df.printSchema()

df.describe().show()

#to show avg salary for a job category and title at a particular location
job_title = sys.argv[1] if len(sys.argv) > 1 else ""
job_category = sys.argv[2] if len(sys.argv) > 2 else ""
salary_usd = sys.argv[3] if len(sys.argv) > 3 else ""
salary = sys.argv[4] if len(sys.argv) > 4 else ""

# Filter the DataFrame
filtered_df = df

if job_title:
    filtered_df = filtered_df.filter(df["job_title"] == job_title)

if job_category:
    filtered_df = filtered_df.filter(df["job_category"] == job_category)

if salary and salary_usd:
    filtered_df = filtered_df.filter(
        (df["salary_in_usd"].cast("int") >= int(salary)) &
        (df["salary_in_usd"].cast("int") <= int(salary_usd))
    )

# Group by location (employee_residence) and calculate average salary (salary)
salary_summary = (
    filtered_df
    .groupBy("employee_residence")
    .agg({"salary": "avg"})
    .withColumnRenamed("avg(salary)", "average_salary")
)

# Show the result
salary_summary.show(84, truncate=False)

#-----------------------------------------------
#to show avg salary for a job category and title at a particular location

# Convert salary range to int (if not empty)
min_salary = int(min_salary) if min_salary else None
max_salary = int(max_salary) if max_salary else None

# Filter DataFrame
filtered_df = df

if job_category:
    filtered_df = filtered_df.filter(col("job_category") == job_category)

if location:
    filtered_df = filtered_df.filter(col("location") == location)

if min_salary is not None and max_salary is not None:
    filtered_df = filtered_df.filter(
        (col("salary_usd").cast("int") >= min_salary) & 
        (col("salary_usd").cast("int") <= max_salary)
    )

# Group by job title and compute average salary
result_by_job = (
    filtered_df
    .groupBy("_c1")  # Assuming _c1 is job title
    .agg(avg("_c5").alias("average_salary"))  # Assuming _c5 is salary column
    .orderBy("average_salary", ascending=False)
    .toPandas()
)

# Display result using print or visualize with seaborn/matplotlib
print(result_by_job)



# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(data=result_by_job.head(10), x="average_salary", y="job_title", palette="viridis")
plt.title("Top 10 Highest Paying Job Titles")
plt.xlabel("Average Salary (USD)")
plt.ylabel("Job Title")
plt.tight_layout()
plt.show()






# # Create input widgets
# dbutils.widgets.text("_c1", "")        # Job Title
# dbutils.widgets.text("_c2", "")        # Job Category
# dbutils.widgets.text("_c5", "")        # Salary USD (Max)
# dbutils.widgets.text("_c4", "")        # Salary (Min)

# # Get widget values
# job_title = dbutils.widgets.get("_c1")
# job_category = dbutils.widgets.get("_c2")
# salary_usd = dbutils.widgets.get("_c5")
# salary = dbutils.widgets.get("_c4")

# # Filter the DataFrame based on input
# filtered_df = df

# if job_title:
#     filtered_df = filtered_df.filter(df["_c1"] == job_title)

# if job_category:
#     filtered_df = filtered_df.filter(df["_c2"] == job_category)

# if salary and salary_usd:
#     filtered_df = filtered_df.filter((df["_c5"].cast("int") >= int(salary)) & 
#                                      (df["_c5"].cast("int") <= int(salary_usd)))

# # Group by location (_c6) and calculate average salary (_c4)
# salary_summary = (
#     filtered_df
#     .groupBy("_c6")
#     .agg({"_c4": "avg"})
#     .withColumnRenamed("avg(_c4)", "average_salary")
#     .toPandas()
# )

# salary_summary.show()

#Code

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pyspark.sql import SparkSession
# import pandas as pd

#  # Initialize Flask
# app = Flask(__name__)
# CORS(app)  # Allow React to fetch data from Flask

# # Initialize PySpark
# spark = SparkSession.builder \
#     .appName("SalaryAnalysis").getOrCreate()
#     #.config("spark.jars", "jars/hadoop-aws-3.1.1.jar,jars/aws-java-sdk-bundle-1.11.1026.jar") \
#     #.getOrCreate()

# # Optional: AWS Credentials (if your S3 bucket is private)

# S3_DATA_SOURCE_PATH = "s3://mrunalproj/jobs_in_data.csv"

# Load dataset
#df = spark.read.csv("s3://mrunalproj/jobs_in_data.csv")
df = spark.read.csv(S3_DATA_SOURCE_PATH, header=True, inferSchema=True)

# @app.route('/api/jobs_in_data', methods=['GET'])
# def get_salary_data():
#     """Return salary data based on selected filters"""
#     job_title = request.args.get('job_title')
#     job_category = request.args.get('job_category')
#     salary_usd = request.args.get('salary_in_usd', type=int)
#     salary = request.args.get('salary', type=int)

#     # Apply filters
#     filtered_df = df
#     if job_title:
#         filtered_df = filtered_df.filter(df.job_title == job_title)
#     if job_category:
#         filtered_df = filtered_df.filter(df.job_category == job_category)
#     if salary_usd and salary:
#         filtered_df = filtered_df.filter((df.salary_usd >= salary) & (df.salary_usd <= salary))

#     # Group by location and get average salary
#     salary_summary = filtered_df.groupBy("employee_residence").avg("salary").toPandas()

#     return jsonify(salary_summary.to_dict(orient="records"))  # Send JSON to React

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


# from pyspark.sql import SparkSession

# def load_csv_from_s3():
#     spark = SparkSession.builder \
#         .appName("Salary Dashboard") \
#         .getOrCreate()

#     s3_path = "s3://mrunalproject/jobs_in_data.csv"

#     df = spark.read.csv(s3_path, header=True, inferSchema=True)

#     df.printSchema()
#     df.show(10)

# if __name__ == "__main__":
#     load_csv_from_s3()
