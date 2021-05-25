---
title: Serialize arbitrary objects to YAML with Python
date: 2018-10-19 19:42:39
tags: [yaml, attrs, python, serialization]
author: Misha Behersky
---

When working with [YAML](http://yaml.org/) files in Python you probably are using [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) library. This is handy when storing configuration files, nested structures or sequence-like data. The nice thing about it is the ability to dump/load Python objects as well (not only regular _int_'s, _str_'s, _float_'s, _list_'s). In this article we are going to talk about customizing this serialization process and adapting resulting format to our needs.

Suppose we have a `User` model written with a help of another great library named [attrs](https://www.attrs.org/en/stable/)
```
import attr

@attr.s
class User(object):
    name: str = attr.ib()
    age: int = attr.ib(default=0)
```
We can create our own store with a list of users and serialize/deserialize it to a file
```
users = []
user1 = User(name='Misha', age=24)
user2 = User(name='Bob', age=42)

users.append(user1)
users.append(user2)

with open('users.yml', 'w') as f:
    f.write(yaml.dump(users))

with open('users.yml') as f:
    data = yaml.load(f)

assert len(data) == len(users)
user = data[0]
assert isinstance(user, User)
print(user.name)
```
That's pretty neat to have such a convenient method of storing any Python object in a file. But look at the output
```
- !!python/object:__main__.User {age: 24, name: Misha}
- !!python/object:__main__.User {age: 42, name: Bob}
```
It's not what I've expected to see and it's not what can be easily edited manually without accidentally messing with its structure. What we want actually is to have something like this one
```
- name: Misha
  age: 24
- name: Bob
  age: 42
```
Trying to step back and store our users as regular dictionaries doesn't help too
```
users = [{'name': 'Misha', 'age': 24}, {'name': 'Bob', 'age': 42}]

with open('users.yml', 'w') as f:
    f.write(yaml.dump(users))
```
We'll still have a slightly different output from desired one
```
- {age: 24, name: Misha}
- {age: 42, name: Bob}
```
It's pretty easy to fix that passing additional parameters to dump function
```
yaml.dump(users, default_flow_style=False, indent=2)
```
At this point we've got nicely formatted output. You can also provide `default_style` argument. YAML provides three styles: double-quoted, single-quoted and plain (unquoted). Pass `default_style='"'` in case you want items in your output to be quoted.
But that is only for regular dictionary and we wanted to have such a nice output for our custom objects. There is still type definition for each record `!!python/object:__main__.User`. We can shift responsibility of loading an instance from library to class
itself. This way our class will know how to create it's instances from regular dicts and resulting file will be clean and human readable. We can implement `to_dict` method on our class but hopefully _attrs_ has its own `attr.asdict` function. 
The next thing we need to implement is our own `Dumper` class that will be passed to `yaml.dump` method when serializing `User` objects. This class is somewhat a complex thing inherited from `Emitter`, `Serializer`, `Representer`, `Resolver`
bases. But the only one we care about is `Representer` deciding how our object will look like in the target output.
```
from yaml.representer import SafeRepresenter

class UserRepresenter(SafeRepresenter):
    def represent_user(self, user_obj):
        data = attr.asdict(user_obj)
        return self.represent_mapping('tag:yaml.org,2002:map', data)
				
UserRepresenter.add_representer(User, UserRepresenter.represent_proxy)
```
We need to define our own represent method which basically will create a dict from our object and than invoke existing `represent_mapping` implementation. Here's the place where you can provide your own logic or call something like `obj.serialize` method.
Then we declare our dumper class which is just a subclass of `SafeDumper` and our `UserRepresenter` classes. _Safe_ dumper limits the ability to use serialization with simple Python objects instead of regular one that is as powerful a [pickle](https://docs.python.org/3/library/pickle.html).
```
from functools import partial

class UserDumper(SafeDumper, UserRepresenter):
    pass

user_dump = partial(yaml.dump, default_flow_style=False, Dumper=UserDumper)
```
Having the code above in place let's check how it works with our users storage
```
users = [User(name='Misha', age=24), User(name='Bob', age=42)]

with open('users.yml', 'w') as f:
    user_dump(users, f)

with open('users.yml') as f:
    data = yaml.load(f)

loaded_users = [User(**u) for u in data]
print(loaded_users)
```
Here we go! Now we can dump/edit/load our users seamlessly within YAML file and we can write same process for any object we want. I'm going to leave you with a picture of this cat and its pet, have a good weekend.

![kitty](/img/article/da5aadcaaef03b119712acdcef558817.jpg)