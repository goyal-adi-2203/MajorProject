package com.example.dimdetect.utils;

import android.media.ExifInterface;
import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.security.spec.ECField;
import java.util.Objects;

public class ImageData {

    String TAG = "ImgData";
    String phoneArjun = "EB2101";
    String phoneBajpai = "OnePlus Nord 2T 5G";
    public double sensorHeight;
    public double sensorWidth;
    public double focalLength;
    public double imgWid;
    public double imgLen;

    public void getImageData(InputStream inputStream) throws IOException {
        ExifInterface exifInterface = new ExifInterface(inputStream);

        String dateTime = exifInterface.getAttribute(ExifInterface.TAG_DATETIME);
        String focalLen = exifInterface.getAttribute(ExifInterface.TAG_FOCAL_LENGTH);
        String imgWidth = exifInterface.getAttribute(ExifInterface.TAG_IMAGE_WIDTH);
        String imgLen = exifInterface.getAttribute(ExifInterface.TAG_IMAGE_LENGTH);
        String phoneName = exifInterface.getAttribute(ExifInterface.TAG_MODEL);

        String[] split = focalLen.split("/");
        focalLength = 0;
        if(split.length == 2) {
            focalLength = Double.parseDouble(split[0]) / Double.parseDouble(split[1]);
        }

        double imageWidth = Double.parseDouble(imgWidth), imageHeight = Double.parseDouble(imgLen);

        // Log the EXIF data
        Log.d(TAG, "Date and Time: " + dateTime);
        Log.d(TAG, "Focal Length: " + focalLength + "mm");
        Log.d(TAG, "Image Width: " + imageWidth);
        Log.d(TAG, "Image Length: " + imageHeight);
        Log.d(TAG, "Model: " + phoneName);

        this.imgLen = imageHeight;
        this.imgWid = imageWidth;

        if(Objects.equals(phoneName, phoneArjun)){
            Log.d(TAG, "getImageData: arjun phone");
            sensorHeight = 6.26; //mm
            sensorWidth = 4.26; //mm
        } else if(Objects.equals(phoneName, phoneBajpai)){
            Log.d(TAG, "getImageData: bajpai phone");
            sensorHeight = 8.08; //mm
            sensorWidth = 6.06; //mm
        } else {
            Log.d(TAG, "getImageData: phone achha lao");
            sensorHeight = 8.08; //mm
            sensorWidth = 6.06; //mm
        }
    }

    public double[] getPixelCoordinates(double imageX, double imageY, double bitmapWidth,double bitmapHeight){
        double pixelX = imageX * imgWid / bitmapWidth;
        double pixelY = imageY * imgLen / bitmapHeight;
        return new double[]{pixelX, pixelY};
    }
}
