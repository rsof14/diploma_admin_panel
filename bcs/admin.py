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
    search_fields = ['ISIN', 'ticker', 'name']
    list_filter = ['sector']
    list_display = ['ticker', 'name']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['currency', 'description']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['branch']
    ordering = ['name']
    list_display = ['name', 'branch']


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
    inlines = (ObjectsPermissionsInline,)


@admin.register(RiskProfile)
class RiskProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_var']


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency', 'type', 'risk_profile', 'valid']
    search_fields = ['name', 'description']
    list_filter = ['currency', 'type', 'risk_profile', 'valid']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'login', 'role_id']
    search_fields = ['name', 'login']
    list_filter = ['role_id', 'is_superuser']


@admin.register(RiskMetrics)
class RiskMetricsAdmin(admin.ModelAdmin):
    pass


@admin.register(SupportMessages)
class SupportMessagesAdmin(admin.ModelAdmin):
    search_fields = ['message', 'answer']
    list_filter = ['done', 'msg_date']
    sortable_by = ['msg_date']
    list_display = ['msg_date', 'done', 'user_id']


class PortfolioValuesInline(admin.TabularInline):
    model = PortfolioValues


class PortfolioRisksInline(admin.TabularInline):
    model = PortfolioRisks


class PortfolioStrategyHistoryInline(admin.TabularInline):
    model = PortfolioStrategyHistory


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = (PortfolioValuesInline, PortfolioRisksInline, PortfolioStrategyHistoryInline,)
    list_display = ['account', 'customer_id', 'asset_manager', 'strategy_id', 'updated']
    search_fields = ['account']
    list_filter = ['creation_date', 'updated', 'asset_manager', 'strategy_id']
