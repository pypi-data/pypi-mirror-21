#include <Python.h>

#if PY_MAJOR_VERSION >= 3

#define PyBufferProcs_PADDING

#else

// TODO: fix memleak for python2
#define PyUnicode_AsUTF8(obj) PyUnicode_AS_DATA(PyUnicode_AsASCIIString(obj))

#define PyException_HEAD \
	PyObject_HEAD PyObject * dict; \
	PyObject * args; \
	PyObject * traceback; \
	PyObject * context; \
	PyObject * cause; \
	char suppress_context;

#define PyBufferProcs_PADDING 0, 0, 0, 0,

#endif
