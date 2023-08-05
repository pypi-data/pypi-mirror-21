#include "ContextMember.hpp"

#include "Error.hpp"

PyObject * MGLContextMember_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLContextMember * self = (MGLContextMember *)type->tp_alloc(type, 0);

	if (self) {
	}

	return (PyObject *)self;
}

void MGLContextMember_tp_dealloc(MGLContextMember * self) {
	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLContextMember_tp_init(MGLContextMember * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.ContextMember manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLContextMember_tp_str(MGLContextMember * self) {
	return PyUnicode_FromFormat("<ModernGL.ContextMember>");
}

PyMethodDef MGLContextMember_tp_methods[] = {
	{0},
};

MGLContext * MGLContextMember_get_context(MGLContextMember * self, void * closure) {
	Py_INCREF(self->context);
	return self->context;
}

char MGLContextMember_context_doc[] = R"(
	context

	The Context object used for creation.
)";

PyGetSetDef MGLContextMember_tp_getseters[] = {
	{(char *)"context", (getter)MGLContextMember_get_context, 0, MGLContextMember_context_doc, 0},
	{0},
};

const char * MGLContextMember_tp_doc = R"(
	ContextMember
)";

PyTypeObject MGLContextMember_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.ContextMember",                               // tp_name
	sizeof(MGLContextMember),                               // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLContextMember_tp_dealloc,                // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLContextMember_tp_str,                      // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLContextMember_tp_str,                      // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLContextMember_tp_doc,                                // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLContextMember_tp_methods,                            // tp_methods
	0,                                                      // tp_members
	MGLContextMember_tp_getseters,                          // tp_getset
	&MGLObject_Type,                                        // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLContextMember_tp_init,                     // tp_init
	0,                                                      // tp_alloc
	MGLContextMember_tp_new,                                // tp_new
};
