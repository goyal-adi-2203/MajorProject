package com.example.dimdetect.models;

public class DistanceResponse {
    private Data data;

    public Data getData() {
        return data;
    }

    public static class Data {
        private String dis; // Keep it as String because the API returns it as a string

        public String getDis() {
            return dis;
        }

        public double getDisAsDouble() {
            try {
                return Double.parseDouble(dis); // Convert to double
            } catch (NumberFormatException e) {
                e.printStackTrace();
                return 0.0; // Default value in case of error
            }
        }
    }
}

