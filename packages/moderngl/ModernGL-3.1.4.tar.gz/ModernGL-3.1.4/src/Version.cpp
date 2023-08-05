#include "Version.hpp"

#include "Error.hpp"

PyObject * MGLVersion_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLVersion * self = (MGLVersion *)type->tp_alloc(type, 0);

	// #ifdef MGL_VERBOSE
	// printf("MGLVersion_tp_new %p\n", self);
	// #endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLVersion_tp_dealloc(MGLVersion * self) {

	// #ifdef MGL_VERBOSE
	// printf("MGLVersion_tp_dealloc %p\n", self);
	// #endif

	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLVersion_tp_init(MGLVersion * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Version manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLVersion_tp_str(MGLVersion * self) {
	return PyUnicode_FromFormat("<Version: %d.%d>", self->major, self->minor);
}

PyMethodDef MGLVersion_tp_methods[] = {
	{0},
};

PyObject * MGLVersion_get_major(MGLVersion * self, void * closure) {
	return PyLong_FromLong(self->major);
}

char MGLVersion_major_doc[] = R"(
	major

	The major
)";

PyObject * MGLVersion_get_minor(MGLVersion * self, void * closure) {
	return PyLong_FromLong(self->minor);
}

char MGLVersion_minor_doc[] = R"(
	minor

	The minor
)";

PyGetSetDef MGLVersion_tp_getseters[] = {
	{(char *)"major", (getter)MGLVersion_get_major, 0, MGLVersion_major_doc, 0},
	{(char *)"minor", (getter)MGLVersion_get_minor, 0, MGLVersion_minor_doc, 0},
	{0},
};

const char * MGLVersion_tp_doc = R"(
	Version

	OpenGL version.
)";

PyTypeObject MGLVersion_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Version",                                     // tp_name
	sizeof(MGLVersion),                                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLVersion_tp_dealloc,                      // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLVersion_tp_str,                            // tp_repr
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
	MGLVersion_tp_doc,                                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLVersion_tp_methods,                                  // tp_methods
	0,                                                      // tp_members
	MGLVersion_tp_getseters,                                // tp_getset
	&MGLObject_Type,                                        // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLVersion_tp_init,                           // tp_init
	0,                                                      // tp_alloc
	MGLVersion_tp_new,                                      // tp_new
};

MGLVersion * MGLVersion_New() {
	MGLVersion * self = (MGLVersion *)MGLVersion_tp_new(&MGLVersion_Type, 0, 0);
	return self;
}
