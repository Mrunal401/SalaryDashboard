# from flask import Flask, request, jsonify
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import avg, col
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Allow cross-origin requests from React frontend

# # Initialize Spark session
# spark = SparkSession.builder.appName("SalaryAnalysis").getOrCreate()


# # Load the dataset (change path if needed)
# df = spark.read.csv("jobs_in_data.csv", header=True, inferSchema=True)
# df.printSchema()

# # Assuming your DataFrame is loaded and accessible
# job_categories = df.select("job_category").distinct().rdd.flatMap(lambda x: x).collect()
# print(job_categories)


# @app.route("/api/test")
# def test():
#     return jsonify(df.limit(5).toPandas().to_dict(orient="records"))


# @app.route('/api/filters', methods=['GET'])
# def get_filter_options():
#     job_titles = [row[0] for row in df.select("job_title").distinct().collect()]
#     job_categories = [row[0] for row in df.select("job_category").distinct().collect()]
#     locations = [row[0] for row in df.select("employee_residence").distinct().collect()]
#     return jsonify({
#         "job_titles": job_titles,
#         "job_categories": job_categories,
#         "employee_residence": locations
#     })


# @app.route('/api/salary-summary', methods=['POST'])
# def salary_summary():
#     data = request.get_json()
#     job_title = data.get("job_title")
#     job_category = data.get("job_category")
#     location = data.get("employee_residence")

#     filtered = df
#     if job_title:
#         filtered = filtered.filter(col("job_title") == job_title)
#     if job_category:
#         filtered = filtered.filter(col("job_category") == job_category)
#     if location:
#         filtered = filtered.filter(col("employee_residence") == location)

#     result = (
#         filtered.groupBy("job_title")
#         .agg(avg("salary_in_usd").alias("average_salary"))
#         .orderBy("average_salary", ascending=False)
#         .toPandas()
#     )

#     return result.to_json(orient="records")

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, avg
# import matplotlib.pyplot as plt
# import io
# import base64

# app = Flask(__name__)
# CORS(app)

# spark = SparkSession.builder.appName("SalaryAnalysis") \
#  .config("spark.jars.packages", ",".join([
#         "org.apache.hadoop:hadoop-aws:3.3.6",
#         "com.amazonaws:aws-java-sdk-bundle:1.11.901"
#     ])) \
#      .getOrCreate()
#     #.config("spark.jars", "file:///C:/spark/jars/hadoop-aws-3.3.6.jar,file:///C:/spark/jars/aws-java-sdk-bundle-1.11.901.jar") \
   


# hadoop_conf = spark._jsc.hadoopConfiguration()
#  #.config("spark.jars", "C:/jars/hadoop-aws-3.3.6.jar,C:/jars/aws-java-sdk-bundle-1.11.901.jar") \
# hadoop_conf.set("fs.s3a.access.key", "AKIASVLKCE7LSGUPRJWA")
# hadoop_conf.set("fs.s3a.secret.key", "YOUR_SECREVLi9tDjoXg2ln3vy1unXpIKugYys5yqQhWUtpLkrT_KEY")
# hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

# df = spark.read.csv("s3a://mrunalproj/jobs_in_data.csv", header=True, inferSchema=True)

# @app.route("/api/test")
# def test():
#     return jsonify(df.limit(5).toPandas().to_dict(orient="records"))

# @app.route('/api/filters', methods=['GET'])
# def get_filter_options():
#     job_titles = [row[0] for row in df.select("job_title").distinct().collect()]
#     job_categories = [row[0] for row in df.select("job_category").distinct().collect()]
#     locations = [row[0] for row in df.select("employee_residence").distinct().collect()]
#     return jsonify({
#         "job_titles": job_titles,
#         "job_categories": job_categories,
#         "locations": locations
#     })

# @app.route('/api/salary-summary', methods=['POST'])
# def salary_summary():
#     try:
#         data = request.get_json()
#         job_title = data.get("job_title")
#         job_category = data.get("job_category")
#         location = data.get("location")

#         filtered = df
#         if job_title:
#             filtered = filtered.filter(col("job_title") == job_title)
#         if job_category:
#             filtered = filtered.filter(col("job_category") == job_category)
#         if location:
#             filtered = filtered.filter(col("employee_residence") == location)

#         result = (
#             filtered.groupBy("employee_residence")
#             .agg(avg("salary").alias("average_salary"))
#             .orderBy("average_salary", ascending=False)
#             .toPandas()
#         )
#         #return jsonify(result.to_dict(orient="records"))

#         #return result.to_json(orient="records")

    
#         # If the result is empty, return a response message
#         if result.empty:
#             return jsonify({"message": "No data found for the selected filters"}), 404

#         # Create a plot for the filtered data
#         fig, ax = plt.subplots(figsize=(8, 6))
#         ax.bar(result['employee_residence'], result['average_salary'], color='skyblue')
#         ax.set_xlabel('Employee Residence')
#         ax.set_ylabel('Average Salary')
#         ax.set_title('Average Salary by Employee Residence')

#         # Save the plot to a BytesIO object and encode it as base64
#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         img_b64 = base64.b64encode(img.read()).decode('utf-8')

#         # Return the image as a base64 string
#         return jsonify({'chart': img_b64})
    
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An error occurred while processing your request"}), 500


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


# from flask import Flask, request, jsonify
# import boto3
# import pandas as pd
# import io
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Allow cross-origin requests from React

# s3_client = boto3.client('s3')
# BUCKET_NAME = 'mrunalproj'

# # Helper to read CSV from S3 to DataFrame
# def read_csv_from_s3(key):
#     obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
#     return pd.read_csv(io.BytesIO(obj['Body'].read()))

# @app.route('/options')
# def get_filter_options():
#     df = read_csv_from_s3('jobs_in_data.csv')
#     return jsonify({
#         'job_title': sorted(df['job_title'].dropna().unique().tolist()),
#         'job_category': sorted(df['job_category'].dropna().unique().tolist()) if 'job_category' in df.columns else [],
#         'employee_residence': sorted(df['employee_residence'].dropna().unique().tolist()),
#         'experience_levels': sorted(df['experience_level'].dropna().unique().tolist()),
#         'work_setting': sorted(df['work_setting'].dropna().unique().tolist())
#     })

# @app.route('/data/<chart_type>')
# def get_chart_data(chart_type):
#     key_map = {
#         'avg_salary_by_title': 'output1/avg_salary_by_title/part-00000-*.csv',
#         'top10_jobs': 'output1/top10_highest_paying_jobs/part-00000-*.csv',
#         'top_by_experience': 'output1/top_by_experience_level/part-00000-*.csv',
#         'job_count_by_location': 'output1/job_postings_by_location/part-00000-*.csv',
#         'expected_salary_prediction': 'output1/expected_salary_prediction/part-00000-*.csv',
#         'salary_trends_over_time': 'output1/salary_trends_over_time/part-00000-*.csv',
#         'work_setting_distribution': 'output1/work_setting_distribution/part-00000-*.csv'
#     }
#     prefix = key_map.get(chart_type)
#     if not prefix:
#         return jsonify({'error': 'Invalid chart type'}), 400

#     paginator = s3_client.get_paginator('list_objects_v2')
#     pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix.split('/')[0] + '/')
#     for page in pages:
#         for obj in page.get('Contents', []):
#             if 'part-00000' in obj['Key']:
#                 df = read_csv_from_s3(obj['Key'])
#                 return df.to_json(orient='records')

#     return jsonify({'error': 'Data not found'}), 404

# @app.route('/predict', methods=['POST'])
# def predict_salary():
#     user_input = request.json
#     df = read_csv_from_s3('output1/expected_salary_prediction/part-00000-*.csv')

#     row = df[
#         (df['job_title'] == user_input['job_title']) &
#         (df['experience_level'] == user_input['experience_level']) &
#         (df['employee_residence'] == user_input['employee_residence']) &
#         (df['work_setting'] == user_input['work_setting'])
#     ]
#     if not row.empty:
#         return jsonify({'predicted_salary': row.iloc[0]['expected_salary']})
#     else:
#         return jsonify({'predicted_salary': 'No match found'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from React frontend

df = pd.read_csv("jobs_in_data.csv")

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = df['job_category'].dropna().unique().tolist()
    return jsonify(sorted(categories))

@app.route('/titles', methods=['GET'])
def get_titles():
    category = request.args.get('category')
    if not category:
        return jsonify([])

    filtered = df[df['job_category'] == category]
    titles = filtered['job_title'].dropna().unique().tolist()
    return jsonify(sorted(titles))

@app.route('/locations', methods=['GET'])
def get_locations():
    category = request.args.get('category')
    title = request.args.get('title')
    if not category or not title:
        return jsonify([])

    filtered = df[(df['job_category'] == category) & (df['job_title'] == title)]
    locations = filtered['employee_residence'].dropna().unique().tolist()
    return jsonify(sorted(locations))

@app.route('/average_salary', methods=['GET'])
def get_average_salary():
    category = request.args.get('category')
    title = request.args.get('title')
    location = request.args.get('location')
    if not all([category, title, location]):
        return jsonify({'average_salary': None})

    filtered = df[
        (df['job_category'] == category) &
        (df['job_title'] == title) &
        (df['employee_residence'] == location)
    ]
    if filtered.empty:
        return jsonify({'average_salary': None})

    avg_salary = filtered['salary_in_usd'].mean()
    return jsonify({'average_salary': round(avg_salary, 2)})


@app.route('/salary_by_experience', methods=['GET'])
def get_salary_by_experience():
    category = request.args.get('category')
    title = request.args.get('title')
    location = request.args.get('location')

    if not all([category, title, location]):
        return jsonify([])

    filtered = df[
        (df['job_category'] == category) &
        (df['job_title'] == title) &
        (df['employee_residence'] == location)
    ]

    if filtered.empty:
        return jsonify([])

    # Group by experience level and compute average salary
    grouped = (
        filtered.groupby('experience_level')['salary_in_usd']
        .mean()
        .reset_index()
        .sort_values('experience_level')
    )

    result = grouped.to_dict(orient='records')
    return jsonify(result)


#for right pay predictor
@app.route('/salary_check', methods=['GET'])
def check_salary_status():
    category = request.args.get('category')
    title = request.args.get('title')
    location = request.args.get('location')
    experience = request.args.get('experience')
    user_salary = float(request.args.get('user_salary', 0))

    if not all([category, title, location, experience]):
        return jsonify({'status': 'Invalid input'}), 400

    filtered = df[
        (df['job_category'] == category) &
        (df['job_title'] == title) &
        (df['employee_residence'] == location) &
        (df['experience_level'] == experience)
    ]

    if filtered.empty:
        return jsonify({'status': 'No data for selected filters'}), 404

    avg_salary = filtered['salary_in_usd'].mean()

    if user_salary < avg_salary - 5000:
        verdict = "You're underpaid compared to the market."
    elif user_salary > avg_salary + 5000:
        verdict = "You're overpaid compared to the market."
    else:
        verdict = "You're earning close to the market average."

    return jsonify({
        'average_salary': round(avg_salary, 2),
        'user_salary': user_salary,
        'verdict': verdict
    })


if __name__ == '__main__':
    app.run(debug=True)
