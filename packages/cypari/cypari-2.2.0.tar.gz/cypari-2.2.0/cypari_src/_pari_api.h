/* Generated by Cython 0.25.2 */

#ifndef __PYX_HAVE_API__cypari_src___pari
#define __PYX_HAVE_API__cypari_src___pari
#include "Python.h"
#include "_pari.h"

static cysigs_t *__pyx_api_vp_10cypari_src_5_pari_cysigs = 0;
#define cysigs (*__pyx_api_vp_10cypari_src_5_pari_cysigs)
#if !defined(__Pyx_PyIdentifier_FromString)
#if PY_MAJOR_VERSION < 3
  #define __Pyx_PyIdentifier_FromString(s) PyString_FromString(s)
#else
  #define __Pyx_PyIdentifier_FromString(s) PyUnicode_FromString(s)
#endif
#endif

#ifndef __PYX_HAVE_RT_ImportModule
#define __PYX_HAVE_RT_ImportModule
static PyObject *__Pyx_ImportModule(const char *name) {
    PyObject *py_name = 0;
    PyObject *py_module = 0;
    py_name = __Pyx_PyIdentifier_FromString(name);
    if (!py_name)
        goto bad;
    py_module = PyImport_Import(py_name);
    Py_DECREF(py_name);
    return py_module;
bad:
    Py_XDECREF(py_name);
    return 0;
}
#endif

#ifndef __PYX_HAVE_RT_ImportVoidPtr
#define __PYX_HAVE_RT_ImportVoidPtr
static int __Pyx_ImportVoidPtr(PyObject *module, const char *name, void **p, const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    d = PyObject_GetAttrString(module, (char *)"__pyx_capi__");
    if (!d)
        goto bad;
    cobj = PyDict_GetItemString(d, name);
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%.200s does not export expected C variable %.200s",
                PyModule_GetName(module), name);
        goto bad;
    }
#if PY_VERSION_HEX >= 0x02070000
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C variable %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), name, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    *p = PyCapsule_GetPointer(cobj, sig);
#else
    {const char *desc, *s1, *s2;
    desc = (const char *)PyCObject_GetDesc(cobj);
    if (!desc)
        goto bad;
    s1 = desc; s2 = sig;
    while (*s1 != '\0' && *s1 == *s2) { s1++; s2++; }
    if (*s1 != *s2) {
        PyErr_Format(PyExc_TypeError,
            "C variable %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), name, sig, desc);
        goto bad;
    }
    *p = PyCObject_AsVoidPtr(cobj);}
#endif
    if (!(*p))
        goto bad;
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(d);
    return -1;
}
#endif


static int import_cypari_src___pari(void) {
  PyObject *module = 0;
  module = __Pyx_ImportModule("cypari_src._pari");
  if (!module) goto bad;
  if (__Pyx_ImportVoidPtr(module, "cysigs", (void **)&__pyx_api_vp_10cypari_src_5_pari_cysigs, "cysigs_t") < 0) goto bad;
  Py_DECREF(module); module = 0;
  return 0;
  bad:
  Py_XDECREF(module);
  return -1;
}

#endif /* !__PYX_HAVE_API__cypari_src___pari */
