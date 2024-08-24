from django.db import models


class suit_details(models.Model):
    suit_id = models.AutoField(primary_key=True)
    fabric  = models.ForeignKey('fabric', on_delete=models.CASCADE)
    front_type = models.ForeignKey('front_type', on_delete=models.CASCADE)
    collar_type = models.ForeignKey('collar_type', on_delete=models.CASCADE)
    sleeves_type = models.ForeignKey('sleeves_type', on_delete=models.CASCADE)
    pockets_type = models.ForeignKey('pockets_type', on_delete=models.CASCADE)
    mobile_pocket = models.ForeignKey('mobile_pocket', on_delete=models.CASCADE)
    instructions = models.ForeignKey('instruction', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    

    def __str__(self):
        return self.suit_name
    
    
class fabric(models.Model):
    fabric_color = models.CharField(max_length=50)
    fabric_code = models.AutoField(primary_key=True)
    fabric_partner = models.CharField(max_length=50)
    fabric_origin = models.CharField(max_length=50)
    fabric_kandora = models.CharField(max_length=50)
    fabric_price = models.DecimalField(max_digits=10, decimal_places=2, default=10)

class front_type(models.Model):
    front_type_id = models.AutoField(primary_key=True)
    front_type_name = models.CharField(max_length=50)
    front_type_price = models.DecimalField(max_digits=10, decimal_places=2 , default=10)
    
class collar_type(models.Model):
    collar_type_id = models.AutoField(primary_key=True)
    collar_type_name = models.CharField(max_length=50)
    collar_type_price = models.DecimalField(max_digits=10, decimal_places=2 , default=10)


class sleeves_type(models.Model):
    sleeves_type_id = models.AutoField(primary_key=True)
    sleeves_type_name = models.CharField(max_length=50)
    sleeves_type_price = models.DecimalField(max_digits=10, decimal_places=2 , default=10)
    
class pockets_type(models.Model):
    pockets_type_id = models.AutoField(primary_key=True)
    pockets_type_name = models.CharField(max_length=50)
    pockets_type_price = models.DecimalField(max_digits=10, decimal_places=2 , default=10)

class mobile_pocket(models.Model):
    mobile_pocket_id = models.AutoField(primary_key=True)
    mobile_pocket_name = models.CharField(max_length=50)
    mobile_pocket_type = models.ForeignKey('mobile_pocket_type', on_delete=models.CASCADE)

class mobile_pocket_type(models.Model):
    mobile_pocket_type_id = models.AutoField(primary_key=True)
    mobile_pocket_type_name = models.CharField(max_length=50)
    if mobile_pocket_type_name == 'pen':
        pocket_type_required  = models.BooleanField(default=True)
    elif mobile_pocket_type_name == 'mobile':
        number_of_pockets = models.IntegerField(default=0)
    mobile_pocket_type_price = models.DecimalField(max_digits=10, decimal_places=2 , default=10)
    
    
class instruction(models.Model):
    instruction_id = models.AutoField(primary_key=True)
    instructions_text = models.TextField(default='')

        
        
    
    
