from pyspark.sql import SparkSession
from pyspark.sql.functions import trim
from pyspark.ml.feature import StringIndexer, OneHotEncoder

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SalaryPredictor") \
    .getOrCreate()

# Load the dataset
data_path = "s3://mrunalproj/jobs_in_data.csv"
data = spark.read.csv(data_path, header=True, inferSchema=True)

# Show first 5 rows
data.show(5)



# Drop rows with nulls in selected columns
data_cleaned = data.select("job_title", "experience_level", "salary_in_usd", 
                           "salary_currency", "work_setting", "employee_residence") \
                   .dropna()

# Trim whitespace from string columns
data_cleaned = data_cleaned.withColumn("job_title", trim("job_title")) \
                           .withColumn("experience_level", trim("experience_level")) \
                           .withColumn("salary_currency", trim("salary_currency")) \
                           .withColumn("work_setting", trim("work_setting")) \
                           .withColumn("employee_residence", trim("employee_residence"))

# Show preview
data_cleaned.show(5)


# Initialize the StringIndexer for each categorical column (Do it one by one)
job_title_indexer = StringIndexer(inputCol="job_title", outputCol="job_title_index", handleInvalid="skip")
experience_level_indexer = StringIndexer(inputCol="experience_level", outputCol="experience_level_index", handleInvalid="skip")
salary_currency_indexer = StringIndexer(inputCol="salary_currency", outputCol="salary_currency_index", handleInvalid="skip")
work_setting_indexer = StringIndexer(inputCol="work_setting", outputCol="work_setting_index", handleInvalid="skip")
employee_residence_indexer = StringIndexer(inputCol="employee_residence", outputCol="employee_residence_index", handleInvalid="skip")

# Fit the StringIndexers on a small subset and broadcast the models for distributed processing
# This approach allows StringIndexer to work in a distributed environment

# Fit the indexers
job_title_indexer_model = job_title_indexer.fit(data_cleaned)
experience_level_indexer_model = experience_level_indexer.fit(data_cleaned)
salary_currency_indexer_model = salary_currency_indexer.fit(data_cleaned)
work_setting_indexer_model = work_setting_indexer.fit(data_cleaned)
employee_residence_indexer_model = employee_residence_indexer.fit(data_cleaned)

# Broadcast the models for distributed processing
job_title_indexer_model_broadcast = spark.sparkContext.broadcast(job_title_indexer_model)
experience_level_indexer_model_broadcast = spark.sparkContext.broadcast(experience_level_indexer_model)
salary_currency_indexer_model_broadcast = spark.sparkContext.broadcast(salary_currency_indexer_model)
work_setting_indexer_model_broadcast = spark.sparkContext.broadcast(work_setting_indexer_model)
employee_residence_indexer_model_broadcast = spark.sparkContext.broadcast(employee_residence_indexer_model)

# Now, transform the data using the broadcasted models
data_indexed = job_title_indexer_model_broadcast.value.transform(data_cleaned)
data_indexed = experience_level_indexer_model_broadcast.value.transform(data_indexed)
data_indexed = salary_currency_indexer_model_broadcast.value.transform(data_indexed)
data_indexed = work_setting_indexer_model_broadcast.value.transform(data_indexed)
data_indexed = employee_residence_indexer_model_broadcast.value.transform(data_indexed)

# Show the result after indexing
data_indexed.show(5)

# Now, let's apply OneHotEncoder for each indexed column
encoder_job_title = OneHotEncoder(inputCol="job_title_index", outputCol="job_title_ohe")
encoder_experience_level = OneHotEncoder(inputCol="experience_level_index", outputCol="experience_level_ohe")
encoder_salary_currency = OneHotEncoder(inputCol="salary_currency_index", outputCol="salary_currency_ohe")
encoder_work_setting = OneHotEncoder(inputCol="work_setting_index", outputCol="work_setting_ohe")
encoder_employee_residence = OneHotEncoder(inputCol="employee_residence_index", outputCol="employee_residence_ohe")

# Apply OneHotEncoder transformations
data_encoded = encoder_job_title.fit(data_indexed).transform(data_indexed)
data_encoded = encoder_experience_level.fit(data_encoded).transform(data_encoded)
data_encoded = encoder_salary_currency.fit(data_encoded).transform(data_encoded)
data_encoded = encoder_work_setting.fit(data_encoded).transform(data_encoded)
data_encoded = encoder_employee_residence.fit(data_encoded).transform(data_encoded)

# Show the result after OneHotEncoding
data_encoded.show(5)

# Save indexed data to S3
indexed_data_path = "s3://mrunalproj/output/step3_indexed_data"
data_indexed.write.format("csv") \
    .mode("overwrite") \
    .option("header", "true") \
    .save(indexed_data_path)

print(f"Indexed data written to: {indexed_data_path}")


# # Save cleaned dataset to S3
# cleaned_data_path = "s3://mrunalproj/output_trial/step2_cleaned_data"
# data_cleaned.write.format("csv") \
#     .mode("overwrite") \
#     .option("header", "true") \
#     .save(cleaned_data_path)

# print(f"Cleaned data written to: {cleaned_data_path}")


# # Save the dataset to a new folder in S3 (as CSV)
# output_path = "s3://mrunalproj/output_trial/step1_raw_data"

# data.write.format("csv") \
#     .mode("overwrite") \
#     .option("header", "true") \
#     .save(output_path)

# print(f"Raw data written to: {output_path}")
