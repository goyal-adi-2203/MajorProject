package com.example.dimdetect.services;

import com.example.dimdetect.models.DistanceResponse;

import retrofit2.Call;
import retrofit2.http.GET;

public interface DistanceService {
    @GET("api/dim/distance")
    Call<DistanceResponse> getDistance();
}
