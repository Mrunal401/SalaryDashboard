from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
import pyspark.sql.functions as F
from pyspark.sql.functions import trim
from pyspark.ml import PipelineModel

# Initialize Spark session
spark = SparkSession.builder.appName("SalaryPrediction").getOrCreate()

# Load the dataset from local file (ensure to use the correct path)
data_path = "s3://mrunalproj/jobs_in_data.csv"  # Update this with your local dataset path
data = spark.read.csv(data_path, header=True, inferSchema=True)

# Show the first few rows of the dataset to check the columns
data.show(5)

# Select relevant columns and drop any rows with null values
data = data.select("job_title", "experience_level", "salary_in_usd", "salary_currency", "work_setting", "employee_residence")
data = data.dropna()


# Strip whitespace from strings
data = data.withColumn("employee_residence", trim("employee_residence"))
data = data.withColumn("job_title", trim("job_title"))
data = data.withColumn("experience_level", trim("experience_level"))
# Do the same for any other string columns


# Apply StringIndexer to categorical columns with handleInvalid='skip'
job_title_indexer = StringIndexer(inputCol="job_title", outputCol="job_title_index", handleInvalid="keep")
experience_level_indexer = StringIndexer(inputCol="experience_level", outputCol="experience_level_index", handleInvalid="keep")
salary_currency_indexer = StringIndexer(inputCol="salary_currency", outputCol="salary_currency_index", handleInvalid="keep")
work_setting_indexer = StringIndexer(inputCol="work_setting", outputCol="work_setting_index", handleInvalid="keep")
employee_residence_indexer = StringIndexer(inputCol="employee_residence", outputCol="employee_residence_index", handleInvalid="keep")

# Assemble features into a single vector column
assembler = VectorAssembler(
    inputCols=["job_title_index", "experience_level_index", "salary_currency_index", "work_setting_index", "employee_residence_index"],
    outputCol="features"
)

# Set up the regression model (Random Forest)
rf = RandomForestRegressor(featuresCol="features", labelCol="salary_in_usd",  numTrees=20, maxBins=200)

# Create a pipeline to train the model
pipeline = Pipeline(stages=[job_title_indexer, experience_level_indexer, salary_currency_indexer, work_setting_indexer, employee_residence_indexer, assembler, rf])

# Fit and transform the data
pipeline_model = pipeline.fit(data)
assembled_data = pipeline_model.transform(data)

# Now show the output
assembled_data.select("features").show(5, truncate=False)

# Split the data into train and test sets (70% training, 30% testing)
train_data, test_data = data.randomSplit([0.7, 0.3], seed=42)
train_data = train_data.cache()
test_data = test_data.cache()

train_data.show()
test_data.show()

# Train the model
model = pipeline.fit(train_data)

# Make predictions
predictions = model.transform(test_data)

# Show predictions and actual salaries
predictions.select("salary_in_usd", "prediction").show()

# Evaluate the model: RMSE and R² metrics
evaluator_rmse = RegressionEvaluator(labelCol="salary_in_usd", predictionCol="prediction", metricName="rmse")
rmse = evaluator_rmse.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Evaluate the model using R²
evaluator_r2 = RegressionEvaluator(labelCol="salary_in_usd", predictionCol="prediction", metricName="r2")
r2 = evaluator_r2.evaluate(predictions)
print(f"R-squared (R²): {r2}")

# Display predictions
print("Predictions:")
predictions.select("salary_in_usd", "prediction").show()

# Define output paths (local paths can be used or change to S3 paths)
PREDICTIONS_PATH = "backend/output/predictions1"
MODEL_OUTPUT_PATH = "backend/output/saved_model"
TRAIN_DATA_PATH = "backend/output2/train_data"
TEST_DATA_PATH = "backend/output/test_data"

# Save the predictions to a CSV file (optional)
# predictions.write.format("csv").mode("overwrite").option("header", "true").save("C:/Users/Mrunal Manoj Patil/salary-dashboard/backend/predictions")

# Select only the necessary columns
predictions.select("salary_in_usd", "prediction") \
    .coalesce(1) \
    .write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", "true") \
    .save(PREDICTIONS_PATH)

# Save the trained model to a folder
#model_output_path = "C:/Users/Mrunal Manoj Patil/salary-dashboard/backend/predictions1"
#model_output_path = "C:/temp/salary_dashboard_model"
#model_output_path = "file:///C:/Users/Mrunal Manoj Patil/salary-dashboard/backend/predictions1"
model.write().overwrite().save(MODEL_OUTPUT_PATH)
print(f"Model saved to {MODEL_OUTPUT_PATH}")


# Save training and test data to separate folders
train_data.write.format("csv").mode("overwrite").option("header", "true").save(TRAIN_DATA_PATH)
test_data.write.format("csv").mode("overwrite").option("header", "true").save(TEST_DATA_PATH)
