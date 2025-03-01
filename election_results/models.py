from django.db import models

# Create your models here.

class State(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'states'

    def __str__(self):
        return self.state_name

class LGA(models.Model):
    lga_id = models.IntegerField(primary_key=True)
    lga_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    lga_description = models.TextField(null=True, blank=True)
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'lga'

    def __str__(self):
        return self.lga_name

class Ward(models.Model):
    ward_id = models.IntegerField(primary_key=True)
    ward_name = models.CharField(max_length=50)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)
    ward_description = models.TextField(null=True, blank=True)
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'ward'

    def __str__(self):
        return self.ward_name

class PollingUnit(models.Model):
    polling_unit_id = models.AutoField(primary_key=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)
    uniqueid = models.IntegerField(unique=True)
    polling_unit_number = models.CharField(max_length=50, null=True)
    polling_unit_name = models.CharField(max_length=50, null=True)
    polling_unit_description = models.TextField(null=True, blank=True)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True, db_column='long')
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'polling_unit'

    def __str__(self):
        return f"{self.polling_unit_name} - {self.polling_unit_number}"

class AnnouncedPuResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE, to_field='uniqueid', db_column='polling_unit_uniqueid')
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'announced_pu_results'

    def __str__(self):
        return f"{self.polling_unit} - {self.party_abbreviation}: {self.party_score}"

class AnnouncedLgaResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    lga_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'announced_lga_results'

    def __str__(self):
        return f"{self.lga_name} - {self.party_abbreviation}: {self.party_score}"
