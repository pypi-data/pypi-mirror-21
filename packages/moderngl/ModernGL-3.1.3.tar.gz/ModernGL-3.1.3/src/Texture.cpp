#include "Texture.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

PyObject * MGLTexture_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLTexture * self = (MGLTexture *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLTexture_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLTexture_tp_dealloc(MGLTexture * self) {

	#ifdef MGL_VERBOSE
	printf("MGLTexture_tp_dealloc %p\n", self);
	#endif

	MGLTexture_Type.tp_free((PyObject *)self);
}

int MGLTexture_tp_init(MGLTexture * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Texture manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLTexture_tp_str(MGLTexture * self) {
	return PyUnicode_FromFormat("<ModernGL.Texture>");
}

PyObject * MGLTexture_use(MGLTexture * self, PyObject * args, PyObject * kwargs) {
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
	gl.BindTexture(GL_TEXTURE_2D, self->texture_obj);

	Py_RETURN_NONE;
}

const char * MGLTexture_use_doc = R"(
	use(index = 0)

	Args:
		optional index: The texture location.
			Same as the integer value that is used for sampler2D uniforms in the shaders.
			The value ``0`` will bind the texture to the ``GL_TEXTURE0`` binding point.

	Returns:
		:py:data:`None`
)";

PyObject * MGLTexture_release(MGLTexture * self) {
	MGLTexture_Invalidate(self);
	Py_RETURN_NONE;
}

const char * MGLTexture_release_doc = R"(
	release()

	Release the texture.
)";

PyMethodDef MGLTexture_tp_methods[] = {
	{"use", (PyCFunction)MGLTexture_use, METH_VARARGS | METH_KEYWORDS, MGLTexture_use_doc},
	{"release", (PyCFunction)MGLTexture_release, METH_NOARGS, MGLTexture_release_doc},
	{0},
};

PyObject * MGLTexture_get_width(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->width);
}

char MGLTexture_width_doc[] = R"(
	width

	The width
)";

PyObject * MGLTexture_get_height(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->height);
}

char MGLTexture_height_doc[] = R"(
	height

	The height
)";

PyObject * MGLTexture_get_size(MGLTexture * self, void * closure) {
	return PyTuple_Pack(2, PyLong_FromLong(self->width), PyLong_FromLong(self->height));
}

char MGLTexture_size_doc[] = R"(
	size

	The size
)";

PyGetSetDef MGLTexture_tp_getseters[] = {
	{(char *)"width", (getter)MGLTexture_get_width, 0, MGLTexture_width_doc, 0},
	{(char *)"height", (getter)MGLTexture_get_height, 0, MGLTexture_height_doc, 0},
	{(char *)"size", (getter)MGLTexture_get_size, 0, MGLTexture_size_doc, 0},
	{0},
};

const char * MGLTexture_tp_doc = R"(
	Texture
)";

PyTypeObject MGLTexture_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Texture",                                     // tp_name
	sizeof(MGLTexture),                                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLTexture_tp_dealloc,                      // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLTexture_tp_str,                            // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLTexture_tp_str,                            // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLTexture_tp_doc,                                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLTexture_tp_methods,                                  // tp_methods
	0,                                                      // tp_members
	MGLTexture_tp_getseters,                                // tp_getset
	&MGLFramebufferAttachment_Type,                         // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLTexture_tp_init,                           // tp_init
	0,                                                      // tp_alloc
	MGLTexture_tp_new,                                      // tp_new
};

MGLTexture * MGLTexture_New() {
	MGLTexture * self = (MGLTexture *)MGLTexture_tp_new(&MGLTexture_Type, 0, 0);
	return self;
}

void MGLTexture_Invalidate(MGLTexture * texture) {
	if (Py_TYPE(texture) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLTexture_Invalidate %p already released\n", texture);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLTexture_Invalidate %p\n", texture);
	#endif

	texture->context->gl.DeleteTextures(1, (GLuint *)&texture->texture_obj);

	Py_DECREF(texture->context);

	Py_TYPE(texture) = &MGLInvalidObject_Type;

	Py_DECREF(texture);
}
