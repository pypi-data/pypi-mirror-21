#include "Error.hpp"

#include <cstdarg>

PyObject * MGLError_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLError * self = (MGLError *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLError_tp_new %p\n", self);
	#endif

	if (self) {
		self->dict = 0;
		self->args = 0;
		self->traceback = 0;
		self->context = 0;
		self->cause = 0;
		self->suppress_context = 0;
	}

	return (PyObject *)self;
}

void MGLError_tp_dealloc(MGLError * self) {

	#ifdef MGL_VERBOSE
	printf("MGLError_tp_dealloc %p\n", self);
	#endif

	Py_XDECREF(self->github);

	PyTypeObject * super = Py_TYPE(self)->tp_base;
	return super->tp_dealloc((PyObject *)self);
}

int MGLError_tp_init(MGLError * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Error manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyMethodDef MGLError_tp_methods[] = {
	{0},
};

PyObject * MGLError_get_github(MGLError * self) {
	if (self->github) {
		Py_INCREF(self->github);
		return self->github;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLError_github_doc[] = R"(
	github

	A link to the source code, where the error occurred.
)";

PyGetSetDef MGLError_tp_getseters[] = {
	{(char *)"github", (getter)MGLError_get_github, 0, MGLError_github_doc, 0},
	{0},
};

const char * MGLError_tp_doc = R"(
	Error
)";

PyTypeObject MGLError_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Error",                                       // tp_name
	sizeof(MGLError),                                       // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLError_tp_dealloc,                        // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	0,                                                      // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	0,                                                      // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLError_tp_doc,                                        // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLError_tp_methods,                                    // tp_methods
	0,                                                      // tp_members
	MGLError_tp_getseters,                                  // tp_getset
	(PyTypeObject *)PyExc_Exception,                        // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLError_tp_init,                             // tp_init
	0,                                                      // tp_alloc
	MGLError_tp_new,                                        // tp_new
};

#define GITHUB_URL "https://github.com/cprogrammer1994/ModernGL/blob/master"
#define GITHUB(path) GITHUB_URL path

MGLError * MGLError_New(const char * filename, int line, const char * format, ...) {
	MGLError * self = (MGLError *)MGLError_tp_new(&MGLError_Type, 0, 0);

	va_list va_args;
	va_start(va_args, format);
	self->args = PyTuple_New(1);
	PyObject * message = PyUnicode_FromFormatV(format, va_args);
	PyTuple_SET_ITEM(self->args, 0, message);
	va_end(va_args);

	self->github = PyUnicode_FromFormat(GITHUB("/src/%s#L%d"), filename + 4, line);

	return self;
}

// void MGLError_LinkSource(MGLError * error, const char * filename, int line) {
// }
