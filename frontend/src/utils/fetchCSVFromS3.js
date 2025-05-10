//import axios from 'axios';
import Papa from 'papaparse';
import { ACCESS_KEY_ID, ACCESS_SECRET_KEY } from './keys';
import AWS from 'aws-sdk';

AWS.config.update({
    accessKeyId: ACCESS_KEY_ID,
    secretAccessKey: ACCESS_SECRET_KEY,
  });
  
  const s3 = new AWS.S3();
  
  export const fetchCSVFromS3 = async (bucketName, fileKey) => {
    try {
      const params = {                                               
        Bucket: bucketName,
        Key: fileKey,
      };
      const response = await s3.getObject(params).promise();
      const parsedData = Papa.parse(response.Body.toString(), { header: true }).data;
      return parsedData;
    } catch (error) {
      console.error('Error fetching CSV from S3:', error);
      throw error;
    }
  };