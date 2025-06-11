from django.db import models


class Customers(models.Model):
    customerID = models.CharField(max_length=5, unique=True, primary_key=True)
    companyName = models.CharField(max_length=200)
    contactName = models.CharField(max_length=150)
    contactTitle = models.CharField(max_length=150)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)


class Categories(models.Model):
    categoryID = models.PositiveIntegerField(primary_key=True, unique=True)
    categoryName = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    picture = models.BinaryField(null=True, blank=True)  


class Employees(models.Model):
    class TitleOfCourtesy(models.TextChoices):  
        MR = 'Mr.', 'Mr.'
        MRS = 'Mrs.', 'Mrs.'
        MS = 'Ms.', 'Ms.'
        DR = 'Dr.', 'Dr.'

    employeeID = models.PositiveIntegerField(primary_key=True, unique=True)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    titleOfCourtesy = models.CharField(max_length=10, choices=TitleOfCourtesy.choices)
    birthDate = models.DateTimeField()
    hireDate = models.DateTimeField()
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    homePhone = models.CharField(max_length=20, null=True, blank=True)
    extension = models.CharField(max_length=20, null=True, blank=True)
    photo = models.BinaryField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    reportsTo = models.PositiveIntegerField(null=True, blank=True)
    photoPath = models.URLField()


class EmployeeTerritories(models.Model):
    employeeID = models.ForeignKey('Employees', on_delete=models.PROTECT)
    territoryID = models.ForeignKey('Territories', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('employeeID', 'territoryID')  


class OrderDetails(models.Model):
    orderID = models.ForeignKey('Orders', on_delete=models.PROTECT)
    productID = models.ForeignKey('Products', on_delete=models.PROTECT)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    discount = models.FloatField(default=0)

    class Meta:
        unique_together = ('orderID', 'productID')  


class Orders(models.Model):
    orderID = models.PositiveIntegerField(primary_key=True, unique=True)
    customerID = models.ForeignKey('Customers', on_delete=models.PROTECT)
    employeeID = models.ForeignKey('Employees', on_delete=models.PROTECT)
    orderDate = models.DateTimeField()
    requiredDate = models.DateTimeField()
    shippedDate = models.DateTimeField()
    shipVia = models.ForeignKey('Shippers', on_delete=models.PROTECT)
    freight = models.FloatField()
    shipName = models.CharField(max_length=100)
    shipAddress = models.CharField(max_length=255)
    shipCity = models.CharField(max_length=100, null=True, blank=True)
    shipRegion = models.CharField(max_length=100, blank=True, null=True)
    shipPostalCode = models.CharField(max_length=20, null=True, blank=True)
    shipCountry = models.CharField(max_length=100, null=True, blank=True)


class Products(models.Model):
    productID = models.PositiveIntegerField(primary_key=True, unique=True)
    productName = models.CharField(max_length=200)
    supplierID = models.ForeignKey('Suppliers', on_delete=models.PROTECT)
    categoryID = models.ForeignKey('Categories', on_delete=models.PROTECT)
    quantityPerUnit = models.CharField(max_length=100)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    unitsInStock = models.PositiveIntegerField(default=0)
    unitsOnOrder = models.PositiveIntegerField(default=0)
    reorderLevel = models.PositiveIntegerField(default=0)
    discontinued = models.PositiveIntegerField(default=0)


class Regions(models.Model):
    class RegionChoices(models.TextChoices):  
        EASTERN = 'Eastern', 'Eastern'
        WESTERN = 'Western', 'Western'
        NORTHERN = 'Northern', 'Northern'
        SOUTHERN = 'Southern', 'Southern'

    regionID = models.PositiveIntegerField(primary_key=True, unique=True)
    regionDescription = models.CharField(max_length=50, choices=RegionChoices.choices)


class Shippers(models.Model):
    shipperID = models.PositiveIntegerField(primary_key=True, unique=True)
    companyName = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)


class Suppliers(models.Model):
    supplierID = models.PositiveIntegerField(primary_key=True, unique=True)
    companyName = models.CharField(max_length=100)
    contactName = models.CharField(max_length=100)
    contactTitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    homePage = models.CharField(max_length=200, null=True, blank=True)


class Territories(models.Model):
    territoryID = models.PositiveIntegerField(primary_key=True, unique=True)
    territoryDescription = models.TextField()
    regionID = models.ForeignKey('Regions', on_delete=models.PROTECT)