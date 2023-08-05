#include "MultisampleTexture.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

PyObject * MGLMultisampleTexture_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLMultisampleTexture * self = (MGLMultisampleTexture *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLMultisampleTexture_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLMultisampleTexture_tp_dealloc(MGLMultisampleTexture * self) {

	#ifdef MGL_VERBOSE
	printf("MGLMultisampleTexture_tp_dealloc %p\n", self);
	#endif

	MGLMultisampleTexture_Type.tp_free((PyObject *)self);
}

int MGLMultisampleTexture_tp_init(MGLMultisampleTexture * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.MultisampleTexture manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLMultisampleTexture_tp_str(MGLMultisampleTexture * self) {
	return PyUnicode_FromFormat("<ModernGL.MultisampleTexture>");
}

PyObject * MGLMultisampleTexture_use(MGLMultisampleTexture * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"index", 0};

	int index = 0;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|I",
		(char **)kwlist,
		&index
	);

	if (!args_ok) {
		return 0;
	}

	const GLMethods & gl = self->context->gl;
	gl.ActiveTexture(GL_TEXTURE0 + index);
	gl.BindTexture(GL_TEXTURE_2D_MULTISAMPLE, self->texture_obj);

	Py_RETURN_NONE;
}

const char * MGLMultisampleTexture_use_doc = R"(
	use(index = 0)

	Args:
		optional index: The texture location.
			Same as the integer value that is used for sampler2D uniforms in the shaders.
			The value ``0`` will bind the texture to the ``GL_TEXTURE0`` binding point.

	Returns:
		:py:data:`None`
)";

PyObject * MGLMultisampleTexture_release(MGLMultisampleTexture * self) {
	MGLMultisampleTexture_Invalidate(self);
	Py_RETURN_NONE;
}

const char * MGLMultisampleTexture_release_doc = R"(
	release()

	Release the texture.
)";

PyMethodDef MGLMultisampleTexture_tp_methods[] = {
	{"use", (PyCFunction)MGLMultisampleTexture_use, METH_VARARGS | METH_KEYWORDS, MGLMultisampleTexture_use_doc},
	{"release", (PyCFunction)MGLMultisampleTexture_release, METH_NOARGS, MGLMultisampleTexture_release_doc},
	{0},
};

PyGetSetDef MGLMultisampleTexture_tp_getseters[] = {
	{0},
};

const char * MGLMultisampleTexture_tp_doc = R"(
	MultisampleTexture
)";

PyTypeObject MGLMultisampleTexture_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.MultisampleTexture",                          // tp_name
	sizeof(MGLMultisampleTexture),                          // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLMultisampleTexture_tp_dealloc,           // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLMultisampleTexture_tp_str,                 // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLMultisampleTexture_tp_str,                 // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLMultisampleTexture_tp_doc,                           // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLMultisampleTexture_tp_methods,                       // tp_methods
	0,                                                      // tp_members
	MGLMultisampleTexture_tp_getseters,                     // tp_getset
	&MGLFramebufferAttachment_Type,                         // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLMultisampleTexture_tp_init,                // tp_init
	0,                                                      // tp_alloc
	MGLMultisampleTexture_tp_new,                           // tp_new
};

MGLMultisampleTexture * MGLMultisampleTexture_New() {
	MGLMultisampleTexture * self = (MGLMultisampleTexture *)MGLMultisampleTexture_tp_new(&MGLMultisampleTexture_Type, 0, 0);
	return self;
}

void MGLMultisampleTexture_Invalidate(MGLMultisampleTexture * texture) {
	if (Py_TYPE(texture) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLMultisampleTexture_Invalidate %p already released\n", texture);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLMultisampleTexture_Invalidate %p\n", texture);
	#endif

	texture->context->gl.DeleteTextures(1, (GLuint *)&texture->texture_obj);

	Py_DECREF(texture->context);

	Py_TYPE(texture) = &MGLInvalidObject_Type;

	Py_DECREF(texture);
}
