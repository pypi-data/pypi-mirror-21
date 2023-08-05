#include "ComputeShader.hpp"

#include "Error.hpp"

PyObject * MGLComputeShader_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLComputeShader * self = (MGLComputeShader *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLComputeShader_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLComputeShader_tp_dealloc(MGLComputeShader * self) {

	#ifdef MGL_VERBOSE
	printf("MGLComputeShader_tp_dealloc %p\n", self);
	#endif

	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLComputeShader_tp_init(MGLComputeShader * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.ComputeShader manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLComputeShader_tp_str(MGLComputeShader * self) {
	return PyUnicode_FromFormat("<ModernGL.ComputeShader>");
}

PyObject * MGLComputeShader_run(MGLComputeShader * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"x", "y", "z", 0};

	int x = 1;
	int y = 1;
	int z = 1;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|iii",
		(char **)kwlist,
		&x,
		&y,
		&z
	);

	if (!args_ok) {
		return 0;
	}

	PyErr_Format(PyExc_NotImplementedError, "Not implemented: %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
	return 0;

	// Py_RETURN_NONE;
}

const char * MGLComputeShader_run_doc = R"(
	run(x = 1, y = 1, z = 1)
)";

PyMethodDef MGLComputeShader_tp_methods[] = {
	{"run", (PyCFunction)MGLComputeShader_run, METH_VARARGS | METH_KEYWORDS, MGLComputeShader_run_doc},
	{0},
};

PyGetSetDef MGLComputeShader_tp_getseters[] = {
	{0},
};

const char * MGLComputeShader_tp_doc = R"(
	ComputeShader
)";

PyTypeObject MGLComputeShader_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.ComputeShader",                               // tp_name
	sizeof(MGLComputeShader),                               // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLComputeShader_tp_dealloc,                // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLComputeShader_tp_str,                      // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLComputeShader_tp_str,                      // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLComputeShader_tp_doc,                                // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLComputeShader_tp_methods,                            // tp_methods
	0,                                                      // tp_members
	MGLComputeShader_tp_getseters,                          // tp_getset
	&MGLContextMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLComputeShader_tp_init,                     // tp_init
	0,                                                      // tp_alloc
	MGLComputeShader_tp_new,                                // tp_new
};

MGLComputeShader * MGLComputeShader_New() {
	MGLComputeShader * self = (MGLComputeShader *)MGLComputeShader_tp_new(&MGLComputeShader_Type, 0, 0);
	return self;
}
