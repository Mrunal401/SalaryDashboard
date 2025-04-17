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

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)

spark = SparkSession.builder.appName("SalaryAnalysis") \
    .getOrCreate()
df = spark.read.csv("s3://mrunalproj/jobs_in_data.csv", header=True, inferSchema=True)

@app.route("/api/test")
def test():
    return jsonify(df.limit(5).toPandas().to_dict(orient="records"))

@app.route('/api/filters', methods=['GET'])
def get_filter_options():
    job_titles = [row[0] for row in df.select("job_title").distinct().collect()]
    job_categories = [row[0] for row in df.select("job_category").distinct().collect()]
    locations = [row[0] for row in df.select("employee_residence").distinct().collect()]
    return jsonify({
        "job_titles": job_titles,
        "job_categories": job_categories,
        "locations": locations
    })

@app.route('/api/salary-summary', methods=['POST'])
def salary_summary():
    try:
        data = request.get_json()
        job_title = data.get("job_title")
        job_category = data.get("job_category")
        location = data.get("location")

        filtered = df
        if job_title:
            filtered = filtered.filter(col("job_title") == job_title)
        if job_category:
            filtered = filtered.filter(col("job_category") == job_category)
        if location:
            filtered = filtered.filter(col("employee_residence") == location)

        result = (
            filtered.groupBy("employee_residence")
            .agg(avg("salary").alias("average_salary"))
            .orderBy("average_salary", ascending=False)
            .toPandas()
        )
        #return jsonify(result.to_dict(orient="records"))

        #return result.to_json(orient="records")

    
        # If the result is empty, return a response message
        if result.empty:
            return jsonify({"message": "No data found for the selected filters"}), 404

        # Create a plot for the filtered data
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(result['employee_residence'], result['average_salary'], color='skyblue')
        ax.set_xlabel('Employee Residence')
        ax.set_ylabel('Average Salary')
        ax.set_title('Average Salary by Employee Residence')

        # Save the plot to a BytesIO object and encode it as base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_b64 = base64.b64encode(img.read()).decode('utf-8')

        # Return the image as a base64 string
        return jsonify({'chart': img_b64})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred while processing your request"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
