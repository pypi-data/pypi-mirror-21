Sourcerer
=========

![image](https://img.shields.io/pypi/v/sourcerer.svg)

Programatically generate PEP8 python source code

### Running examples

```bash
shark@tack ~/sourcerer/examples $ python swagger_to_flask.py ../sample_data/uber.yaml
shark@tack ~/sourcerer/examples $ python call_example.py
```

### Generate code from code

Let’s start with the absolute basics

```python
from sourcerer import Document, Statement

# The most important class in Sourcerer is the statement. Just about everything is a statement.
# Statements hold source code, and have a child scope. They can hold other statements.
# Even a document is just a special kind of Statement.
# A Document job is to hold statements and then output its contents.
doc = Document()

# Now we make a generic statement to assign 1 to x
s = Statement("x = 1")

# Add it to the  document.
# add_child() is a member function of Statement. It will append to a Statements child scope.
doc.add_child(s)

# Now output the current document
# output() without an output_file_name will output to standard out.

doc.output()
```

**Output**:

```python
x = 1
```

Let’s use some of the purpose built tools in Sourcerer to make this easier to generate.

```python
from sourcerer import Document, Name

doc = Document()

# Names are variable/function/class/etc... names
# We'll use a good name
good_name = Name("descriptive_name")

# and a bad name
bad_name = Name("1@*plz_help")

# Add both the children at once

doc.add_children([good_name, bad_name])

doc.output()
```

**Output**:

```python
descriptive_name
plz_help
```

Notice the bad name has been transformed into a valid python name, this behavior can be turned off by setting validate=False

Let’s get back to that naive assignment we first made. We can improve it using Name and Assignment. We’ll also use Num just for good practice.

```python
from sourcerer import Document, Name, Assignment, Num

doc = Document()

# We'll wrap this up in one line because it's not that long.
# Num can take a string, int, long, float, etc...
a = Assignment(Name("x"), Num("1"))

doc.add_child(a)

doc.output()
```

**Output**:

```python
x = 1
```

Now that we’re warmed up, let’s do something more interesting. How about some functions?

```python
from sourcerer import Document, FunctionDef, Return, Str, Num, Name, Assignment, DecoratorDef, Call

doc = Document()

# A function that returns 0
func_a = FunctionDef(name=Name("get_a_zero"))
ret_a = Return(Num("0"))

func_a.add_child(ret_a)
doc.add_child(func_a)

# A function that passes. We'll put it in an list for easier consumption later
func_b = [FunctionDef(name=Name("just_pass")),
          Return(_type="pass")
]

# Cascade the list of statements
doc.create_lineage(func_b)

# A function with args, and a *arg
func_c = [FunctionDef(name=Name("so_many_args"), arg_names=["a1", Name("a2")], varargs="args"),
          Return(Str("Not enough time"))
]

doc.create_lineage(func_c)

# A function with kwargs, and a **
func_d = [FunctionDef(name=Name("so_many_kwargs"), kwarg_pairs={Name("a1"):"val"}, keywords="kwargs"),
          Return()
]

doc.create_lineage(func_d)

# A function decorated function. Philosophy: If things get complicated, just make them a list.
func_e = [DecoratorDef(name=Name("fancy")),
          FunctionDef(name=Name("pants")),
          Return(Str("Hello World!"))
]

doc.create_lineage(func_e)

doc.output()
```

**Output**:

```python
def get_a_zero():
    return 0


def just_pass():
    pass


def so_many_args(a1, a2, *args):
    return "Not enough time"


def so_many_kwargs(a1=val, **kwargs):
    return


@fancy()
def pants():
    return "Hello World!"
```

Here is an example that generates an extremely rough flask Blueprint from a swagger (<http://swagger.io/>) yml doc

``` python
from yaml import load
from sourcerer import Document, FunctionDef, DecoratorDef, Return, Str, Name, Call, Assignment, Attribute
from sys import argv

# Create a document to put our code in
doc = Document()

# Open our yml file and read it in
api = load(open(argv[1], 'r').read())

blueprint = Name(api['basePath'])

bp = Assignment(blueprint,
                Call(name="Blueprint",
                     arg_names=[Str(blueprint), '__name__'],
                     kwarg_pairs={'template_folder': Str('templates')}))

doc.add_child(bp)

for path in api['paths']:
    route = [DecoratorDef(name=Attribute(caller_list=[blueprint], name=Name('route')),
                          arg_names=[Str(path)]), # A decorator: @routename("mypath")
             FunctionDef(name=Name(path)), # A function: def routename():
             Return()] # A return statement: return

    doc.create_lineage(route) # Cascade these objects into the main document scope
                              # ...
                              # @routename("mypath")
                              # def routename():
                              #     return
                              # ...

doc.output() # Send output to standard out (output to file optional)

####################
# Without inline comments:
##

from yaml import load
from sourcerer import Document, FunctionDef, DecoratorDef, Return, Str, Name, Call, Assignment, Attribute
from sys import argv

doc = Document()

api = load(open(argv[1], 'r').read())

blueprint = Name(api['basePath'])

bp = Assignment(blueprint,
                Call(name="Blueprint",
                     arg_names=[Str(blueprint), '__name__'],
                     kwarg_pairs={'template_folder': Str('templates')}))
doc.add_child(bp)

for path in api['paths']:
    route = [DecoratorDef(name=Attribute(caller_list=[blueprint], name=Name('route')),
                          arg_names=[Str(path)]),
             FunctionDef(name=Name(path)),
             Return()]
    doc.create_lineage(route)

doc.output()
```

**Output:**

```python
v1 = Blueprint("v1", __name__, template_folder="templates")


@v1.route("/products")
def products():
    return


@v1.route("/estimates/price")
def estimatesprice():
    return


@v1.route("/history")
def history():
    return


@v1.route("/me")
def me():
    return


@v1.route("/estimates/time")
def estimatestime():
    return
```

## Technologies

* YAPF formatted output to produce pep8 compliant code


## Upcoming Features

### Generate code from Spellbooks

Source code can also be generated by ingesting and parsing a config document (ex. yaml, json, xml…), known as a Spellbook. Spellbooks can be parsed into source code be defining a schema, called a Syntax Map.

#### Example Spellbook (YAML):

```YAML
functions:
    func1:
        args: ['thing1', 'thing2']
        kwargs: {"key1": "val1"}
        varargs: false
        keywords: false
        ret:
            value:
                true
```

#### Example Syntax Map to parse this Spellbook:


```python
# Without inline comments
{"functions": {'type': FunctionDef,
               'key': 'name',
               'value_map': {'args': 'arg_names',
                             'kwargs': 'kwarg_pairs',
                             'varargs': 'varargs',
                             'keywords': 'keywords'},
               'children':{'ret':'return'}},
 "return": {'type': Return,
             'value_map': {'value':'val'}}
}

# With inline comments
{"functions": {'type': FunctionDef, # Each top level entry under functions is a FunctionDef
               'key': 'name', # The functions key (func1) is the value to the name argument for the FunctionDef
               'value_map': {'args': 'arg_names',  # Define what args are called in the markups schema
                             'kwargs': 'kwarg_pairs',
                             'varargs': 'varargs',
                             'keywords': 'keywords'},
               'children':{'ret':'return'}}, # When top-level objects are seen their values will be 
                                             # pared as well, building a new object from the mapping 
                                             # they specify and then appended to this object
 "return": {'type': Return,
             'value_map': {'value':'val'}}
}
```

#### Building a Syntax Map for a Spellbook:

Your Syntax Maps top-level keys define what your Spellbook top-level sections are containing. The values of your Syntax Map top-level keys are dictionaries defining how to handle the contents of your Spellbook sections.

In the given example, the only top-level Spellbook section is ‘functions’. In the Syntax Map, the ‘functions’ key’s value says several things:

1.  For each child node encountered, create a new FunctionObj (defined by ‘type’)
2.  The key defining each child node is the ‘name’ argument for the FunctionObj
3.  The sub-keys of the child node are properties of the FunctionObj. The values of those sub-keys are can be one of two things:
    -   If the value is in the value map, it is an argument to FunctionObj
    -   If the value is in the children map, it should be placed into the scope of the FunctionObj. The value will be looked up in the Syntax Map top-level to see if it can be be instantiated into a new sourcerer object.

#### The Syntax Map schema should consist of:

-   type (required): The class name to instantiate
-   key (required): what the key for the node represents
-   value\_map (required): map properties to arguments to the class
-   children: values that should be instantiated and placed into the current nodes child scope

#### Using a Syntax Map and Spellbook to generate your source:

Based on the example Syntax Map and the Example YAML, the following will write the resulting source code to stardard out

```python
from sourcerer import YAMLProcessor

gen = YAMLProcessor()
gen.load('sample_data/sample.yml')
gen.output()
```




History
-------

0.0.3 (2015-04-15)
---------------------




