---
title: Django migrations create index
tags: [python, django, migration, postgres, sql]
author: Misha Behersky
language: en
date: 2022-03-23 10:09:54
---

Sometimes you need to add an index to already existing field within the table for performance gains. However, operation of adding index locks table by default, so on production workload you cannot afford such a thing as it might cause downtime. The bigger table you have, the longer it takes to create an index resulting in table unavailability. PostgreSQL [supports](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY) building indexes without locking out writes, but let's see how Django handles this migration.

### Default behaviour

Consider having this simple `User` model

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

class User(AbstractBaseUser):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
```

At some point you have decided you need efficient sort on `date_created` field. Following the usual workflow you update the field like this

```python
date_created = models.DateTimeField(default=timezone.now, db_index=True)
```

and create corresponding migration file

```bash
$ python manage.py makemigrations
```

Somewhat similar to this migration file should be produced

```python
import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(
                db_index=True,
                default=django.utils.timezone.now,
            ),
        ),
    ]
```

We can check the underlying SQL code and verify that index will be created with command
`python manage.py sqlmigrate app 0002`

```sql
BEGIN;
--
-- Alter field date_created on user
--
CREATE INDEX "app_user_date_created_a9e0fc3e" ON "app_user" ("date_created");
COMMIT;
```

Nonetheless, this is not exactly what we need as the operation is blocking and cannot be applied safely on the production environment. Surely, you can execute `CREATE INDEX CONCURRENTLY` directly on the database, but it's a really bad practice to diverge code and database state when using an ORM.

### Proper solution

Here's the correct way of applying such a migration. I'll go over most important points below

```python
from django.db import migrations, models
from django.contrib.postgres.operations import AddIndexConcurrently

class Migration(migrations.Migration):
    atomic = False

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='user',
                    name='date_created',
                    field=models.DateTimeField(
                        db_index=True,
                    ),
                ),
            ],
            database_operations=[
                AddIndexConcurrently(
                    'user',
                    models.Index(
                        fields=['date_created'],
                        name='app_user_date_created_idx',
                    )
                ),
            ]
        ),
    ]
```

1. We are using [SeparateDatabaseAndState](https://docs.djangoproject.com/en/dev/ref/migration-operations/#django.db.migrations.operations.SeparateDatabaseAndState) operation to make sure any custom modification on the database schema (`database_operations`) has a corresponding change reflected within the model definition (`state_operations`)
2. We are using [AddIndexConcurrently](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/operations/#django.contrib.postgres.operations.AddIndexConcurrently) to leverage PostgreSQL feature of creating/dropping indexes without locking out writes.
3. We are setting `atomic = False` as concurrent option is not supported inside a transaction.

Note that we have no `BEGIN`/`COMMIT` section when checking underlying SQL code
`python manage.py sqlmigrate app 0002` (make sure to provide correct number for the migration)

```sql
--
-- Custom state/database change combination
--
CREATE INDEX CONCURRENTLY "app_user_date_created_idx" ON "app_user" ("date_created");
```

### Workaround for older Django versions

Support for concurrent index operation has been added in Django 3.0 version, so in case you are using older version for some reason here's a way you can achieve the same thing

```python
database_operations=[
    migrations.RunSQL(
        'CREATE INDEX CONCURRENTLY "app_user_date_created_idx" ON "app_user" ("date_created");',
        reverse_sql='DROP INDEX CONCURRENTLY "app_user_date_created_idx";',
    ),
]
```

Now the only thing left is to apply migrations the next time you deliver your code to production.

```bash
$ python manage.py migrate
```

### Resources

* [Non-atomic migrations in Django](https://docs.djangoproject.com/en/dev/howto/writing-migrations/#non-atomic-migrations)
* [Django sqlmigrate command](https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-sqlmigrate)
* [More detailed article on RealPython](https://realpython.com/create-django-index-without-downtime/)
