#include "ProgramStageMember.hpp"

#include "Error.hpp"

PyObject * MGLProgramStageMember_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLProgramStageMember * self = (MGLProgramStageMember *)type->tp_alloc(type, 0);

	if (self) {
	}

	return (PyObject *)self;
}

void MGLProgramStageMember_tp_dealloc(MGLProgramStageMember * self) {
	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLProgramStageMember_tp_init(MGLProgramStageMember * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.ProgramStageMember manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLProgramStageMember_tp_str(MGLProgramStageMember * self) {
	return PyUnicode_FromFormat("<ModernGL.ProgramStageMember>");
}

PyMethodDef MGLProgramStageMember_tp_methods[] = {
	{0},
};

PyGetSetDef MGLProgramStageMember_tp_getseters[] = {
	{0},
};

const char * MGLProgramStageMember_tp_doc = R"(
	ProgramStageMember
)";

PyTypeObject MGLProgramStageMember_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.ProgramStageMember",                          // tp_name
	sizeof(MGLProgramStageMember),                          // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLProgramStageMember_tp_dealloc,           // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLProgramStageMember_tp_str,                 // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLProgramStageMember_tp_str,                 // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLProgramStageMember_tp_doc,                           // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLProgramStageMember_tp_methods,                       // tp_methods
	0,                                                      // tp_members
	MGLProgramStageMember_tp_getseters,                     // tp_getset
	&MGLObject_Type,                                        // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLProgramStageMember_tp_init,                // tp_init
	0,                                                      // tp_alloc
	MGLProgramStageMember_tp_new,                           // tp_new
};
