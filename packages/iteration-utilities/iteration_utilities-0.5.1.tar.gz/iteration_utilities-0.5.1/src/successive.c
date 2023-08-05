/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE.rst
 *****************************************************************************/

typedef struct {
    PyObject_HEAD
    PyObject *iterator;
    Py_ssize_t times;
    PyObject *result;
} PyIUObject_Successive;

PyTypeObject PyIUType_Successive;

/******************************************************************************
 * New
 *****************************************************************************/

static PyObject *
successive_new(PyTypeObject *type,
               PyObject *args,
               PyObject *kwargs)
{
    static char *kwlist[] = {"iterable", "times", NULL};
    PyIUObject_Successive *self;

    PyObject *iterable;
    PyObject *iterator = NULL;
    Py_ssize_t times = 2;

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|n:successive", kwlist,
                                     &iterable, &times)) {
        goto Fail;
    }
    if (times <= 0) {
        PyErr_Format(PyExc_ValueError,
                     "times must be greater than 0.");
        goto Fail;
    }

    /* Create and fill struct */
    iterator = PyObject_GetIter(iterable);
    if (iterator == NULL) {
        goto Fail;
    }
    self = (PyIUObject_Successive *)type->tp_alloc(type, 0);
    if (self == NULL) {
        goto Fail;
    }
    self->iterator = iterator;
    self->times = times;
    self->result = NULL;
    return (PyObject *)self;

Fail:
    Py_XDECREF(iterator);
    return NULL;
}

/******************************************************************************
 * Destructor
 *****************************************************************************/

static void
successive_dealloc(PyIUObject_Successive *self)
{
    PyObject_GC_UnTrack(self);
    Py_XDECREF(self->iterator);
    Py_XDECREF(self->result);
    Py_TYPE(self)->tp_free(self);
}

/******************************************************************************
 * Traverse
 *****************************************************************************/

static int
successive_traverse(PyIUObject_Successive *self,
                    visitproc visit,
                    void *arg)
{
    Py_VISIT(self->iterator);
    Py_VISIT(self->result);
    return 0;
}

/******************************************************************************
 * Next
 *****************************************************************************/

static PyObject *
successive_next(PyIUObject_Successive *self)
{
    PyObject *result = self->result;
    PyObject *newresult, *item, *olditem, *temp=NULL;
    Py_ssize_t i;

    /* First call needs to create a tuple for the result. */
    if (result == NULL) {
        result = PyTuple_New(self->times);
        if (result == NULL) {
            return NULL;
        }

        for (i=0; i<self->times; i++) {
            item = (*Py_TYPE(self->iterator)->tp_iternext)(self->iterator);
            if (item == NULL) {
                Py_DECREF(result);
                return NULL;
            }
            PyTuple_SET_ITEM(result, i, item);
        }
        Py_INCREF(result);
        self->result = result;
        return result;
    }

    /* After the first element we can use the normal procedure. */
    item = (*Py_TYPE(self->iterator)->tp_iternext)(self->iterator);
    if (item == NULL) {
        return NULL;
    }

    /* Recycle old tuple or create a new one. */
    if (Py_REFCNT(result) == 1) {

        /* Remove the first item of the result. */
        temp = PyTuple_GET_ITEM(result, 0);
        PyIU_TupleRemove(result, 0, self->times);
        Py_XDECREF(temp);

        /* Insert the new item (at the end) and return it. */
        PyTuple_SET_ITEM(result, self->times-1, item);
        Py_INCREF(result);
        return result;

    } else {
        newresult = PyTuple_New(self->times);
        if (newresult == NULL) {
            Py_DECREF(item);
            return NULL;
        }

        /* Shift all earlier items one index to the left. */
        for (i=1 ; i < self->times ; i++) {
            olditem = PyTuple_GET_ITEM(result, i);
            Py_INCREF(olditem);
            PyTuple_SET_ITEM(newresult, i-1, olditem);
        }
        /* Insert the new item (at the end), then replace the saved result. */
        PyTuple_SET_ITEM(newresult, self->times-1, item);
        Py_INCREF(newresult);
        self->result = newresult;
        Py_DECREF(result);
        return newresult;
    }
}

/******************************************************************************
 * Reduce
 *****************************************************************************/

static PyObject *
successive_reduce(PyIUObject_Successive *self)
{
    /* Seperate cases depending on the status of "result". We use and modify
       it in next. It is copied in next when the refcount isn't 1, so we
       don't need to copy it for reduce. However using "reduce" a lot will
       definetly slow the function down. But it does not matter if the slowdown
       is in "next" or "reduce". :)
       */
    if (self->result == NULL) {
        return Py_BuildValue("O(On)", Py_TYPE(self),
                             self->iterator,
                             self->times);
    } else {
        return Py_BuildValue("O(On)(O)", Py_TYPE(self),
                             self->iterator,
                             self->times,
                             self->result);
    }
}

/******************************************************************************
 * Setstate
 *****************************************************************************/

static PyObject *
successive_setstate(PyIUObject_Successive *self,
                    PyObject *state)
{
    PyObject *result;

    if (!PyTuple_Check(state)) {
        PyErr_Format(PyExc_TypeError,
                     "`%.200s.__setstate__` expected a `tuple`-like argument"
                     ", got `%.200s` instead.",
                     Py_TYPE(self)->tp_name, Py_TYPE(state)->tp_name);
        return NULL;
    }

    if (!PyArg_ParseTuple(state, "O:successive.__setstate__", &result)) {
        return NULL;
    }

    /* The result must be a tuple, otherwise we could risk segfaults (because
       "next" use PyTuple_GET_ITEM). It also needs to have the same size as
       "self->times" otherwise the for-loop in "next" could go beyond the
       tuple-size (again risking undefined behaviour).
       */
    if (!PyTuple_CheckExact(result)) {
        PyErr_Format(PyExc_TypeError,
                     "`%.200s.__setstate__` expected a `tuple` instance as "
                     "first argument in the `state`, got %.200s.",
                     Py_TYPE(self)->tp_name, Py_TYPE(result)->tp_name);
        return NULL;
    }
    if (PyTuple_GET_SIZE(result) != self->times) {
        PyErr_Format(PyExc_ValueError,
                     "`%.200s.__setstate__` expected that the first argument "
                     "in the `state`, satisfies `len(firstarg) == self->times`. "
                     "But `%zd != %zd`.",
                     Py_TYPE(self)->tp_name,
                     PyTuple_GET_SIZE(result),
                     self->times);
        return NULL;
    }

    /* No need to  copy the "result". If it has a refcount different from
       1 it will be copied in "next" before it is mutated.
       */

    Py_CLEAR(self->result);
    self->result = result;
    Py_XINCREF(result);

    Py_RETURN_NONE;
}

/******************************************************************************
 * LengthHint
 *****************************************************************************/

#if PY_MAJOR_VERSION > 3 || (PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 4)
static PyObject *
successive_lengthhint(PyIUObject_Successive *self)
{
    Py_ssize_t len = 0;
    if (self->result == NULL) {
        len = (PyObject_LengthHint(self->iterator, 0) - self->times) + 1;
    } else {
        len = PyObject_LengthHint(self->iterator, 0);
    }

    if (len < 0) {
        len = 0;
    }

    return PyLong_FromSsize_t(len);
}
#endif

/******************************************************************************
 * Methods
 *****************************************************************************/

static PyMethodDef successive_methods[] = {
#if PY_MAJOR_VERSION > 3 || (PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 4)
    {"__length_hint__", (PyCFunction)successive_lengthhint, METH_NOARGS, PYIU_lenhint_doc},
#endif
    {"__reduce__",   (PyCFunction)successive_reduce,   METH_NOARGS, PYIU_reduce_doc},
    {"__setstate__", (PyCFunction)successive_setstate, METH_O,      PYIU_setstate_doc},
    {NULL, NULL}
};

/******************************************************************************
 * Docstring
 *****************************************************************************/

PyDoc_STRVAR(successive_doc, "successive(iterable, times=2)\n\
--\n\
\n\
Like the recipe for pairwise but allows to get an arbitary number\n\
of successive elements.\n\
\n\
Parameters\n\
----------\n\
iterable : iterable\n\
    Get the successive elements from this `iterable`.\n\
\n\
times : integer, optional\n\
    The number of successive elements.\n\
    Default is ``2``.\n\
\n\
Returns\n\
-------\n\
successive_elements : generator\n\
    The successive elements as generator. Each element of the generator\n\
    is a tuple containing `times` successive elements.\n\
\n\
Examples\n\
--------\n\
Each item of the `iterable` is returned as ``tuple`` with `times` successive\n\
items::\n\
\n\
    >>> from iteration_utilities import successive\n\
    >>> list(successive(range(5)))\n\
    [(0, 1), (1, 2), (2, 3), (3, 4)]\n\
\n\
Varying the `times` can give you also 3 successive elements::\n\
\n\
    >>> list(successive(range(5), times=3))\n\
    [(0, 1, 2), (1, 2, 3), (2, 3, 4)]\n\
    >>> list(successive('Hello!', times=2))\n\
    [('H', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o'), ('o', '!')]");

/******************************************************************************
 * Type
 *****************************************************************************/

PyTypeObject PyIUType_Successive = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "iteration_utilities.successive",                   /* tp_name */
    sizeof(PyIUObject_Successive),                      /* tp_basicsize */
    0,                                                  /* tp_itemsize */
    /* methods */
    (destructor)successive_dealloc,                     /* tp_dealloc */
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
    successive_doc,                                     /* tp_doc */
    (traverseproc)successive_traverse,                  /* tp_traverse */
    0,                                                  /* tp_clear */
    0,                                                  /* tp_richcompare */
    0,                                                  /* tp_weaklistoffset */
    PyObject_SelfIter,                                  /* tp_iter */
    (iternextfunc)successive_next,                      /* tp_iternext */
    successive_methods,                                 /* tp_methods */
    0,                                                  /* tp_members */
    0,                                                  /* tp_getset */
    0,                                                  /* tp_base */
    0,                                                  /* tp_dict */
    0,                                                  /* tp_descr_get */
    0,                                                  /* tp_descr_set */
    0,                                                  /* tp_dictoffset */
    0,                                                  /* tp_init */
    PyType_GenericAlloc,                                /* tp_alloc */
    successive_new,                                     /* tp_new */
    PyObject_GC_Del,                                    /* tp_free */
};