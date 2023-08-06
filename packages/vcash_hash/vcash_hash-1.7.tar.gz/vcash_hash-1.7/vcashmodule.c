#include <Python.h>

#include "vcashhash.h"

static PyObject *blake_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    if (!PyArg_ParseTuple(args, "S", &input))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    blake_hash((char *)PyBytes_AsString((PyObject*) input), output);
#else
    blake_hash((char *)PyString_AsString((PyObject*) input), output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, 32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyObject *whirlpoolx_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    if (!PyArg_ParseTuple(args, "S", &input))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    whirlpoolx_hash((char *)PyBytes_AsString((PyObject*) input), output);
#else
    whirlpoolx_hash((char *)PyString_AsString((PyObject*) input), output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, 32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyMethodDef VcashMethods[] = {
    { "getBlakePoWHash", blake_getpowhash, METH_VARARGS, "Returns the proof of work hash using blake hash" },
    { "getWhirlpoolxPoWHash", whirlpoolx_getpowhash, METH_VARARGS, "Returns the proof of work hash using whirlpoolx hash" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef VcashModule = {
    PyModuleDef_HEAD_INIT,
    "vcash_hash",
    "...",
    -1,
    VcashMethods
};

PyMODINIT_FUNC PyInit_vcash_hash(void) {
    return PyModule_Create(&VcashModule);
}

#else

PyMODINIT_FUNC initvcash_hash(void) {
    (void) Py_InitModule("vcash_hash", VcashMethods);
}
#endif
