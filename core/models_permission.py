from django.db import models

class DashboardPermission(models.Model):
    class Meta:
        verbose_name = "Dashboard Permission"
        verbose_name_plural = "Dashboard Permissions"
        permissions = [
            ("view_dashboard", "Pode ver o Dashboard"),
        ]
