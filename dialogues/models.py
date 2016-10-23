from django.core.validators import RegexValidator
from django.db import models

class Campaign(models.Model):
    DAIMOKU = 'DA'
    HOME_VISIT = 'HV'
    DIALOGUE = 'DL'
    CAMPAIGN_CHOICES = (
        (DAIMOKU, 'Daimoku'),
        (HOME_VISIT, 'Home Visit'),
        (DIALOGUE, 'Dialogue'),
        )

    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=60)
    campaign_type = models.CharField(
            max_length=2,
            choices=CAMPAIGN_CHOICES,
            default=DAIMOKU,
            )
    start_date = models.DateField()
    end_date = models.DateField()
    target_value = models.PositiveIntegerField()
    target_unit = models.CharField(max_length=10)
    
    def __str__(self):
        return "Campaign: %s Type %s"%(self.name, self.campaign_type)

class Daimoku(models.Model):
    member_name = models.CharField(max_length=60)
    member_email = models.CharField(max_length=60)
    campaign = models.ForeignKey(Campaign)
    duration_minutes = models.PositiveIntegerField()
    daimoku_date = models.DateField()

    def __str__(self):
        return "Daimoku in %s campaign,date %s duration %d minutes "%(self.campaign.name,
                str(self.daimoku_date), self.duration_minutes)

class DaimokuCommitment(models.Model):
    member_name = models.CharField(max_length=60)
    member_email = models.CharField(max_length=60)
    campaign = models.ForeignKey(Campaign)
    duration_minutes = models.PositiveIntegerField()
    committed_on_date = models.DateField()

    def __str__(self):
        return "Daimoku committed in %s campaign, on date %s duration %d minutes "%(self.campaign.name,
                str(self.committed_on_date), self.duration_minutes)

class Dialogue(models.Model):
    member_name = models.CharField(max_length=60)
    friend_name = models.CharField(max_length=60)
    member_email = models.CharField(max_length=60)
    campaign = models.ForeignKey(Campaign)
    dialogue_date = models.DateField()

    def __str__(self):
        return "Diag in %s campaign: %s spoke to %s "%(self.campaign.name,
                self.member_name, self.friend_name)

class HomeVisit(models.Model):
    visitor_name = models.CharField(max_length=30)
    visited_name = models.CharField(max_length=30)
    visitor_email = models.CharField(max_length=30)
    campaign = models.ForeignKey(Campaign)
    visit_date= models.DateField()

    def __str__(self):
        return "Home Visit in %s campaign : %s visited %s "%(self.campaign.name,
                self.visitor_name, self.visited_name)

