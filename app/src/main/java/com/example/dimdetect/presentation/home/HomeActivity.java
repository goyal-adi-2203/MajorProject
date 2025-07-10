package com.example.dimdetect.presentation.home;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.graphics.Canvas;
import android.content.ContentValues;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import com.bumptech.glide.Glide;
import com.example.dimdetect.R;
import com.example.dimdetect.models.DistanceResponse;
import com.example.dimdetect.services.DistanceService;
import com.example.dimdetect.utils.ImageData;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;


public class HomeActivity extends AppCompatActivity {

//    private static final String BASE_URL = "https://dimdetect.onrender.com/";
    private static final String BASE_URL = "http://192.168.57.178:8747/";

    ImageView imageView;
    Button disBtn, calcBtn;
    Uri imageUri;
    String TAG = "HomeActBC";
    double imageX;
    double imageY;

    List<double[]> coordinateList;

    ImageData imageData;
    double distance;
    double pixelX, pixelY;

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        ImageView camerabtn = findViewById(R.id.cameraBtn);

        imageView = findViewById(R.id.cameraImg);
        disBtn = findViewById(R.id.getDisBtn);
        calcBtn = findViewById(R.id.calcBtn);

        imageData = new ImageData();
        coordinateList = new ArrayList<>();
        camerabtn.setOnClickListener(v -> {
            setImageUri();
            // Create the camera_intent ACTION_IMAGE_CAPTURE it will open the camera for capture the image
            Intent camera_intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            camera_intent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);
            // Start the activity with camera_intent, and request pic id
            startActivityForResult(camera_intent, 100);
        });

        imageView.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_UP) {
                    double[] coordinates = getImageCoordinates(imageView, event.getX(), event.getY());
                    if (coordinates != null) {
                         imageX = coordinates[0];
                         String xx = String.format("%.2f",imageX);
                        String yy = String.format("%.2f",imageY);
                         imageY = coordinates[1];
                         coordinateList.add(coordinates);
                        Log.d(TAG, "Pixel coordinates: (" + imageX + ", " + imageY + ")");

                        Toast.makeText(HomeActivity.this,"X Co-ordinate: "+ xx + ", Y Co-ordinate: " + yy, Toast.LENGTH_SHORT).show();
                    }
                }

                return true;
            }
        });

        disBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fetchDistance();
            }
        });

        calcBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                double calculatedDistance = calculateDistance(distance);
                String dist = String.format("%.2f", calculatedDistance);
                AlertDialog.Builder builder = new AlertDialog.Builder(HomeActivity.this);
                builder.setTitle("Actual Distance")               // Set the title of the dialog
                        .setMessage("Distance between the two points are: " + dist)           // Set the message to display
                        .setCancelable(false)          // Prevent dialog from being dismissed by clicking outside
                        .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();      // Dismiss the dialog when the button is clicked
                            }
                        });

                AlertDialog alert = builder.create(); // Create the AlertDialog
                alert.show();

            }
        });
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        // Match the request 'pic id with requestCode
        if (requestCode == 100) {
            // BitMap is data structure of image file which store the image in memory
//            Bitmap photo = (Bitmap) data.getExtras().get("data");

            Log.d(TAG, "onActivityResult: " + imageUri);

            try {
                imageData.getImageData(getContentResolver().openInputStream(imageUri));

            } catch (IOException e) {
                Log.e(TAG, "onActivityResult: this is exception");
                e.printStackTrace();
            }

            // Set the image in imageview for display
            Glide.with(this)
                    .load(imageUri)
                    .into(imageView);
        }
    }


    // Function to get the actual pixel coordinates in the image
    private double[] getImageCoordinates(ImageView imageView, float touchX, float touchY) {

        // Get the dimensions of the ImageView
        int viewWidth = imageView.getWidth();
        int viewHeight = imageView.getHeight();

        // Get the original dimensions of the bitmap
        Drawable drawable = imageView.getDrawable();
        if (drawable == null) {
            return null;
        }

        Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();
        float bitmapWidth = bitmap.getWidth();
        float bitmapHeight = bitmap.getHeight();

//        Log.d(TAG, "getImageCoordinates: " + bitmapWidth + " " + bitmapHeight);

        // Get the scale type and the scaling factors
        Matrix matrix = new Matrix();
        imageView.getImageMatrix().invert(matrix);
        float[] touchPoint = new float[]{touchX, touchY};
        matrix.mapPoints(touchPoint);

        // Clamp the coordinates to the original image size
        double originalX = Math.max(0, Math.min(touchPoint[0], bitmapWidth - 1));
        double originalY = Math.max(0, Math.min(touchPoint[1], bitmapHeight - 1));

//        Log.d("ImageCoordinates", "Original Coordinates: (" + originalX + ", " + originalY + ")");
        // Draw a circle at the touched position
        drawCircleOnImage(imageView, originalX, originalY);

        double[] coordinates = imageData.getPixelCoordinates(originalX, originalY, bitmapWidth, bitmapHeight);
        return coordinates;
    }

    // Function to draw a circle on the image
    private void drawCircleOnImage(ImageView imageView, double imageX, double imageY) {
        Bitmap originalBitmap = ((BitmapDrawable) imageView.getDrawable()).getBitmap();
        Bitmap mutableBitmap = originalBitmap.copy(Bitmap.Config.ARGB_8888, true);

        Canvas canvas = new Canvas(mutableBitmap);
        Paint paint = new Paint();
        paint.setColor(Color.RED);
        paint.setStyle(Paint.Style.FILL);

        // Draw a circle at the specified pixel coordinates
        canvas.drawCircle((float) imageX,(float) imageY, 10, paint); // Adjust radius (10) as needed

        // Set the updated bitmap to the ImageView
        imageView.setImageBitmap(mutableBitmap);
    }

    private void setImageUri(){
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.DISPLAY_NAME, "MyImage_" + System.currentTimeMillis() + ".jpg"); // Image file name
        values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
        values.put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/MyAppImages");  // Save to Pictures/MyAppImages

        // Insert the image into MediaStore and get the URI to save the image to
        imageUri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
    }

    private void fetchDistance(){
        Log.d(TAG, "fetchDistance: I am here");
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        DistanceService service = retrofit.create(DistanceService.class);

        Call<DistanceResponse> call = service.getDistance();
        call.enqueue(new Callback<DistanceResponse>() {
            @Override
            public void onResponse(Call<DistanceResponse> call, Response<DistanceResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    distance = response.body().getData().getDisAsDouble();

                    Log.d(TAG, "Distance: " + distance);
                    String dist = String.format("%.2f",distance);
                    Toast.makeText(HomeActivity.this, "" +  dist, Toast.LENGTH_SHORT).show();
                } else {
                    Log.e(TAG, "Failed to get a valid response");
                    Toast.makeText(HomeActivity.this, "Try again!", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<DistanceResponse> call, Throwable t) {
                Log.e(TAG, "Error: " + t.getMessage());
            }
        });
    }

    private double calculateDistance(double distance){
        int n= coordinateList.size();
        double x1 = coordinateList.get(n-1)[0];
        double y1 = coordinateList.get(n-1)[1];
        double x2 = coordinateList.get(n-2)[0];
        double y2 = coordinateList.get(n-2)[1];
        double obj_length_pixels = Math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
        double obj_length_on_sensor_mms = (imageData.sensorHeight*obj_length_pixels)/imageData.imgLen;
        double obj_length_meters = ( (distance * obj_length_on_sensor_mms )/imageData.focalLength);

        Log.d(TAG, "ERROR " + obj_length_meters+"");

        return obj_length_meters;

    }
}

//tag:ImgData tag:ImageViewClick tag:HomeActBC tag:ImageCoordinates
