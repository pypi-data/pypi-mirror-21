#include "MultisampleRenderbuffer.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

PyObject * MGLMultisampleRenderbuffer_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLMultisampleRenderbuffer * self = (MGLMultisampleRenderbuffer *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLMultisampleRenderbuffer_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLMultisampleRenderbuffer_tp_dealloc(MGLMultisampleRenderbuffer * self) {

	#ifdef MGL_VERBOSE
	printf("MGLMultisampleRenderbuffer_tp_dealloc %p\n", self);
	#endif

	MGLMultisampleRenderbuffer_Type.tp_free((PyObject *)self);
}

int MGLMultisampleRenderbuffer_tp_init(MGLMultisampleRenderbuffer * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.MultisampleRenderbuffer manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLMultisampleRenderbuffer_tp_str(MGLMultisampleRenderbuffer * self) {
	return PyUnicode_FromFormat("<ModernGL.MultisampleRenderbuffer>");
}

PyObject * MGLMultisampleRenderbuffer_release(MGLMultisampleRenderbuffer * self) {
	MGLMultisampleRenderbuffer_Invalidate(self);
	Py_RETURN_NONE;
}

const char * MGLMultisampleRenderbuffer_release_doc = R"(
	release()

	Release the renderbuffer.
)";

PyMethodDef MGLMultisampleRenderbuffer_tp_methods[] = {
	{"release", (PyCFunction)MGLMultisampleRenderbuffer_release, METH_NOARGS, MGLMultisampleRenderbuffer_release_doc},
	{0},
};

PyGetSetDef MGLMultisampleRenderbuffer_tp_getseters[] = {
	{0},
};

const char * MGLMultisampleRenderbuffer_tp_doc = R"(
	MultisampleRenderbuffer
)";

PyTypeObject MGLMultisampleRenderbuffer_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.MultisampleRenderbuffer",                     // tp_name
	sizeof(MGLMultisampleRenderbuffer),                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLMultisampleRenderbuffer_tp_dealloc,      // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLMultisampleRenderbuffer_tp_str,            // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLMultisampleRenderbuffer_tp_str,            // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLMultisampleRenderbuffer_tp_doc,                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLMultisampleRenderbuffer_tp_methods,                  // tp_methods
	0,                                                      // tp_members
	MGLMultisampleRenderbuffer_tp_getseters,                // tp_getset
	&MGLFramebufferAttachment_Type,                         // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLMultisampleRenderbuffer_tp_init,           // tp_init
	0,                                                      // tp_alloc
	MGLMultisampleRenderbuffer_tp_new,                      // tp_new
};

MGLMultisampleRenderbuffer * MGLMultisampleRenderbuffer_New() {
	MGLMultisampleRenderbuffer * self = (MGLMultisampleRenderbuffer *)MGLMultisampleRenderbuffer_tp_new(&MGLMultisampleRenderbuffer_Type, 0, 0);
	return self;
}

void MGLMultisampleRenderbuffer_Invalidate(MGLMultisampleRenderbuffer * renderbuffer) {
	if (Py_TYPE(renderbuffer) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLMultisampleRenderbuffer_Invalidate %p already released\n", renderbuffer);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLMultisampleRenderbuffer_Invalidate %p\n", renderbuffer);
	#endif

	renderbuffer->context->gl.DeleteRenderbuffers(1, (GLuint *)&renderbuffer->renderbuffer_obj);

	Py_DECREF(renderbuffer->context);

	Py_TYPE(renderbuffer) = &MGLInvalidObject_Type;

	Py_DECREF(renderbuffer);
}
