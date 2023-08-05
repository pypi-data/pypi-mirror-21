#include "VertexArrayMember.hpp"

#include "Error.hpp"

PyObject * MGLVertexArrayMember_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLVertexArrayMember * self = (MGLVertexArrayMember *)type->tp_alloc(type, 0);

	if (self) {
	}

	return (PyObject *)self;
}

void MGLVertexArrayMember_tp_dealloc(MGLVertexArrayMember * self) {
	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLVertexArrayMember_tp_init(MGLVertexArrayMember * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.VertexArrayMember manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLVertexArrayMember_tp_str(MGLVertexArrayMember * self) {
	return PyUnicode_FromFormat("<ModernGL.VertexArrayMember>");
}

PyMethodDef MGLVertexArrayMember_tp_methods[] = {
	{0},
};

MGLVertexArray * MGLVertexArrayMember_get_vertex_array(MGLVertexArrayMember * self, void * closure) {
	Py_INCREF(self->vertex_array);
	return self->vertex_array;
}

char MGLVertexArrayMember_vertex_array_doc[] = R"(
	vertex_array

	The Program object used for creation.
)";

PyGetSetDef MGLVertexArrayMember_tp_getseters[] = {
	{(char *)"vertex_array", (getter)MGLVertexArrayMember_get_vertex_array, 0, MGLVertexArrayMember_vertex_array_doc, 0},
	{0},
};

const char * MGLVertexArrayMember_tp_doc = R"(
	VertexArrayMember
)";

PyTypeObject MGLVertexArrayMember_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.VertexArrayMember",                           // tp_name
	sizeof(MGLVertexArrayMember),                           // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLVertexArrayMember_tp_dealloc,            // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLVertexArrayMember_tp_str,                  // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLVertexArrayMember_tp_str,                  // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLVertexArrayMember_tp_doc,                            // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLVertexArrayMember_tp_methods,                        // tp_methods
	0,                                                      // tp_members
	MGLVertexArrayMember_tp_getseters,                      // tp_getset
	&MGLObject_Type,                                        // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLVertexArrayMember_tp_init,                 // tp_init
	0,                                                      // tp_alloc
	MGLVertexArrayMember_tp_new,                            // tp_new
};
