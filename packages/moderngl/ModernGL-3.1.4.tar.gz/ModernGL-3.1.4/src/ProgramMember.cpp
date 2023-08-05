#include "ProgramMember.hpp"

#include "Error.hpp"

PyObject * MGLProgramMember_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLProgramMember * self = (MGLProgramMember *)type->tp_alloc(type, 0);

	if (self) {
	}

	return (PyObject *)self;
}

void MGLProgramMember_tp_dealloc(MGLProgramMember * self) {
	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLProgramMember_tp_init(MGLProgramMember * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.ProgramMember manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLProgramMember_tp_str(MGLProgramMember * self) {
	return PyUnicode_FromFormat("<ModernGL.ProgramMember>");
}

PyMethodDef MGLProgramMember_tp_methods[] = {
	{0},
};

// MGLProgram * MGLProgramMember_get_program(MGLProgramMember * self, void * closure) {
// 	Py_INCREF(self->program);
// 	return self->program;
// }

// char MGLProgramMember_program_doc[] = R"(
// 	program

// 	The Program object used for creation.
// )";

PyGetSetDef MGLProgramMember_tp_getseters[] = {
	// {(char *)"program", (getter)MGLProgramMember_get_program, 0, MGLProgramMember_program_doc, 0},
	{0},
};

const char * MGLProgramMember_tp_doc = R"(
	ProgramMember
)";

PyTypeObject MGLProgramMember_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.ProgramMember",                               // tp_name
	sizeof(MGLProgramMember),                               // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLProgramMember_tp_dealloc,                // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLProgramMember_tp_str,                      // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLProgramMember_tp_str,                      // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLProgramMember_tp_doc,                                // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLProgramMember_tp_methods,                            // tp_methods
	0,                                                      // tp_members
	MGLProgramMember_tp_getseters,                          // tp_getset
	&MGLObject_Type,                                        // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLProgramMember_tp_init,                     // tp_init
	0,                                                      // tp_alloc
	MGLProgramMember_tp_new,                                // tp_new
};
