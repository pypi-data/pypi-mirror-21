#include "SubroutineUniform.hpp"

#include "Error.hpp"

PyObject * MGLSubroutineUniform_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLSubroutineUniform * self = (MGLSubroutineUniform *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLSubroutineUniform_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLSubroutineUniform_tp_dealloc(MGLSubroutineUniform * self) {

	#ifdef MGL_VERBOSE
	printf("MGLSubroutineUniform_tp_dealloc %p\n", self);
	#endif

	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLSubroutineUniform_tp_init(MGLSubroutineUniform * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.SubroutineUniform manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLSubroutineUniform_tp_str(MGLSubroutineUniform * self) {
	return PyUnicode_FromFormat("<ModernGL.SubroutineUniform>");
}

PyMethodDef MGLSubroutineUniform_tp_methods[] = {
	{0},
};

PyGetSetDef MGLSubroutineUniform_tp_getseters[] = {
	{0},
};

const char * MGLSubroutineUniform_tp_doc = R"(
	SubroutineUniform
)";

PyTypeObject MGLSubroutineUniform_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.SubroutineUniform",                           // tp_name
	sizeof(MGLSubroutineUniform),                           // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLSubroutineUniform_tp_dealloc,            // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLSubroutineUniform_tp_str,                  // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLSubroutineUniform_tp_str,                  // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLSubroutineUniform_tp_doc,                            // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLSubroutineUniform_tp_methods,                        // tp_methods
	0,                                                      // tp_members
	MGLSubroutineUniform_tp_getseters,                      // tp_getset
	&MGLProgramStageMember_Type,                            // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLSubroutineUniform_tp_init,                 // tp_init
	0,                                                      // tp_alloc
	MGLSubroutineUniform_tp_new,                            // tp_new
};

MGLSubroutineUniform * MGLSubroutineUniform_New() {
	MGLSubroutineUniform * self = (MGLSubroutineUniform *)MGLSubroutineUniform_tp_new(&MGLSubroutineUniform_Type, 0, 0);
	return self;
}

void MGLSubroutineUniform_Complete(MGLSubroutineUniform * subroutine_uniform) {
}
