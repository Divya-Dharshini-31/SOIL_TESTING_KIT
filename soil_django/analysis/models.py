# analysis/models.py

from django.db import models

class SoilAnalysis(models.Model):
    soil_type = models.CharField(max_length=255)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    soil_score = models.FloatField()
    
    def _str_(self):
        return f"Soil Analysis: {self.soil_type}"

class CropRecommendation(models.Model):
    soil_type = models.CharField(max_length=255)
    recommended_crop = models.CharField(max_length=255)
    
    def _str_(self):
        return f"Recommended Crop for {self.soil_type}"

class FertilizerRecommendation(models.Model):
    soil_type = models.CharField(max_length=255)
    recommended_fertilizer = models.CharField(max_length=255)
    
    def _str_(self):
        return f"Recommended Fertilizer for {self.soil_type}"