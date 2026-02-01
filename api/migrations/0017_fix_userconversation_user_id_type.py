from django.db import migrations


def fix_userconversation_user_id_type(apps, schema_editor):
    """Ensure api_userconversation.user_id is an integer FK in PostgreSQL.

    In your Railway Postgres DB this column was created/modified as a
    character varying, which breaks joins to auth_user.id (integer).
    We delete any rows with non-numeric user_id values, then cast the
    column to integer so it matches the Django ForeignKey definition.
    """

    connection = schema_editor.connection
    if connection.vendor != "postgresql":
        # Only relevant to the Railway Postgres database.
        return

    with connection.cursor() as cursor:
        # Drop any rows where user_id cannot be safely cast to integer.
        cursor.execute(
            "DELETE FROM api_userconversation WHERE user_id !~ '^[0-9]+$';"
        )
        # Cast the column to integer so it matches auth_user.id.
        cursor.execute(
            "ALTER TABLE api_userconversation "
            "ALTER COLUMN user_id TYPE integer USING user_id::integer;"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_activity_lounge_models"),
    ]

    operations = [
        migrations.RunPython(fix_userconversation_user_id_type, migrations.RunPython.noop),
    ]
