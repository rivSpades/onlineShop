from django.db import models,transaction
from store.models import Product,Variation
from accounts.models import Account
import datetime

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class PaymentPurchase(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Purchase(models.Model):
    STATUS = (("New", "New"), ("Completed", "Completed"), ("Cancelled", "Cancelled"))
    stock_updated = models.BooleanField(default=False, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(PaymentPurchase, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_number = models.CharField(max_length=20, blank=True, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    extra_costs = models.FloatField(default=0.0)  # Extra costs (like shipping, taxes, etc.)
    total_amount = models.FloatField(default=0.0, editable=False)  # Total amount (calculated dynamically)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _generate_purchase_number(self):
        """Generate a unique purchase number based on the current date and ID."""
        yr = int(datetime.date.today().strftime('%Y'))
        mt = int(datetime.date.today().strftime('%m'))
        dt = int(datetime.date.today().strftime('%d'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        return current_date + str(self.id)

    def save(self, *args, update_stock=True, **kwargs):
        """Override save to manage stock updates based on status changes."""
        # Detect status change
        if self.pk:
            previous_status = Purchase.objects.get(pk=self.pk).status
        else:
            previous_status = None

        # Generate purchase number for new records
        if not self.purchase_number:
            super().save(*args, **kwargs)  # Save to get the ID first
            self.purchase_number = self._generate_purchase_number()
            super().save(*args, **kwargs)  # Save again to update the purchase_number

        # Update the total amount based on purchase products
        self.update_total_amount()

        # Handle stock updates
        if update_stock:
            if self.status == "Completed" and not self.stock_updated:
                # Status changed to "Completed" and stock hasn't been updated yet
                self.update_product_stock(increase=True)
                self.stock_updated = True
            elif self.status != "Completed" and self.stock_updated:
                # Status changed from "Completed" to another status, reduce the stock
                self.update_product_stock(increase=False)
                self.stock_updated = False

        super().save(*args, **kwargs)  # Save final changes

    def update_product_stock(self, increase):
        """Update stock of variations based on purchase completion or reversion."""
        for purchase_product in self.purchaseproduct_set.all():
            for variation in purchase_product.variation.all():
                # Adjust the stock of the variation directly
                if variation:
                    adjustment = purchase_product.quantity
                    if increase:
                        variation.quantity += adjustment  # Increase stock
                    else:
                        variation.quantity -= adjustment  # Decrease stock

                    variation.save()  # Save the variation after stock adjustment
                else:
                    print(f"Stock entry not found for variation: {variation}")

    def update_total_amount(self):
        """Recalculate the total amount based on purchase products and extra costs."""
        self.total_amount = sum(
            purchase_product.product_price * purchase_product.quantity
            for purchase_product in self.purchaseproduct_set.all()
        ) + self.extra_costs

    def __str__(self):
        return self.purchase_number

    @property
    def calculated_total_amount(self):
        """Dynamic total amount calculation."""
        return sum(purchase_product.product_price * purchase_product.quantity for purchase_product in self.purchaseproduct_set.all()) + self.extra_costs


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.purchase.purchase_number}"

    def save(self, *args, **kwargs):
        """Override save to ensure stock availability and update purchase total amount."""
        if self.purchase.status == "Completed":
            raise ValueError("Cannot modify purchase products for completed purchases. Change the state first and save.")
        


        if not self.pk:
            super().save(*args, **kwargs)  # Save the instance to generate an ID

            
        # Ensure sufficient stock in variations
        for variation in self.variation.all():
            if variation.quantity < self.quantity:
                raise ValueError(f"Insufficient stock for variation: {variation}")

        super().save(*args, **kwargs)

        # After saving, update the total amount of the associated Purchase
        self.purchase.update_total_amount()
        self.purchase.save(update_stock=False)

    def delete(self, *args, **kwargs):
        """Prevent deletion if purchase is completed, and handle stock rollback."""
        if self.purchase.status == "Completed":
            raise ValueError("Cannot delete purchase products for completed purchases. Change the state first and save.")

        super().delete(*args, **kwargs)

        # Update total amount after deletion
        self.purchase.update_total_amount()
        self.purchase.save(update_stock=False)
