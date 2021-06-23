---
title: Django integrity error while running migration
date: 2018-05-31 10:31:33
tags: [fix, django, error, python, migrations]
author: Misha Behersky
---

Recently I've got an error when invoking `python manage.py migrate`

```
Traceback (most recent call last):
  File "/home/ubuntu/virt/lib/python3.5/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
psycopg2.IntegrityError: duplicate key value violates unique constraint "django_migrations_pkey"
DETAIL:  Key (id)=(99) already exists.
```

This one means that you have out of date sequence within your database (improper previous migrations or jumps between different versions of code which leads to migrations being applied in chaotic order can cause this broken state). To quickly workaround this issue you can manually update values in your database. Go with `python manage.py dbshell` and check current values

```sql
SELECT last_value FROM django_migrations_id_seq;
SELECT l
ast_value FROM django_content_type_id_seq;
```
Then update them with a command below (any sane values that are greater than ones from output above). Usually first command is enough but if you are still getting errors with `key value violates unique constraint "django_content_type_pkey"` you need to run second one as well (you might need to alter `auth_permission_id_seq` too depending on your database state)

```sql
ALTER SEQUENCE django_migrations_id_seq RESTART WITH 101;
ALTER SEQUENCE django_content_type_id_seq RESTART WITH 212;
```

### Resources
* [Related question on StackOverflow #1](https://stackoverflow.com/questions/19135161/django-db-utils-integrityerror-duplicate-key-value-violates-unique-constraint)
* [Related question on StackOverflow #2](https://stackoverflow.com/questions/32943214/django-db-migration-failed-with-postgres)
