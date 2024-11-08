# Generated by Django 4.2.16 on 2024-11-01 10:58
import logging

from django.db import migrations
import django_migration_linter as linter

logger = logging.getLogger(__name__)


def populate_slack_channel(apps, schema_editor):
    ResolutionNoteSlackMessage = apps.get_model("alerts", "ResolutionNoteSlackMessage")
    SlackChannel = apps.get_model("slack", "SlackChannel")
    AlertGroup = apps.get_model("alerts", "AlertGroup")
    AlertReceiveChannel = apps.get_model("alerts", "AlertReceiveChannel")
    Organization = apps.get_model("user_management", "Organization")

    logger.info("Starting migration to populate slack_channel field.")

    sql = f"""
    UPDATE {ResolutionNoteSlackMessage._meta.db_table} AS rsm
    JOIN {AlertGroup._meta.db_table} AS ag ON ag.id = rsm.alert_group_id
    JOIN {AlertReceiveChannel._meta.db_table} AS arc ON arc.id = ag.channel_id
    JOIN {Organization._meta.db_table} AS org ON org.id = arc.organization_id
    JOIN {SlackChannel._meta.db_table} AS sc ON sc.slack_id = rsm._slack_channel_id
                           AND sc.slack_team_identity_id = org.slack_team_identity_id
    SET rsm.slack_channel_id = sc.id
    WHERE rsm._slack_channel_id IS NOT NULL
      AND org.slack_team_identity_id IS NOT NULL;
    """

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql)
        updated_rows = cursor.rowcount  # Number of rows updated

    logger.info(f"Bulk updated {updated_rows} ResolutionNoteSlackMessage records with their Slack channel.")
    logger.info("Finished migration to populate slack_channel field.")


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0063_migrate_channelfilter_slack_channel_id'),
    ]

    operations = [
        # simply setting this new field is okay, we are not deleting the value of channel
        # therefore, no need to revert it
        linter.IgnoreMigration(),
        migrations.RunPython(populate_slack_channel, migrations.RunPython.noop),
    ]
