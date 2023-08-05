#include "Renderbuffer.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

PyObject * MGLRenderbuffer_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLRenderbuffer * self = (MGLRenderbuffer *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLRenderbuffer_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLRenderbuffer_tp_dealloc(MGLRenderbuffer * self) {

	#ifdef MGL_VERBOSE
	printf("MGLRenderbuffer_tp_dealloc %p\n", self);
	#endif

	MGLRenderbuffer_Type.tp_free((PyObject *)self);
}

int MGLRenderbuffer_tp_init(MGLRenderbuffer * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Renderbuffer manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLRenderbuffer_tp_str(MGLRenderbuffer * self) {
	return PyUnicode_FromFormat("<ModernGL.Renderbuffer>");
}

PyObject * MGLRenderbuffer_release(MGLRenderbuffer * self) {
	MGLRenderbuffer_Invalidate(self);
	Py_RETURN_NONE;
}

const char * MGLRenderbuffer_release_doc = R"(
	release()

	Release the renderbuffer.
)";

PyMethodDef MGLRenderbuffer_tp_methods[] = {
	{"release", (PyCFunction)MGLRenderbuffer_release, METH_NOARGS, MGLRenderbuffer_release_doc},
	{0},
};

PyGetSetDef MGLRenderbuffer_tp_getseters[] = {
	{0},
};

const char * MGLRenderbuffer_tp_doc = R"(
	Renderbuffer
)";

PyTypeObject MGLRenderbuffer_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Renderbuffer",                                // tp_name
	sizeof(MGLRenderbuffer),                                // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLRenderbuffer_tp_dealloc,                 // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLRenderbuffer_tp_str,                       // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLRenderbuffer_tp_str,                       // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLRenderbuffer_tp_doc,                                 // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLRenderbuffer_tp_methods,                             // tp_methods
	0,                                                      // tp_members
	MGLRenderbuffer_tp_getseters,                           // tp_getset
	&MGLFramebufferAttachment_Type,                         // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLRenderbuffer_tp_init,                      // tp_init
	0,                                                      // tp_alloc
	MGLRenderbuffer_tp_new,                                 // tp_new
};

MGLRenderbuffer * MGLRenderbuffer_New() {
	MGLRenderbuffer * self = (MGLRenderbuffer *)MGLRenderbuffer_tp_new(&MGLRenderbuffer_Type, 0, 0);
	return self;
}

void MGLRenderbuffer_Invalidate(MGLRenderbuffer * renderbuffer) {
	if (Py_TYPE(renderbuffer) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLRenderbuffer_Invalidate %p already released\n", renderbuffer);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLRenderbuffer_Invalidate %p\n", renderbuffer);
	#endif

	renderbuffer->context->gl.DeleteRenderbuffers(1, (GLuint *)&renderbuffer->renderbuffer_obj);

	Py_DECREF(renderbuffer->context);

	Py_TYPE(renderbuffer) = &MGLInvalidObject_Type;

	Py_DECREF(renderbuffer);
}
