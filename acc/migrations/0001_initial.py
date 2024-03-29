# Generated by Django 4.0.5 on 2022-12-29 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('name', models.CharField(default='0', max_length=40, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(default='Balance', max_length=100, unique=True)),
                ('assets', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('liabilities', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('acc_type', models.IntegerField(default=2)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='acc.account')),
            ],
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reversed', models.BooleanField(default=False)),
                ('reverse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='acc.assign')),
            ],
        ),
        migrations.CreateModel(
            name='AssignDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='acc.assign')),
                ('credit_acc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='credit_acc', to='acc.account')),
                ('debit_acc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='debit_acc', to='acc.account')),
            ],
        ),
        migrations.CreateModel(
            name='AccountHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assets', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('liabilities', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('amaount_debit', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('amount_credit', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('end_assets', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('end_liabilities', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('end_balance', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('assignDetail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='acc.assigndetail')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='acc.account')),
            ],
        ),
    ]
