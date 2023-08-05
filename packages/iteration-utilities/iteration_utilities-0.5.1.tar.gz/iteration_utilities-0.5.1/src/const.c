/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE.rst
 *****************************************************************************/

typedef struct {
    PyObject_HEAD
    PyObject *item;
} PyIUObject_Constant;

PyTypeObject PyIUType_Constant;

/******************************************************************************
 * New
 *****************************************************************************/

static PyObject *
constant_new(PyTypeObject *type,
             PyObject *args,
             PyObject *kwargs)
{
    PyIUObject_Constant *self;

    PyObject *item;

    /* Parse arguments */
    if (!PyArg_UnpackTuple(args, "constant", 1, 1, &item)) {
        return NULL;
    }

    /* Create struct */
    self = (PyIUObject_Constant *)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }
    Py_INCREF(item);
    self->item = item;
    return (PyObject *)self;
}

/******************************************************************************
 * Destructor
 *****************************************************************************/

static void
constant_dealloc(PyIUObject_Constant *self)
{
    PyObject_GC_UnTrack(self);
    Py_XDECREF(self->item);
    Py_TYPE(self)->tp_free(self);
}

/******************************************************************************
 * Traverse
 *****************************************************************************/

static int
constant_traverse(PyIUObject_Constant *self,
                  visitproc visit,
                  void *arg)
{
    Py_VISIT(self->item);
    return 0;
}

/******************************************************************************
 * Call
 *****************************************************************************/

static PyObject *
constant_call(PyIUObject_Constant *self,
              PyObject *args,
              PyObject *kwargs)
{
    Py_INCREF(self->item);
    return self->item;
}

/******************************************************************************
 * Repr
 *****************************************************************************/

static PyObject *
constant_repr(PyIUObject_Constant *self)
{
    PyObject *result = NULL;
    int ok;

    ok = Py_ReprEnter((PyObject *)self);
    if (ok != 0) {
        return ok > 0 ? PyUnicode_FromString("...") : NULL;
    }

    result = PyUnicode_FromFormat("%s(%R)",
                                  Py_TYPE(self)->tp_name,
                                  self->item);

    Py_ReprLeave((PyObject *)self);
    return result;
}

/******************************************************************************
 * Reduce
 *****************************************************************************/

static PyObject *
constant_reduce(PyIUObject_Constant *self,
                PyObject *unused)
{
    return Py_BuildValue("O(O)", Py_TYPE(self), self->item);
}

/******************************************************************************
 * Methods
 *****************************************************************************/

static PyMethodDef constant_methods[] = {
    {"__reduce__", (PyCFunction)constant_reduce, METH_NOARGS, PYIU_reduce_doc},
    {NULL, NULL}
};

/******************************************************************************
 * Docstring
 *****************************************************************************/

PyDoc_STRVAR(constant_doc, "constant(x)\n\
--\n\
\n\
Class that always returns `x` when called.\n\
\n\
Parameters\n\
----------\n\
x : any type\n\
    The item that should be returned when called. Positional only parameter.\n\
\n\
Methods\n\
-------\n\
__call__(\\*args, \\*\\*kwargs)\n\
    Returns `x`.\n\
\n\
Examples\n\
--------\n\
Creating `const` instances::\n\
\n\
    >>> from iteration_utilities import constant\n\
    >>> five = constant(5)\n\
    >>> five()\n\
    5\n\
    >>> ten = constant(10)\n\
    >>> # Any parameters are ignored\n\
    >>> ten(5, give_me=100)\n\
    10\n\
\n\
There are already three predefined instances:\n\
\n\
- ``return_True`` : always returns `True`.\n\
- ``return_False`` : always returns `False`.\n\
- ``return_None`` : always returns `None`.\n\
\n\
For example::\n\
\n\
    >>> from iteration_utilities import return_True, return_False, return_None\n\
    >>> return_True()\n\
    True\n\
    >>> return_False()\n\
    False\n\
    >>> return_None()\n\
    >>> return_None() is None\n\
    True");

/******************************************************************************
 * Type
 *****************************************************************************/

PyTypeObject PyIUType_Constant = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "iteration_utilities.constant",                     /* tp_name */
    sizeof(PyIUObject_Constant),                        /* tp_basicsize */
    0,                                                  /* tp_itemsize */
    /* methods */
    (destructor)constant_dealloc,                       /* tp_dealloc */
    0,                                                  /* tp_print */
    0,                                                  /* tp_getattr */
    0,                                                  /* tp_setattr */
    0,                                                  /* tp_reserved */
    (reprfunc)constant_repr,                            /* tp_repr */
    0,                                                  /* tp_as_number */
    0,                                                  /* tp_as_sequence */
    0,                                                  /* tp_as_mapping */
    0,                                                  /* tp_hash */
    (ternaryfunc)constant_call,                         /* tp_call */
    0,                                                  /* tp_str */
    PyObject_GenericGetAttr,                            /* tp_getattro */
    0,                                                  /* tp_setattro */
    0,                                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,                            /* tp_flags */
    constant_doc,                                       /* tp_doc */
    (traverseproc)constant_traverse,                    /* tp_traverse */
    0,                                                  /* tp_clear */
    0,                                                  /* tp_richcompare */
    0,                                                  /* tp_weaklistoffset */
    0,                                                  /* tp_iter */
    0,                                                  /* tp_iternext */
    constant_methods,                                   /* tp_methods */
    0,                                                  /* tp_members */
    0,                                                  /* tp_getset */
    0,                                                  /* tp_base */
    0,                                                  /* tp_dict */
    0,                                                  /* tp_descr_get */
    0,                                                  /* tp_descr_set */
    0,                                                  /* tp_dictoffset */
    0,                                                  /* tp_init */
    0,                                                  /* tp_alloc */
    constant_new,                                       /* tp_new */
    PyObject_GC_Del,                                    /* tp_free */
};
