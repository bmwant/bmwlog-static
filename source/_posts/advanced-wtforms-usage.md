---
title: Advanced wtforms usage
date: 2018-06-08 11:08:24
tags: [python, forms, web, validation, framework]
author: Misha Behersky
language: en
---

WTForms is a powerful form validation and rendering library especially for web development. It's framework agnostic but there are packages that integrate it with popular web frameworks (e.g. [Flask WTF](https://flask-wtf.readthedocs.io/en/stable/) ). In this article I'm going to cover some advanced techniques which is not covered in documentation.

### Creating custom fields
If you want to add some non-standard field to your form you can create a custom field. First you need to inherit from appropriate field to describe which type of value you want to get as a result (`StringField` will fit in most cases) and then define a widget on it. Widget is a class returning an html string when called. This is the place where you define how it will be rendered on a page.
In the example below we will create a field for [jquery on-off switch](https://github.com/timmywil/jquery.onoff).

```python
from wtforms.widgets import HTMLString, CheckboxInput

class OnOffInput(CheckboxInput):
    def __call__(self, *args, **kwargs):
        if 'checked' not in kwargs:
            kwargs['checked'] = True
        parent_html = super(CheckboxInput, self).__call__(*args, **kwargs)
        onoff_html = '<div class="form-onoff">{}</div>'.format(parent_html)
        return HTMLString(onoff_html)


class OnOffField(wtforms.BooleanField):
    widget = OnOffInput()


class ToggleForm(Form):
    toggle = OnOffField('Toggle me')
```
So our widget is just a class which implements `__call__` method so when rendering it returns string representation of its html code. And as a result we get a nice switch on our page.

![switch](/old/article/2d5af865b8993265ae3ca548a47e6e55.png)

In case you do not want to create a new field and just need to slightly customize some of existing you can just pass different widget when instantiating.

```python
from wtforms.widgets import TextInput

class AutoFocusTextInput(TextInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('autofocus', True)
        return super(AutoFocusTextInput, self).__call__(field, **kwargs)


class NameForm(Form):
    first_name = wtforms.StringField(widget=AutoFocusTextInput())
    last_name = wtforms.StringField()
```
This way you will tell wtforms to render regular text input but with [autofocus](https://www.w3schools.com/tags/att_input_autofocus.asp) attribute on it.

### Store your own properties on a field
Sometimes you want to store additional data on your field and be able to pass it during field initialization stage. So you cannot just inherit from a `Field` class each time you want to customize a field. One way is to override `__init__` method with a [monkey patch](https://en.wikipedia.org/wiki/Monkey_patch). For example when rendering a field we want some flag telling us whether to display label for it or not. In the template it looks like this (assuming [Jinja2](http://jinja.pocoo.org/docs)-like syntax)

```html
<div class="form-field">
  {% if field.show_label | default(True) %}
    {{ field.label }}
  {% endif %}
  {{ field(**kwargs)|safe }}
</div>
```
And to control visibility of a field's label we need to provide `show_label` boolean value when defining a field for our form. But first let's allow a field to accept such a parameter.

```python
import wtforms

old_field_init = wtforms.Field.__init__

def new_field_init(self, *args, **kwargs):
    if 'show_label' in kwargs:
        self.show_label = kwargs.pop('show_label')

    old_field_init(self, *args, **kwargs)

wtforms.Field.__init__ = new_field_init
```

### Custom name for a field
You might want to customize default name for field that will be set on html input. Most of the time you should be fine with the default name (field variable named with underscores). But if you need hyphens or your front end framework requires different name convention you can provide your own name or specify a rule of how to generate a name for you. For this purpose we will dive a bit to a world of [metaclasses](https://realpython.com/python-metaclasses/). Basically we will provide our metaclass for a `Form` which will responsible for binding declared fields to our form and setting desired name in the meanwhile.

```python
from wtforms.meta import DefaultMeta

class BindNameMeta(DefaultMeta):
    def bind_field(self, form, unbound_field, options):
        if 'custom_name' in unbound_field.kwargs:
            options['name'] = unbound_field.kwargs.pop('custom_name')
        return unbound_field.bind(form=form, **options)


class Form(wtforms.Form):
    Meta = BindNameMeta
```
Just create a form as usually passing `custom_name` keyword argument on any field you don't want the default name to be set.

```python
class NameForm(Form):
    first_name = StringField('Name', custom_name='first-name')
```
As you can see we specified a name with hyphens instead of default one with underscores. If that's what you are looking for on regular basis you can just pass `name` parameter with applied `str.replace('_', '-')` method. They said [WTForms 3.0 will support](https://github.com/wtforms/wtforms/issues/205) specifying a name for an input but for now we need to use this workaround

### Create custom validators
Each field allows to store a list of validators (functions returning boolean value and checking field data to correspond your criteria). Some of them are `InputRequired`, `Length`, `Optional` and you can easily implement most business requirements using `Regexp` validator. When more control is needed you can implement your own validator. So validator is a class(callable) accepting `form` and `field` parameters and raising `ValidationError` if data doesn't fit your condition.

```python
from wtforms import IntegerField
from wtforms.validators import ValidationError

class DivisibleByValidator(object):
    def __init__(self, number=1):
        self.number = number

    def __call__(self, form, field):
        value = int(field.data)
        if value % self.number != 0:
            raise ValidationError(
                '{} is not divisible by {}'.format(value, self.number))


class NumbersForm(Form):
    divisible = IntegerField(validators=[DivisibleByValidator(3)])


form = NumbersForm(data={'divisible': 7})
if not form.validate():
    print(form.errors)
```
As expected we will get `{'divisible': ['7 is not divisible by 3']}` message because form did not validate.

### Passing regular dicts to a form constructor
When instantiating a form wtforms expects some sort of request-data wrapper which can get multiple parameters from the form input, e.g. a Werkzeug/Django MultiDict. So to create a form you need either to provide `data` parameter or use a wrapper around your dictionary. Note that `data` will be used only if you did not provide `formdata` and `obj` arguments when creating a form.

```python
class NameForm(Form):
    first_name = wtforms.StringField(widget=AutoFocusTextInput())
    last_name = wtforms.StringField()

data = {'first_name': 'Misha', 'last_name': 'Behersky'}
form = NameForm(data=data)
print(form.first_name.data, form.last_name.data)
```

But in case you need to override default `Form` behavior or will be implementing your own version of `process` method you definitely will need to follow the approach below

```python
class MultiDictWrapper(dict):
    def getlist(self, key):
        return [self[key]]


data = {'first_name': 'Misha', 'last_name': 'Behersky'}
wrapped_data = MultiDictWrapper(data)

form = NameForm(wrapped_data)
print(form.first_name.data, form.last_name.data)
```

### Custom validation for a form
One of the most useful features is the ability to validate data passed to the form. As we already created our custom version of a `Form` it would be nice to enhance it with additional abilities. Imagine we want a form to be valid only when request is made with `POST` method. Instead of checking request method every time in your view/handler we can implement that directly on a form and reuse it later as many times as we want.

```python
class Form(wtforms.Form):
    def validate_on_post(self):
        if request.method in ('POST', 'PUT'):
            return super(Form, self).validate()
        return False
```

Exact implementation might be framework-dependent but general idea is to add any validation logic to a form itself. You can even update `self._errors` attribute  for a form to be more verbose about what happened wrong. And now instead of calling `form.validate()` just invoke the newly defined method

```python
form = MyForm(data)
if not form.validate_on_post():
    print('Invalid form', form.errors)
    # Render a page displaying your error message
```

### Populating an object with form data
`populate_obj` method allows a form to set attributes on some arbitrary object. Each field name on a from will correspond to an attribute name and value will be set to a field data. Sometimes you may want to set only a subset of fields or specify another target which differs from field name. We just need to override this method and implement custom logic within it. In the example below we will populate our objects according to specified target fields.

```python
import wtforms

class Form(wtforms.Form):
    def populate_obj(self, obj):
        for name, field in self._fields.items():
            target_name = getattr(field, 'target_name', name)
            field.populate_obj(obj, target_name)
```

This way we will check a field for additional parameter defining target name and if none found follow the default behavior and use regular field name. Usage will look like the following

```python
class NameForm(Form):
    first_name = StringField(target_name='name')
    last_name = StringField(target_name='surname')


class Person(object):
    def __init__(self):
        self.name = ''
        self.surname = ''


data = {
    'first_name': 'Misha',
    'last_name': 'Behersky',
}

name_form = NameForm(data=data)
person = Person()
name_form.populate_obj(person)
print(name_form.first_name.data, name_form.last_name.data)
print(person.name, person.surname)
```

Be aware that your `StringField` should support arbitrary keyword arguments (`target_name` in our example) to work properly. You can accomplish this by subclassing a field and creating your own implementation that does support such a behavior or patch all the fields at once as mentioned in _Creating custom fields_ section above. The simplest way is to create class like this

```python
class StringField(wtforms.StringField):
    def __init__(self, *args, **kwargs):
        if 'target_name' in kwargs:
            self.target_name = kwargs.pop('target_name')

        super(StringField, self).__init__(*args, **kwargs)
```

But if you use more than one type of field (and in most cases you do) the better way is to modify all of them.
That's mostly it. I did not describe password confirmation field and file upload fields because there are recipes on the web for that but will probably add another article on that later.

See you then.

### Resources
* [wekzeug multidict](http://werkzeug.pocoo.org/docs/0.14/datastructures/#werkzeug.datastructures.MultiDict)
* [marshmallow validation/serialization library](http://marshmallow.readthedocs.io/en/latest/index.html)
* [Trafaret library for schema validation](https://github.com/Deepwalker/trafaret)
