---
title: Alter field migration with Peewee
date: 2018-05-24 09:50:37
tags: [sql, mysql, python, peewee, migrations, orm]
author: Misha Behersky
language: en
---

[Peewee](http://docs.peewee-orm.com/en/latest/) - is very small though powerful ORM for Python. It even support migration within its own [playhouse](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations). In the simplest form you can write migrations like this

```python
from peewee import CharField, MySQLDatabase
from playhouse.migrate import migrate, MySQLMigrator


db = MySQLDatabase('db_name', host='127.0.0.1', port='3306',
                   user='db_user', password='db_password')
migrator = MySQLMigrator(db)

table_name = 'my_table'
new_field = CharField(null=False, default='empty', max_length=100)

migrate(
    migrator.add_column(table_name, 'new_column', new_field)
)
```

We can do migrations for `MySQL`, `SQLite` and `PostgreSQL` and supported operations are: `add_column`, `rename_column`, `drop_column`, `rename_table`, `add_index`, `drop_index`, `add_not_null`, `drop_not_null`, so basically you can accomplish most of the common tasks on your database migration.

So what's the issue? Recently I faced problem to migrate one column in my table. In case you don't worry about losing a data you can simply `drop_column` and `add_column` with a new definition or `rename_column`, `add_column`, apply custom script which will copy all the data to new field and finally `drop_column`.
But there is another approach allowing us to use a shortcut and migrate our database the same way as we would do that using raw SQL (smth like `ALTER TABLE <table_name> MODIFY <col_name> VARCHAR(<new_value>);`)
As we can see `migrate` command accepts list of operation from our migrator, so all we need is to implement another `change_column_type` operation in our migration. Let's create our own migrator which will support modifying columns!
First we subclass `MySQLMigrator` and add an `operation` method to it.

```python
from playhouse.migrate import MySQLMigrator, operation

class ExtendedMySQLMigrator(MySQLMigrator):
    @operation
    def change_column_type(self, table, column_name, new_field):
        pass
```

Every operation should return `Context` instance which is basically an object containing all the data needed to generate resulting SQL. We already have an idea about how the final sql code should look like, so all we need is to provide required data to generate that statement.

```python
def change_column_type(self, table, column_name, new_field):
    ctx = self.make_context()
    field_ddl = new_field.ddl(ctx)
    change_ctx = (self
                  .make_context()
                  .literal('ALTER TABLE ')
                  .sql(Entity(table))
                  .literal(' MODIFY ')
                  .sql(Entity(column_name))
                  .sql(field_ddl))
    return change_ctx
```

There are `literal` methods which will evaluate straight to the code provided as parameter and `Entity` which tells peewee to escape names to be valid sql. At the end we insert definition for our field also as sql. We can use our migrator with newly implemented method right after this:

```python
migrator = ExtendedMySQLMigrator(db)

table_name = 'my_table'
column_name = 'new_column'
updated_column = CharField(null=False, default='empty', max_length=555)

migrate(
    migrator.change_column_type(table_name, column_name, updated_column)
)
```

There is another small improvement to this code: we actually need to modify a column that is already present on our model (bound to it), so there is no need to provide `column_name` parameter as it is already known by peewee. So we remove that parameter and not provide *column_name* entity manually.

```python
@operation
def change_column_type(self, table, new_field):
    ctx = self.make_context()
    field_ddl = new_field.ddl(ctx)
    change_ctx = (self
                  .make_context()
                  .literal('ALTER TABLE ')
                  .sql(Entity(table))
                  .literal(' MODIFY ')
                  .sql(field_ddl))
    return change_ctx
```

When applying migration we can know provide update field directly from that model class itself like the following

```python
class User(Model):
    class Meta:
        db_table = 'user'

    user_id = PrimaryKeyField(db_column='user_id')
    # name = CharField(null=True, max_length=10)  # old field
    name = CharField(null=False, max_length=23)

table_name = User._meta.name
updated_column = User.name

migrate(
    migrator.change_column_type(table_name, updated_column)
)
```

Don't forget to create a database backup before applying any migrations (especially your own, especially not well-tested)!
Happy database migration :)

### Resources
* [Wrapper around migrations to apply all of them](https://github.com/bmwant/bmwlog/blob/master/app/migrations/__main__.py)
* [Migrations engine for peewee (complex version of the above)](https://github.com/klen/peewee_migrate)
