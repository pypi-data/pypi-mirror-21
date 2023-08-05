<h1 align="center">
  <img src="https://raw.githubusercontent.com/Daanvdk/jackster/master/logo_full.png" alt="Jackster"/>
</h1>
A python micro webframework focused on keeping your code DRY and short without any black box magic.

## Hello world
Hello world is very short in Jackster, these 3 lines do the trick:
```python
from jackster import Router
from jackster.funcs import html
Router().get(html('Hello world!')).listen()
```

## Table of Contents
- [Jackster](#jackster)
- [Hello World](#hello-world)
- [Table of Contents](#table-of-contents)
- [Routing](#routing)
  - [Example 1](#example-1)
  - [Example 2](#example-2)
  - [Example 3](#example-3)
- [Functions](#functions)
- [Function chaining](#function-chaining)
- [Install](#install)
- [Dependencies](#dependencies)

## Routing
Routing is done in Jackster by `Router`-objects, these support all kind of methods
to define actions for certain request methods on certain urls. The easiest way
to explain this is by just showing it. Since there are multiple ways to do this
in Jackster we have shown three examples that all do the same.

(Don't bother with all those variables that end with `Handler` for now.)

### Example 1
This example illustrates some basic `Router.get` and `Router.post`-method usage and shows how
to create dynamic urls using regex.
```python
router = Router()

router.get(r'^/home$', homeHandler)

router.get(r'^/shop$', shopHandler)
router.get(r'^/shop/(?P<item_id>\d+)$', shopDetailHandler)

router.get(r'^/contact$', contactHandler)
router.post(r'^/contact$', contactSendHandler)
```

### Example 2
Here we use the `Router.route`-method to create a nested router to avoid redundancy in
our urls. We can also see that when we have a route associated with a router you
can omit the path inside of the `Router.get`-method and other similar methods.
```python
router = Router()

router.get(r'^/home$', homeHandler)

shopRouter = router.route(r'^/shop')
shopRouter.get(shopHandler)
shopRouter.get(r'^/(?P<item_id>\d+)$', shopDetailHandler)

contactRouter = router.route(r'^/contact')
contactRouter.get(contactHandler)
contactRouter.post(contactSendHandler)
```

### Example 3
Here we show that you can also chain all these functions together and how to use
the `Router.use`-method to nest Routers within such a chain. Note that you need the parentheses around the top `Router` to be allowed to call methods from lines under it.
```python
router = (Router()
    .get(r'^/home$', homeHandler)
    .use(r'^/shop', Router()
        .get(shopHandler)
        .get(r'^/(?P<item_id>\d+)$', shopDetailHandler)
    )
    .use(r'^/contact', Router()
        .get(contactHandler)
        .post(contactSendHandler)
    )
)
```

## Functions
You have already seen a few Jackster functions in the past few code snippets.
`html('Hello World!')` was one (where `html` is a *function generator*), and all
`Handler` variables should be one.

So two very obvious questions now would be how do these functions work and how
can I make my own? They are both very easy to answer.

All functions have 3 required arguments, through convention named `req`, `res`
and `nxt`. If you want to name any of them differently that is fine as well.

`req` and `res` are a `jackster.Request` and a `jackster.Response` object
respectively, you use `req` to get information about the request that you are
handling and you use `res` to set the data that we will eventually return. We
will cover `nxt` in the next section.

Since these 3 arguments are the only thing that defines a Jackster function they
are very easy to create. If we would want to create our own Hello World function
for example:
```python
def helloWorld(req, res, nxt):
    res.html('Hello world!')
```
Or even if we would want to create our own function generator (like `html`):
```python
def html(html):
    def func(req, res, nxt):
        res.html(html)
    return func
```

## Function chaining
In Jackster we like to chain small clear functions to create powerful big
functions. Since most big functions in web development share a lot of repetition
this works really nicely. The `nxt`-argument we talked about previously is a
function that calls the next function in the chain. You don't have to pass on
`req`, `res` and a new value for `nxt`, Jackster does that for you. You are
however allowed to pass any other arguments or keyword arguments you want into
`nxt` and they will be passed on to the next function.

So how do you create these function chains, very simple. Jackster has the
`jackster.funcs.chain` function for this purpose, you can pass as many functions
as you want into this function and it will chain them into one function.

You however probably won't even need to use this function. When you supply a
list or tuple of functions in a spot where Jackster would expect a single
function Jackster is smart enough to chain them into one function for you. This
is even a bit faster since it will convert nested lists a bit more efficiently
than nested calls to `jackster.funcs.chain`.

## Install
Jackster is on pip, you can install it with:
```
pip install jackster
```

## Dependencies
Jackster is built on python 3.5 and uses the jinja2-package for templating. It
is likely that in the near future new versions of Jackster will also require
SQLAlchemy and Alembic for ORM and Migrations.

## About
Jackster is named after my cat Jack, hence the cat logo.
