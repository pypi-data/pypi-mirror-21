/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE.rst
 *****************************************************************************/

typedef struct {
    PyObject_HEAD
    PyObject *iterator;  /* iterator over data */
    PyObject *func;      /* Function to call */
    Py_ssize_t times;    /* Call side effects each x items */
    Py_ssize_t count;    /* Current counter when to call func */
    PyObject *collected; /* Collect items to pass to side-effects */
    PyObject *funcargs;  /* Wrapper for the arguments for the function */
} PyIUObject_Sideeffects;

PyTypeObject PyIUType_Sideeffects;

/******************************************************************************
 * New
 *****************************************************************************/

static PyObject *
sideeffects_new(PyTypeObject *type,
                PyObject *args,
                PyObject *kwargs)
{
    static char *kwlist[] = {"iterable", "func", "times", NULL};
    PyIUObject_Sideeffects *self;

    PyObject *iterable;
    PyObject *func;
    PyObject *iterator=NULL;
    PyObject *collected=NULL;
    PyObject *funcargs=NULL;
    Py_ssize_t times = 0;
    Py_ssize_t count = 0;

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|n:sideeffects", kwlist,
                                     &iterable, &func, &times)) {
        return NULL;
    }
    if (times <= 0) {  /* negative values will be interpreted as zero... */
        times = 0;
        collected = NULL;
    } else {
        collected = PyTuple_New(times);
        if (collected == NULL) {
            goto Fail;
        }
    }

    /* Create and fill struct */
    iterator = PyObject_GetIter(iterable);
    if (iterator == NULL) {
        goto Fail;
    }
    funcargs = PyTuple_New(1);
    if (funcargs == NULL) {
        goto Fail;
    }
    self = (PyIUObject_Sideeffects *)type->tp_alloc(type, 0);
    if (self == NULL) {
        goto Fail;
    }
    Py_INCREF(func);
    self->iterator = iterator;
    self->func = func;
    self->times = times;
    self->count = count;
    self->collected = collected;
    self->funcargs = funcargs;
    return (PyObject *)self;

Fail:
    Py_XDECREF(collected);
    Py_XDECREF(iterator);
    Py_XDECREF(funcargs);
    return NULL;
}

/******************************************************************************
 * Destructor
 *****************************************************************************/

static void
sideeffects_dealloc(PyIUObject_Sideeffects *self)
{
    PyObject_GC_UnTrack(self);
    Py_XDECREF(self->iterator);
    Py_XDECREF(self->func);
    Py_XDECREF(self->collected);
    Py_XDECREF(self->funcargs);
    Py_TYPE(self)->tp_free(self);
}

/******************************************************************************
 * Traverse
 *****************************************************************************/

static int
sideeffects_traverse(PyIUObject_Sideeffects *self,
                     visitproc visit,
                     void *arg)
{
    Py_VISIT(self->iterator);
    Py_VISIT(self->func);
    Py_VISIT(self->collected);
    Py_VISIT(self->funcargs);
    return 0;
}

/******************************************************************************
 * Next
 *****************************************************************************/

static PyObject *
sideeffects_next(PyIUObject_Sideeffects *self)
{
    PyObject *item, *temp=NULL, *tmptuple=NULL;
    Py_ssize_t i;

    item = (*Py_TYPE(self->iterator)->tp_iternext)(self->iterator);
    if (item == NULL) {
        /* We don't expect that the sideeffect function is called when
           an exception other than StopIteration is raised by the iterator so
           exit early in that case. */
        if (PyErr_Occurred()) {
            if (PyErr_ExceptionMatches(PyExc_StopIteration)) {
                PyErr_Clear();
            } else {
                return NULL;
            }
        }
        if (self->count != 0) {
            /* Call function with the remaining items. */
            tmptuple = PyTuple_GetSlice(self->collected, 0, self->count);
            if (tmptuple == NULL) {
                return NULL;
            }
            PYIU_RECYCLE_ARG_TUPLE(self->funcargs, tmptuple, return NULL);
            temp = PyObject_Call(self->func, self->funcargs, NULL);
            Py_DECREF(tmptuple);
            if (temp != NULL) {
                Py_DECREF(temp);
            }
            /* The case where temp == NULL is handled by the following
               "return NULL" anyway so it does not need to be a special case
               here. */
        }
        return NULL;
    }

    if (self->times == 0) {
        /* Always call the function if times == 0 */
        PYIU_RECYCLE_ARG_TUPLE(self->funcargs, item, goto Fail);
        temp = PyObject_Call(self->func, self->funcargs, NULL);
        if (temp == NULL) {
            goto Fail;
        } else {
            Py_DECREF(temp);
        }
    } else {
        Py_INCREF(item);
        /* Add the item to the collected tuple and call the function if
           count == times after incrementing the count. */
        PyTuple_SET_ITEM(self->collected, self->count, item);
        self->count++;
        if (self->count == self->times) {
            self->count = 0;
            PYIU_RECYCLE_ARG_TUPLE(self->funcargs, self->collected, goto Fail);
            temp = PyObject_Call(self->func, self->funcargs, NULL);
            if (temp == NULL) {
                goto Fail;
            } else {
                Py_DECREF(temp);
            }
            /* Try to reuse collected if possible. In this case the "funcargs"
               and the class own a reference to collected so we can only
               reuse the collected tuple IF nobody except the instance owns
               the "funcargs" and nobody except the instance and the funcargs
               owns the "collected". This can be up to 40-50% faster for small
               "times" values. Even for relativly bigger ones this is still
               10% faster.
               To avoid needing to decrement the values in the tuple while
               iterating these are simply set to NULL.
               */
            if (Py_REFCNT(self->funcargs) == 1 &&
                    Py_REFCNT(self->collected) <= 2) {
                for (i=0 ; i < self->times ; i++) {
                    temp = PyTuple_GET_ITEM(self->collected, i);
                    PyTuple_SET_ITEM(self->collected, i, NULL);
                    Py_DECREF(temp);
                }
            } else {
                Py_DECREF(self->collected);
                self->collected = PyTuple_New(self->times);
                if (self->collected == NULL) {
                    goto Fail;
                }
            }
        }
    }

    return item;

Fail:
    Py_XDECREF(item);
    return NULL;
}

/******************************************************************************
 * Reduce
 *****************************************************************************/

static PyObject *
sideeffects_reduce(PyIUObject_Sideeffects *self)
{
    PyObject *collected;
    PyObject *res;

    /* There are several issues that prevent from simply wrapping the
       attributes.
       */
    if (self->collected == NULL) {
        /* When "collected" is NULL we wrap it as None, and no further
           processing is needed.
           */
        Py_INCREF(Py_None);
        collected = Py_None;
    } else {
        /* When we have "collected" then it's a tuple that may contain NULLs.
           The Python interpreter does not like NULLs so these must be
           replaced by some fillvalue (in this case None). However we modify
           the tuple inside the "next" method so if someone called "reduce"
           that person could **see** the "collected" tuple change. That must
           be avoided so we MUST return a copy of the "collected" tuple.
           */
        Py_ssize_t i;
        Py_ssize_t collected_size = PyTuple_GET_SIZE(self->collected);
        collected = PyTuple_New(collected_size);
        if (collected == NULL) {
            return NULL;
        }
        for (i = 0 ; i < collected_size ; i++) {
            PyObject *tmp = PyTuple_GET_ITEM(self->collected, i);
            if (tmp == NULL) {
                tmp = Py_None;
            }
            Py_INCREF(Py_None);
            PyTuple_SET_ITEM(collected, i, tmp);
        }
    }

    res = Py_BuildValue("O(OOn)(nO)", Py_TYPE(self),
                        self->iterator,
                        self->func,
                        self->times,
                        self->count,
                        collected);
    Py_DECREF(collected);
    return res;
}

/******************************************************************************
 * Setstate
 *****************************************************************************/

static PyObject *
sideeffects_setstate(PyIUObject_Sideeffects *self,
                     PyObject *state)
{
    Py_ssize_t count;
    PyObject *collected;
    PyObject *newcollected = NULL;
    Py_ssize_t collected_size;

    if (!PyTuple_Check(state)) {
        PyErr_Format(PyExc_TypeError,
                     "`%.200s.__setstate__` expected a `tuple`-like argument"
                     ", got `%.200s` instead.",
                     Py_TYPE(self)->tp_name, Py_TYPE(state)->tp_name);
        return NULL;
    }

    if (!PyArg_ParseTuple(state, "nO:sideeffects.__setstate__",
                          &count, &collected)) {
        return NULL;
    }

    /* The "collected" argument should be a tuple (because we use
       PyTuple_GET_ITEM and PyTuple_SET_ITEM and thus would risk segmentation
       faults if we don't check that it's a tuple) or None.
       */
    if (PyTuple_CheckExact(collected)) {
        /* The class itself has a "times" attribute, if that attribute is zero
           we do not need a "collected" tuple, it should have been "None".
           */
        if (self->times == 0) {
            PyErr_Format(PyExc_TypeError,
                         "`%.200s.__setstate__` expected `None` as second "
                         "argument in the `state` when `self->times == 0`, "
                         "got %.200s.",
                         Py_TYPE(self)->tp_name, Py_TYPE(collected)->tp_name);
            return NULL;
        }
        /* The "count" must not be negative or bigger/equal to the size of
           the "collected" tuple. Otherwise we would access indices that are
           out of bounds for the tuple in "next".
           */
        collected_size = PyTuple_GET_SIZE(collected);
        if (count < 0 || count >= collected_size) {
            PyErr_Format(PyExc_ValueError,
                         "`%.200s.__setstate__` expected that the first "
                         "argument in the `state` (%zd) is not negative and "
                         "smaller than the length of the second argument "
                         "(%zd).",
                         Py_TYPE(self)->tp_name, count, collected_size);
            return NULL;
        }
        /* The length of the "collected" tuple must also be equal to the
           "self->times" attribute.
           */
        if (self->times != collected_size) {
            PyErr_Format(PyExc_ValueError,
                         "`%.200s.__setstate__` expected that the second "
                         "argument in the `state` has a length (%zd) "
                         "equal to the `self->times` (%zd) attribute.",
                         Py_TYPE(self)->tp_name, collected_size, self->times);
            return NULL;
        }
    } else if (collected == Py_None) {
        /* We only expect None if self->times and count is zero. */
        if (count != 0 || self->times != 0) {
            PyErr_Format(PyExc_TypeError,
                         "`%.200s.__setstate__` expected a `tuple` as second "
                         "argument in the `state` when `self->times != 0` or "
                         "the first argument in the `state` is not zero, "
                         "got None",
                         Py_TYPE(self)->tp_name);
            return NULL;
        }
    } else {
        PyErr_Format(PyExc_TypeError,
                     "`%.200s.__setstate__` expected a `tuple` or `None` as "
                     "second argument in the `state`, got %.200s",
                     Py_TYPE(self)->tp_name, Py_TYPE(collected)->tp_name);
        return NULL;
    }

    /* In any case we need to process the "collected" value. In case it is
       "None" we simply set it to NULL. However if it's not None then it's
       a tuple. We process the tuple in the "next" function but it's possible
       that someone still holds a reference to the tuple he passed in. So to
       make sure that we don't mutate tuples that are in use elsewhere we
       create a new tuple here. That also has the additional advantage that
       we can leave the values with index below "count" as NULL. The "next"
       method assumes that it doesn't have to decrement items that it sets so
       this makes sure we don't create a memory leak there.
       */
    if (collected != Py_None) {
        Py_ssize_t i;
        newcollected = PyTuple_New(collected_size);
        if (newcollected == NULL) {
            return NULL;
        }
        for (i=0 ; i < count ; i++) {
            PyObject *tmp = PyTuple_GET_ITEM(collected, i);
            Py_INCREF(tmp);
            PyTuple_SET_ITEM(newcollected, i, tmp);
        }
    } else {
        newcollected = NULL;
    }

    self->count = count;

    /* We already created a new tuple for "collected" or it's None so no need
       to increment the reference count here.
       */
    Py_CLEAR(self->collected);
    self->collected = newcollected;

    Py_RETURN_NONE;
}

/******************************************************************************
 * LengthHint
 *****************************************************************************/

#if PY_MAJOR_VERSION > 3 || (PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 4)
static PyObject *
sideeffects_lengthhint(PyIUObject_Sideeffects *self)
{
    return PyLong_FromSsize_t(PyObject_LengthHint(self->iterator, 0));
}
#endif

/******************************************************************************
 * Methods
 *****************************************************************************/

static PyMethodDef sideeffects_methods[] = {
#if PY_MAJOR_VERSION > 3 || (PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 4)
    {"__length_hint__", (PyCFunction)sideeffects_lengthhint, METH_NOARGS, PYIU_lenhint_doc},
#endif
    {"__reduce__",   (PyCFunction)sideeffects_reduce,   METH_NOARGS, PYIU_reduce_doc},
    {"__setstate__", (PyCFunction)sideeffects_setstate, METH_O,      PYIU_setstate_doc},
    {NULL, NULL}
};

/******************************************************************************
 * Docstring
 *****************************************************************************/

PyDoc_STRVAR(sideeffects_doc, "sideeffects(iterable, func, times=0)\n\
--\n\
\n\
Does a normal iteration over `iterable` and only uses `func` each `times` \n\
items for it's side effects.\n\
\n\
Parameters\n\
----------\n\
iterable : iterable\n\
    `Iterable` containing the elements.\n\
\n\
func : callable\n\
    Function that is called for the side effects.\n\
\n\
times : int, optional\n\
    Call the function each `times` items with the last `times` items. \n\
    If ``0`` the argument for `func` will be the item itself. For any \n\
    number greater than zero the argument will be a tuple.\n\
    Default is ``0``.\n\
\n\
Returns\n\
-------\n\
iterator : generator\n\
    A normal iterator over `iterable`.\n\
\n\
Examples\n\
--------\n\
A simple example::\n\
\n\
    >>> from iteration_utilities import sideeffects\n\
    >>> def printit(val):\n\
    ...     print(val)\n\
    >>> list(sideeffects([1,2,3,4], printit))  # in python3 one could use print directly\n\
    1\n\
    2\n\
    3\n\
    4\n\
    [1, 2, 3, 4]\n\
    >>> list(sideeffects([1,2,3,4,5], printit, 2))\n\
    (1, 2)\n\
    (3, 4)\n\
    (5,)\n\
    [1, 2, 3, 4, 5]\n\
\n\
");

/******************************************************************************
 * Type
 *****************************************************************************/

PyTypeObject PyIUType_Sideeffects = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "iteration_utilities.sideeffects",                  /* tp_name */
    sizeof(PyIUObject_Sideeffects),                     /* tp_basicsize */
    0,                                                  /* tp_itemsize */
    /* methods */
    (destructor)sideeffects_dealloc,                    /* tp_dealloc */
    0,                                                  /* tp_print */
    0,                                                  /* tp_getattr */
    0,                                                  /* tp_setattr */
    0,                                                  /* tp_reserved */
    0,                                                  /* tp_repr */
    0,                                                  /* tp_as_number */
    0,                                                  /* tp_as_sequence */
    0,                                                  /* tp_as_mapping */
    0,                                                  /* tp_hash */
    0,                                                  /* tp_call */
    0,                                                  /* tp_str */
    PyObject_GenericGetAttr,                            /* tp_getattro */
    0,                                                  /* tp_setattro */
    0,                                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,                            /* tp_flags */
    sideeffects_doc,                                    /* tp_doc */
    (traverseproc)sideeffects_traverse,                 /* tp_traverse */
    0,                                                  /* tp_clear */
    0,                                                  /* tp_richcompare */
    0,                                                  /* tp_weaklistoffset */
    PyObject_SelfIter,                                  /* tp_iter */
    (iternextfunc)sideeffects_next,                     /* tp_iternext */
    sideeffects_methods,                                /* tp_methods */
    0,                                                  /* tp_members */
    0,                                                  /* tp_getset */
    0,                                                  /* tp_base */
    0,                                                  /* tp_dict */
    0,                                                  /* tp_descr_get */
    0,                                                  /* tp_descr_set */
    0,                                                  /* tp_dictoffset */
    0,                                                  /* tp_init */
    PyType_GenericAlloc,                                /* tp_alloc */
    sideeffects_new,                                    /* tp_new */
    PyObject_GC_Del,                                    /* tp_free */
};