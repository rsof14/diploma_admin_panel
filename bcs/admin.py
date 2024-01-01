from django.contrib import admin
from .models import (
    Asset,
    Currency,
    Customer,
    Permissions,
    StrategyType,
    Roles,
    SystemObjects,
    ObjectsPermissions,
    RiskProfile,
    Strategy,
    User,
    Portfolio,
    PortfolioValues,
    PortfolioRisks,
    RiskMetrics,
    PortfolioStrategyHistory,
    SupportMessages
)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    pass


@admin.register(StrategyType)
class StrategyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass


class ObjectsPermissionsInline(admin.TabularInline):
    model = ObjectsPermissions


# @admin.register(ObjectsPermissions)
# class ObjectsPermissionsAdmin(admin.ModelAdmin):
#     pass


@admin.register(SystemObjects)
class SystemObjectsAdmin(admin.ModelAdmin):
    # pass
    inlines = (ObjectsPermissionsInline,)


@admin.register(RiskProfile)
class RiskProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(RiskMetrics)
class RiskMetricsAdmin(admin.ModelAdmin):
    pass


@admin.register(SupportMessages)
class SupportMessagesAdmin(admin.ModelAdmin):
    pass


class PortfolioValuesInline(admin.TabularInline):
    model = PortfolioValues


class PortfolioRisksInline(admin.TabularInline):
    model = PortfolioRisks


class PortfolioStrategyHistoryInline(admin.TabularInline):
    model = PortfolioStrategyHistory


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = (PortfolioValuesInline, PortfolioRisksInline, PortfolioStrategyHistoryInline,)
