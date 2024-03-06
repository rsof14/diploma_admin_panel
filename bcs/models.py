from django.db import models
from django.core.exceptions import ValidationError
import uuid
from .password_generation import  form_user_password


class Asset(models.Model):
    ISIN = models.CharField(primary_key=True, max_length=12)
    ticker = models.CharField(max_length=10)
    name = models.CharField(verbose_name='Наименование компании', max_length=50)
    sector = models.CharField(verbose_name='Сектор компании', blank=True, max_length=50)

    class Meta:
        db_table = "public\".\"asset"
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'

    def __str__(self):
        return self.ticker


class Currency(models.Model):
    currency = models.CharField(primary_key=True, max_length=3, verbose_name='Валюта')
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        db_table = "public\".\"currency"
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.currency


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='ФИО', max_length=200)
    branch = models.CharField(verbose_name='Город', max_length=50)

    class Meta:
        db_table = "public\".\"customer"
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Permissions(models.Model):
    permission = models.CharField(primary_key=True, verbose_name='Право', max_length=10)

    class Meta:
        db_table = "public\".\"permissions"
        verbose_name = 'Право'
        verbose_name_plural = 'Права'

    def __str__(self):
        return self.permission


class StrategyType(models.Model):
    type = models.CharField(primary_key=True, verbose_name='Тип стратегии', max_length=200)

    class Meta:
        db_table = "public\".\"strategy_type"
        verbose_name = 'Тип стратегии'
        verbose_name_plural = 'Типы стратегий'

    def __str__(self):
        return self.type


class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Наименование', unique=True, max_length=200)

    class Meta:
        db_table = "public\".\"roles"
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class SystemObjects(models.Model):
    object_name = models.CharField(primary_key=True, verbose_name='Наименование объекта', max_length=80)
    ru_name = models.CharField(verbose_name='Наименование на русском', max_length=80)

    class Meta:
        db_table = "public\".\"system_objects"
        verbose_name = 'Объект в системе'
        verbose_name_plural = 'Объекты в системе'

    def __str__(self):
        return self.object_name


class ObjectsPermissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object = models.ForeignKey('SystemObjects', db_column='object', on_delete=models.CASCADE, verbose_name='Объект')
    role_id = models.ForeignKey('Roles', db_column='role_id', on_delete=models.CASCADE, verbose_name='Роль')
    permission = models.ForeignKey('Permissions', db_column='permission', on_delete=models.CASCADE,
                                   verbose_name='Разрешение')
    strategy_type = models.ForeignKey('StrategyType', db_column='strategy_type', on_delete=models.CASCADE,
                                      verbose_name='Тип стратегии (только для объекта Стратегия)', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['object', 'role_id', 'strategy_type'], name='object_role_primary_key')
        ]
        db_table = "public\".\"objects_permissions"
        verbose_name = 'Право роли над объектом'
        verbose_name_plural = 'Права роли над объектом'

    def clean(self):
        if self.object.object_name == "Strategy" and self.strategy_type.type == 'NULL':
            raise ValidationError("For object Strategy choose type")
        if self.object.object_name != "Strategy" and self.strategy_type.type != 'NULL':
            raise ValidationError("For this object choose 'NULL' in field strategy type")


class RiskProfile(models.Model):
    name = models.CharField(primary_key=True, verbose_name='Наименование', max_length=200)
    max_var = models.FloatField(verbose_name='Максимально допустимое значение VaR')

    class Meta:
        db_table = "public\".\"risk_profile"
        verbose_name = 'Риск-профиль'
        verbose_name_plural = 'Риск-профили'

    def __str__(self):
        return self.name


class Strategy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Наименование', max_length=200)
    currency = models.ForeignKey('Currency', db_column='currency', on_delete=models.DO_NOTHING, verbose_name='Валюта')
    description = models.TextField(verbose_name='Описание', blank=True)
    type = models.ForeignKey('StrategyType', db_column='type', on_delete=models.DO_NOTHING,
                             verbose_name='Тип стратегии')
    risk_profile = models.ForeignKey('RiskProfile', db_column='risk_profile', on_delete=models.DO_NOTHING,
                                     verbose_name='Риск-профиль')
    structure = models.TextField(verbose_name='Состав')
    valid = models.BooleanField(verbose_name='Действующая', default=True)
    management_fee = models.FloatField(verbose_name='Комиссия за управление', blank=True)
    success_fee = models.FloatField(verbose_name='Комиссия за успех', blank=True)
    benchmark = models.TextField(verbose_name='Бенчмарк', blank=True)

    class Meta:
        db_table = "public\".\"strategy"
        verbose_name = 'Стратегия'
        verbose_name_plural = 'Стратегии'

    def __str__(self):
        return self.name


def validate_login(value):
    if value[len(value) - 6:] == "bcs.ru":
        return value
    else:
        raise ValidationError("This field accepts mail ends with bcs.ru")


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(verbose_name='Логин', max_length=200, validators=[validate_login])
    name = models.CharField(verbose_name='ФИО', max_length=200)
    password = models.TextField(verbose_name='Пароль', blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления в систему')
    is_superuser = models.BooleanField(verbose_name='Суперпользователь', default=False)
    role_id = models.ForeignKey('Roles', db_column='role_id', on_delete=models.DO_NOTHING, verbose_name='Роль')

    class Meta:
        db_table = "public\".\"user"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.password == '':
            self.password = form_user_password(str(self.login))
        super(User, self).save(*args, **kwargs)


class Portfolio(models.Model):
    account = models.CharField(primary_key=True, max_length=8, verbose_name='Номер счета')
    customer_id = models.ForeignKey('Customer', db_column='customer_id', on_delete=models.CASCADE,
                                    verbose_name='Клиент')
    strategy_id = models.ForeignKey('Strategy', db_column='strategy_id', on_delete=models.DO_NOTHING,
                                    verbose_name='Стратегия', blank=True)
    structure = models.TextField(verbose_name='Состав', blank=True, default='{}')
    asset_manager = models.ForeignKey('User', db_column='asset_manager', on_delete=models.DO_NOTHING,
                                      verbose_name='Управляющий', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.BooleanField(verbose_name='Обновлено', default=False)

    class Meta:
        db_table = "public\".\"portfolio"
        verbose_name = 'Портфель'
        verbose_name_plural = 'Портфели'

    def __str__(self):
        return self.account

    def clean(self):
        if self.asset_manager.role_id.name != "Управляющий":
            raise ValidationError("Choose user with correct role as asset manager")


class PortfolioValues(models.Model):
    account = models.ForeignKey('Portfolio', primary_key=True, db_column='account', on_delete=models.CASCADE,
                                verbose_name='Портфель')
    date = models.DateField(verbose_name='Дата')
    value = models.FloatField(verbose_name='Стоимость')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'date_'], name='account_date_value_primary_key')
        ]
        db_table = "public\".\"portfolio_values"
        verbose_name = 'Стоимость портфеля'
        verbose_name_plural = 'Стоимости портфелей'

    def __str__(self):
        return self.account


class RiskMetrics(models.Model):
    name = models.CharField(primary_key=True, verbose_name='Наименование', max_length=200)

    class Meta:
        db_table = "public\".\"risk_metrics"
        verbose_name = 'Риск-метрика'
        verbose_name_plural = 'Риск-метрики'

    def __str__(self):
        return self.name


class PortfolioRisks(models.Model):
    risk_metric = models.ForeignKey('RiskMetrics', primary_key=True, db_column='risk_metric', on_delete=models.CASCADE,
                                    verbose_name='Риск-метрика')
    account = models.ForeignKey('Portfolio', db_column='account', on_delete=models.CASCADE, verbose_name='Портфель')
    value = models.FloatField(verbose_name='Значение')
    updated = models.BooleanField(verbose_name='Обновлено', default=False)
    violation = models.BooleanField(verbose_name='Нарушение', default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['risk_metric', 'account'], name='account_risk_primary_key')
        ]
        db_table = "public\".\"portfolio_risks"
        verbose_name = 'Риски портфеля'
        verbose_name_plural = 'Риски портфелей'

    def __str__(self):
        return self.account


class PortfolioStrategyHistory(models.Model):
    account = models.ForeignKey('Portfolio', primary_key=True, db_column='account', on_delete=models.CASCADE,
                                verbose_name='Портфель')
    changed_date = models.DateField(verbose_name='Дата изменения')
    strategy_id = models.ForeignKey('Strategy', db_column='strategy_id', on_delete=models.CASCADE,
                                    verbose_name='Стратегия')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'changed_date'], name='account_date_primary_key')
        ]
        db_table = "public\".\"portfolio_strategy_history"
        verbose_name = 'История измения стратегии портфеля'
        verbose_name_plural = 'История измения стратегий портфелей'

    def __str__(self):
        return self.account


class SupportMessages(models.Model):
    msg_date = models.DateField(verbose_name='Дата обращения', primary_key=True)
    user_id = models.ForeignKey('User', db_column='user_id', on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    message = models.TextField(verbose_name='Текст обращения')
    answer = models.TextField(verbose_name='Текст ответа', blank=True)
    done = models.BooleanField(verbose_name='Выполнено', default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['msg_date', 'user_id'], name='user_date_primary_key')
        ]
        db_table = "public\".\"support_messages"
        verbose_name = 'Обращение в поддержку'
        verbose_name_plural = 'Обращения в поддержку'

    def __str__(self):
        return f"{str(self.msg_date)} {'Выполнено' if self.done else 'Ожидает ответа'}"
