#include "Object.hpp"

#include "Error.hpp"

PyObject * MGLObject_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLObject * self = (MGLObject *)type->tp_alloc(type, 0);

	if (self) {
	}

	return (PyObject *)self;
}

void MGLObject_tp_dealloc(MGLObject * self) {
	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLObject_tp_init(MGLObject * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Object manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLObject_tp_str(MGLObject * self) {
	return PyUnicode_FromFormat("<ModernGL.Object>");
}

PyMethodDef MGLObject_tp_methods[] = {
	{0},
};

PyGetSetDef MGLObject_tp_getseters[] = {
	{0},
};

const char * MGLObject_tp_doc = R"(
	Object

	ModernGL objects.
)";

PyTypeObject MGLObject_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Object",                                      // tp_name
	sizeof(MGLObject),                                      // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLObject_tp_dealloc,                       // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLObject_tp_str,                             // tp_repr
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
	MGLObject_tp_doc,                                       // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLObject_tp_methods,                                   // tp_methods
	0,                                                      // tp_members
	MGLObject_tp_getseters,                                 // tp_getset
	0,                                                      // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLObject_tp_init,                            // tp_init
	0,                                                      // tp_alloc
	MGLObject_tp_new,                                       // tp_new
};
