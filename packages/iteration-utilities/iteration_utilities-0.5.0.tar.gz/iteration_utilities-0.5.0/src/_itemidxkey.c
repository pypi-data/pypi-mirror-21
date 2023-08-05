/******************************************************************************
 * Licensed under Apache License Version 2.0 - see LICENSE.rst
 *
 * Helper class that mimics a 2-tuple when compared but dynamically decides
 * which item to compare (item or key) and assumes that the idx is always
 * different.
 *
 * It also has a constructor function that bypasses the args/kwargs unpacking
 * to allow faster creation from within C code.
 *****************************************************************************/

typedef struct {
    PyObject_HEAD
    PyObject *item;
    PyObject *key;
    Py_ssize_t idx;
} PyIUObject_ItemIdxKey;

PyTypeObject PyIUType_ItemIdxKey;

#define PyIU_ItemIdxKey_Check(obj) PyObject_IsInstance(obj, (PyObject*) &PyIUType_ItemIdxKey)
#define PyIU_ItemIdxKey_CheckExact(op) (Py_TYPE(op) == &PyIUType_ItemIdxKey)

/******************************************************************************
 * New
 *****************************************************************************/

static PyObject *
itemidxkey_new(PyTypeObject *type,
               PyObject *args,
               PyObject *kwargs)
{
    static char *kwlist[] = {"item", "idx", "key", NULL};
    PyIUObject_ItemIdxKey *self;

    PyObject *item, *key=NULL;
    Py_ssize_t idx;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "On|O:ItemIdxKey", kwlist,
                                     &item, &idx, &key)) {
        return NULL;
    }
    if (PyIU_ItemIdxKey_Check(item)) {
        PyErr_Format(PyExc_TypeError, "cannot use `ItemIdxKey` instance as `item`.");
        return NULL;
    }
    if (key != NULL && PyIU_ItemIdxKey_Check(key)) {
        PyErr_Format(PyExc_TypeError, "cannot use `ItemIdxKey` instance as `key`.");
        return NULL;
    }

    self = (PyIUObject_ItemIdxKey *)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }
    Py_INCREF(item);
    Py_XINCREF(key);
    self->item = item;
    self->idx = idx;
    self->key = key;

    return (PyObject *)self;
}

/******************************************************************************
 * New (only from C code)
 *
 * This bypasses the argument unpacking!
 *****************************************************************************/

PyObject *
PyIU_ItemIdxKey_FromC(PyObject *item,
                      Py_ssize_t idx,
                      PyObject *key)
{
    /* STEALS REFERENCES!!! */
    PyIUObject_ItemIdxKey *self;
    /* Verifing the inputs could be done but the API isn't exported and it
       should never be NULL we can neglect this check for the sake of
       performance:
    if (item == NULL) {
        PyErr_Format(PyExc_TypeError, "`item` must be given.");
        return NULL;
    }
    */
    /* Create and fill new ItemIdxKey. */
    self = PyObject_GC_New(PyIUObject_ItemIdxKey, &PyIUType_ItemIdxKey);
    if (self == NULL) {
        return NULL;
    }
    self->item = item;
    self->idx = idx;
    self->key = key;
    PyObject_GC_Track(self);
    return (PyObject *)self;
}

/******************************************************************************
 *
 * Copy (only from C code)
 *
 *****************************************************************************/

PyObject *
PyIU_ItemIdxKey_Copy(PyObject *iik)
{
    PyIUObject_ItemIdxKey *n;
    PyIUObject_ItemIdxKey *o = (PyIUObject_ItemIdxKey *)iik;

    n = PyObject_GC_New(PyIUObject_ItemIdxKey, &PyIUType_ItemIdxKey);
    if (n == NULL) {
        return NULL;
    }
    Py_INCREF(o->item);
    n->item = o->item;
    n->idx = o->idx;
    Py_XINCREF(o->key);
    n->key = o->key;
    PyObject_GC_Track(n);
    return (PyObject *)n;
}

/******************************************************************************
 * Destructor
 *****************************************************************************/

static void
itemidxkey_dealloc(PyIUObject_ItemIdxKey *self)
{
    Py_XDECREF(self->item);
    Py_XDECREF(self->key);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

/******************************************************************************
 * Traverse
 *****************************************************************************/

static int
itemidxkey_traverse(PyIUObject_ItemIdxKey *self,
                    visitproc visit,
                    void *arg)
{
    Py_VISIT(self->item);
    Py_VISIT(self->key);
    return 0;
}

/******************************************************************************
 * Representation
 *****************************************************************************/

static PyObject *
itemidxkey_repr(PyIUObject_ItemIdxKey *self)
{
    PyObject *repr;
    int ok;

    ok = Py_ReprEnter((PyObject*)self);
    if (ok != 0) {
        return ok > 0 ? PyUnicode_FromString("...") : NULL;
    }

    if (self->key == NULL) {
        repr = PyUnicode_FromFormat("%s(item=%R, idx=%zd)",
                                    Py_TYPE(self)->tp_name,
                                    self->item, self->idx);
    } else {
        /* The representation of the item could modify/delete the key and then
           the representation of the key could segfault. Better to make the key
           undeletable as long as PyUnicode_FromFormat runs.
           */
        PyObject *tmpkey = self->key;
        Py_INCREF(tmpkey);
        repr = PyUnicode_FromFormat("%s(item=%R, idx=%zd, key=%R)",
                                    Py_TYPE(self)->tp_name,
                                    self->item, self->idx, tmpkey);
        Py_DECREF(tmpkey);
    }
    Py_ReprLeave((PyObject *)self);
    return repr;
}

/******************************************************************************
 * Richcompare
 *****************************************************************************/


int
PyIU_ItemIdxKey_Compare(PyObject *v,
                        PyObject *w,
                        int op)
{
    /* Several assumptions in here:
       - That the objects are actually PyIUObject_ItemIdxKey objects.
       - That no other operator than > or < is going here.
       */
    PyObject *item1, *item2;
    PyIUObject_ItemIdxKey *l, *r;

    l = (PyIUObject_ItemIdxKey *)v;
    r = (PyIUObject_ItemIdxKey *)w;

    /* Compare items if key is NULL otherwise compare keys. */
    if (l->key == NULL) {
        item1 = l->item;
        item2 = r->item;
    } else {
        item1 = l->key;
        item2 = r->key;
    }

    /* The order to check for equality and lt makes a huge performance
       difference:
       - lots of duplicates: first eq then "op"
       - no/few duplicates: first "op" then eq
       - first compare idx and if it's smaller check le/ge otherwise lt/gt

       --> I chose eq then "op" but the other version is also avaiable as
       comment. */

    if (l->idx < r->idx) {
        op = (op == Py_LT) ? Py_LE : Py_GE;
    }
    return PyObject_RichCompareBool(item1, item2, op);

    /* First eq then "op" : Better if there are lots of duplicates! Worse if
                            there are few or None!
    */
    /*
    ok = PyObject_RichCompareBool(item1, item2, Py_EQ);
    if (ok == -1) {
        return NULL;
    } else if (ok == 1) {
        if (l->idx < r->idx) {
            Py_RETURN_TRUE;
        } else {
            Py_RETURN_FALSE;
        }
    } else {
        ok = PyObject_RichCompareBool(item1, item2, op);
        if (ok == -1) {
            return NULL;
        } else if (ok == 0) {
            Py_RETURN_FALSE;
        } else {
            Py_RETURN_TRUE;
        }
    }
    */

    /* First "op" then eq : Better if there are almost no duplicates! Worse if
                            there are lots!
    */
    /*
    ok = PyObject_RichCompareBool(item1, item2, op);
    if (ok == 1) {
        Py_RETURN_TRUE;
    } else if (ok == 0) {
        ok = PyObject_RichCompareBool(item1, item2, Py_EQ);
        if (ok == 1) {
            if (l->idx < r->idx) {
                Py_RETURN_TRUE;
            } else {
                Py_RETURN_FALSE;
            }
        } else if (ok == 0) {
            Py_RETURN_FALSE;
        } else {
            return NULL;
        }
    } else {
        return NULL;
    }
    */

    /* First compare idx and then compare the other elements.
    */
    /*
    if (l->idx < r->idx) {
        op = (op == Py_LT) ? Py_LE : Py_GE;
    }
    ok = PyObject_RichCompareBool(item1, item2, op);
    if (ok == 1) {
        Py_RETURN_TRUE;
    } else if (ok == 0) {
        Py_RETURN_FALSE;
    } else {
        return NULL;
    }
    */
}


static PyObject *
itemidxkey_richcompare(PyObject *v,
                       PyObject *w,
                       int op)
{
    int ok;

    /* Only allow < and > for now */
    switch (op) {
        case Py_LT: break;
        case Py_GT: break;
        default: Py_RETURN_NOTIMPLEMENTED;
    }
    /* only allow ItemIdxKey to be compared. */
    if (!PyIU_ItemIdxKey_Check(v) || !PyIU_ItemIdxKey_Check(w))
        Py_RETURN_NOTIMPLEMENTED;

    ok = PyIU_ItemIdxKey_Compare(v, w, op);
    if (ok == 1) {
        Py_RETURN_TRUE;
    } else if (ok == 0) {
        Py_RETURN_FALSE;
    } else {
        return NULL;
    }
}

/******************************************************************************
 * item Property
 *****************************************************************************/

static PyObject *
itemidxkey_getitem(PyIUObject_ItemIdxKey *self,
                   void *closure)
{
    Py_INCREF(self->item);
    return self->item;
}

static int
itemidxkey_setitem(PyIUObject_ItemIdxKey *self,
                   PyObject *o,
                   void *closure)
{
    if (o == NULL) {
        PyErr_Format(PyExc_TypeError, "cannot delete `item`.");
        return -1;
    } else if (PyIU_ItemIdxKey_Check(o)) {
        PyErr_Format(PyExc_TypeError, "cannot use `ItemIdxKey` instance as `item`.");
        return -1;
    }
    Py_DECREF(self->item);
    Py_INCREF(o);
    self->item = o;
    return 0;
}

/******************************************************************************
 * idx Property
 *****************************************************************************/

static PyObject *
itemidxkey_getidx(PyIUObject_ItemIdxKey *self,
                  void *closure)
{
    #if PY_MAJOR_VERSION == 2
        return PyInt_FromSsize_t(self->idx);
    #else
        return PyLong_FromSsize_t(self->idx);
    #endif
}

static int
itemidxkey_setidx(PyIUObject_ItemIdxKey *self,
                  PyObject *o,
                  void *closure)
{
    Py_ssize_t idx;
    if (o == NULL) {
        PyErr_Format(PyExc_TypeError, "cannot delete `idx`.");
        return -1;
    }
    #if PY_MAJOR_VERSION == 2
    if (PyInt_Check(o)) {
        idx = PyInt_AsSsize_t(o);
    } else
    #endif
    if (PyLong_Check(o)) {
        idx = PyLong_AsSsize_t(o);
    } else {
        PyErr_Format(PyExc_TypeError, "an integer is required.");
        return -1;
    }

    if (PyErr_Occurred()) {
        return -1;
    }

    self->idx = idx;
    return 0;
}

/******************************************************************************
 * key Property
 *****************************************************************************/

static PyObject *
itemidxkey_getkey(PyIUObject_ItemIdxKey *self,
                  void *closure)
{
    if (self->key == NULL) {
        Py_RETURN_NONE;
    }
    Py_INCREF(self->key);
    return self->key;
}

static int
itemidxkey_setkey(PyIUObject_ItemIdxKey *self,
                  PyObject *o,
                  void *closure)
{
    if (o != NULL && PyIU_ItemIdxKey_Check(o)) {
        PyErr_Format(PyExc_TypeError, "cannot use `ItemIdxKey` instance as `key`.");
        return -1;
    }
    Py_XDECREF(self->key);
    Py_XINCREF(o);
    self->key = o;
    return 0;
}

/******************************************************************************
 * Properties
 *****************************************************************************/

static PyGetSetDef itemidxkey_getsetlist[] = {
    {"item", (getter)itemidxkey_getitem, (setter)itemidxkey_setitem, NULL},
    {"idx",  (getter)itemidxkey_getidx,  (setter)itemidxkey_setidx,  NULL},
    {"key",  (getter)itemidxkey_getkey,  (setter)itemidxkey_setkey,  NULL},
    {NULL}
};

/******************************************************************************
 * Reduce
 *****************************************************************************/

static PyObject *
itemidxkey_reduce(PyIUObject_ItemIdxKey *self)
{
    if (self->key == NULL) {
        return Py_BuildValue("O(On)", Py_TYPE(self),
                             self->item, self->idx);
    } else {
        return Py_BuildValue("O(OnO)", Py_TYPE(self),
                             self->item, self->idx, self->key);
    }
}

/******************************************************************************
 * Methods
 *****************************************************************************/

static PyMethodDef itemidxkey_methods[] = {
    {"__reduce__",   (PyCFunction)itemidxkey_reduce,   METH_NOARGS, PYIU_reduce_doc},
    {NULL, NULL}
};

/******************************************************************************
 * Docstring
 *****************************************************************************/

PyDoc_STRVAR(itemidxkey_doc, "ItemIdxKey(item, idx, /, key)\n\
--\n\
\n\
Helper class that makes it easier and faster to compare two values for\n\
*stable* sorting algorithms supporting key functions.\n\
\n\
Parameters\n\
----------\n\
item : any type\n\
    The original `item`.\n\
\n\
idx : number\n\
    The position (index) of the `item`.\n\
\n\
key : any type, optional\n\
    If given (even as ``None``) this should be the `item` processed by the \n\
    `key` function. If it is set then comparisons will compare the `key` \n\
    instead of the `item`.\n\
\n\
Attributes\n\
----------\n\
item : any type\n\
    The `item` to sort.\n\
idx : integer\n\
    The original position of the `item`.\n\
key : any type\n\
    The result of a key function applied to the `item`.\n\
\n\
Notes\n\
-----\n\
Comparisons involving `ItemIdxKey` have some limitations:\n\
\n\
- Both have to be `ItemIdxKey` instances.\n\
- If the first operand has no `key` then the `items` are compared.\n\
- The `idx` must be different.\n\
- only ``<`` and ``>`` are supported!\n\
\n\
The implementation is rougly like:\n\
\n\
.. code::\n\
\n\
   _notgiven = object()\n\
   \n\
   class ItemIdxKey(object):\n\
       def __init__(self, item, idx, key=_notgiven):\n\
           self.item = item\n\
           self.idx = idx\n\
           self.key = key\n\
   \n\
       def __lt__(self, other):\n\
           if type(other) != ItemIdxKey:\n\
               raise TypeError()\n\
           if self.key is _notgiven:\n\
               item1, item2 = self.item, other.item\n\
           else:\n\
               item1, item2 = self.key, other.key\n\
           if self.idx < other.idx:\n\
               return item1 <= item2\n\
           else:\n\
               return item1 < item2\n\
   \n\
       def __gt__(self, other):\n\
           if type(other) != ItemIdxKey:\n\
               raise TypeError()\n\
           if self.key is _notgiven:\n\
               item1, item2 = self.item, other.item\n\
           else:\n\
               item1, item2 = self.key, other.key\n\
           if self.idx < other.idx:\n\
               return item1 >= item2\n\
           else:\n\
               return item1 > item2\n\
\n\
.. note::\n\
   The actual C makes the initialization and comparisons several times faster\n\
   than the above illustrated Python class! But it's only slightly faster\n\
   than comparing `tuple` or `list`. If you do not plan to support `reverse`\n\
   or `key` then there is no need to use this class!\n\
\n\
.. warning::\n\
   You should **never** insert a `ItemIdxKey` instance as `item` or `key` in\n\
   another `ItemIdxKey` instance. This would yield false results and breaks\n\
   your computer! (the latter might not be true.)\n\
\n\
Examples\n\
--------\n\
Stability is one of the distinct features of sorting algorithms. This class\n\
aids in supporting those algorithms which allow `reverse` and `key`.\n\
This means that comparisons require absolute lesser (or greater if `reverse`)\n\
if the `idx` is bigger but only require lesser or equal (or greater or equal)\n\
if the `idx` is smaller. This class implements exactly these conditions::\n\
\n\
    >>> # Use < for normal sorting.\n\
    >>> ItemIdxKey(10, 2) < ItemIdxKey(10, 3)\n\
    True\n\
    >>> # and > for reverse sorting.\n\
    >>> ItemIdxKey(10, 2) > ItemIdxKey(10, 3)\n\
    True\n\
\n\
The result may seem surprising but if the `item` (or `key`) is equal then\n\
in either normal or `reverse` sorting the one with the smaller `idx` should\n\
come first! If the `items` (or `keys`) differ they take precedence.\n\
\n\
    >>> ItemIdxKey(10, 2) < ItemIdxKey(11, 3)\n\
    True\n\
    >>> ItemIdxKey(10, 2) > ItemIdxKey(11, 3)\n\
    False\n\
\n\
But it compares the `key` instead of the `item` if it's given::\n\
\n\
    >>> ItemIdxKey(0, 2, 20) < ItemIdxKey(10, 3, 19)\n\
    False\n\
    >>> ItemIdxKey(0, 2, 20) > ItemIdxKey(10, 3, 19)\n\
    True\n\
\n\
This allows to sort based on `item` or `key` but always to access the `item`\n\
for the value that should be sorted.");


/******************************************************************************
 * Type
 *****************************************************************************/

PyTypeObject PyIUType_ItemIdxKey = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "iteration_utilities.ItemIdxKey",                   /* tp_name */
    sizeof(PyIUObject_ItemIdxKey),                      /* tp_basicsize */
    0,                                                  /* tp_itemsize */
    /* methods */
    (destructor)itemidxkey_dealloc,                     /* tp_dealloc */
    0,                                                  /* tp_print */
    0,                                                  /* tp_getattr */
    0,                                                  /* tp_setattr */
    0,                                                  /* tp_reserved */
    (reprfunc)itemidxkey_repr,                          /* tp_repr */
    0,                                                  /* tp_as_number */
    0,                                                  /* tp_as_sequence */
    0,                                                  /* tp_as_mapping */
    0,                                                  /* tp_hash  */
    0,                                                  /* tp_call */
    0,                                                  /* tp_str */
    0,                                                  /* tp_getattro */
    0,                                                  /* tp_setattro */
    0,                                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,                            /* tp_flags */
    itemidxkey_doc,                                     /* tp_doc */
    (traverseproc)itemidxkey_traverse,                  /* tp_traverse */
    0,                                                  /* tp_clear */
    itemidxkey_richcompare,                             /* tp_richcompare */
    0,                                                  /* tp_weaklistoffset */
    0,                                                  /* tp_iter */
    0,                                                  /* tp_iternext */
    itemidxkey_methods,                                 /* tp_methods */
    0,                                                  /* tp_members */
    itemidxkey_getsetlist,                              /* tp_getset */
    0,                                                  /* tp_base */
    0,                                                  /* tp_dict */
    0,                                                  /* tp_descr_get */
    0,                                                  /* tp_descr_set */
    0,                                                  /* tp_dictoffset */
    0,                                                  /* tp_init */
    0,                                                  /* tp_alloc */
    itemidxkey_new,                                     /* tp_new */
    PyObject_GC_Del,                                    /* tp_free */
};
