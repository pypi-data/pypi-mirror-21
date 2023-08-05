#include "Framebuffer.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"
#include "Renderbuffer.hpp"
#include "Texture.hpp"

PyObject * MGLFramebuffer_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLFramebuffer * self = (MGLFramebuffer *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLFramebuffer_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLFramebuffer_tp_dealloc(MGLFramebuffer * self) {

	#ifdef MGL_VERBOSE
	printf("MGLFramebuffer_tp_dealloc %p\n", self);
	#endif

	MGLFramebuffer_Type.tp_free((PyObject *)self);
}

int MGLFramebuffer_tp_init(MGLFramebuffer * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Framebuffer manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLFramebuffer_tp_str(MGLFramebuffer * self) {
	return PyUnicode_FromFormat("<ModernGL.Framebuffer>");
}

PyObject * MGLFramebuffer_release(MGLFramebuffer * self) {
	MGLFramebuffer_Invalidate(self);
	Py_RETURN_NONE;
}

const char * MGLFramebuffer_release_doc = R"(
	release()

	Release the framebuffer.
)";

PyObject * MGLFramebuffer_read(MGLFramebuffer * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"size", "origin", "components", "floats", 0};

	int width;
	int height;
	int origin_x = 0;
	int origin_y = 0;
	int components = 4;
	int floats = false;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"(II)|(II)$Ip",
		(char **)kwlist,
		&width,
		&height,
		&origin_x,
		&origin_y,
		&components,
		&floats
	);

	if (!args_ok) {
		return 0;
	}

	int size = floats ? (width * height * components * 4) : (height * ((width * components + 3) & ~3));
	int type = floats ? GL_FLOAT : GL_UNSIGNED_BYTE;

	const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};
	int format = formats[components];

	PyObject * result = PyBytes_FromStringAndSize(0, size);
	char * data = PyBytes_AS_STRING(result);
	self->context->gl.ReadPixels(origin_x, origin_y, width, height, format, type, data);
	return result;
}

const char * MGLFramebuffer_read_doc = R"(
	read()
)";

PyObject * MGLFramebuffer_use(MGLFramebuffer * self) {
	self->context->gl.BindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_obj);
	Py_RETURN_NONE;
}

const char * MGLFramebuffer_use_doc = R"(
	use()

	Bind the framebuffer. Set the target for the :py:func:`~VertexArray.render` or :py:func:`~VertexArray.transform` methods.
)";

PyMethodDef MGLFramebuffer_tp_methods[] = {
	{"release", (PyCFunction)MGLFramebuffer_release, METH_NOARGS, MGLFramebuffer_release_doc},
	{"read", (PyCFunction)MGLFramebuffer_read, METH_VARARGS | METH_KEYWORDS, MGLFramebuffer_read_doc},
	{"use", (PyCFunction)MGLFramebuffer_use, METH_NOARGS, MGLFramebuffer_use_doc},
	{0},
};

PyObject * MGLFramebuffer_get_color_attachments(MGLFramebuffer * self, void * closure) {
	if (self->color_attachments) {
		Py_INCREF(self->color_attachments);
		return self->color_attachments;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLFramebuffer_color_attachments_doc[] = R"(
)";

PyObject * MGLFramebuffer_get_depth_attachment(MGLFramebuffer * self, void * closure) {
	if (self->depth_attachment) {
		Py_INCREF(self->depth_attachment);
		return self->depth_attachment;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLFramebuffer_depth_attachment_doc[] = R"(
)";

PyGetSetDef MGLFramebuffer_tp_getseters[] = {
	{(char *)"color_attachments", (getter)MGLFramebuffer_get_color_attachments, 0, MGLFramebuffer_color_attachments_doc, 0},
	{(char *)"depth_attachment", (getter)MGLFramebuffer_get_depth_attachment, 0, MGLFramebuffer_depth_attachment_doc, 0},
	{0},
};

const char * MGLFramebuffer_tp_doc = R"(
	Framebuffer
)";

PyTypeObject MGLFramebuffer_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Framebuffer",                                 // tp_name
	sizeof(MGLFramebuffer),                                 // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLFramebuffer_tp_dealloc,                  // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLFramebuffer_tp_str,                        // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLFramebuffer_tp_str,                        // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLFramebuffer_tp_doc,                                  // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLFramebuffer_tp_methods,                              // tp_methods
	0,                                                      // tp_members
	MGLFramebuffer_tp_getseters,                            // tp_getset
	&MGLContextMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLFramebuffer_tp_init,                       // tp_init
	0,                                                      // tp_alloc
	MGLFramebuffer_tp_new,                                  // tp_new
};

MGLFramebuffer * MGLFramebuffer_New() {
	MGLFramebuffer * self = (MGLFramebuffer *)MGLFramebuffer_tp_new(&MGLFramebuffer_Type, 0, 0);
	return self;
}

void MGLFramebuffer_Invalidate(MGLFramebuffer * framebuffer) {
	if (Py_TYPE(framebuffer) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLFramebuffer_Invalidate %p already released\n", framebuffer);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLFramebuffer_Invalidate %p\n", framebuffer);
	#endif

	if (framebuffer->framebuffer_obj) {
		framebuffer->context->gl.DeleteFramebuffers(1, (GLuint *)&framebuffer->framebuffer_obj);

		if (framebuffer->color_attachments) {
			int color_attachments_len = (int)PyList_GET_SIZE(framebuffer->color_attachments);

			for (int i = 0; i < color_attachments_len; ++i) {
				PyObject * attachment = PyList_GET_ITEM(framebuffer->color_attachments, i);

				if (Py_TYPE(attachment) == &MGLTexture_Type) {
					MGLTexture * texture = (MGLTexture *)attachment;
					if (Py_REFCNT(texture) == 2) {
						MGLTexture_Invalidate(texture);
					}
				} else if (Py_TYPE(attachment) == &MGLRenderbuffer_Type) {
					MGLRenderbuffer * renderbuffer = (MGLRenderbuffer *)attachment;
					if (Py_REFCNT(renderbuffer) == 2) {
						MGLRenderbuffer_Invalidate(renderbuffer);
					}
				}
			}

			Py_DECREF(framebuffer->color_attachments);
		}

		if (framebuffer->depth_attachment) {
			if (Py_TYPE(framebuffer->depth_attachment) == &MGLTexture_Type) {
				MGLTexture * texture = (MGLTexture *)framebuffer->depth_attachment;
				if (Py_REFCNT(texture) == 2) {
					MGLTexture_Invalidate(texture);
				}
			} else if (Py_TYPE(framebuffer->depth_attachment) == &MGLRenderbuffer_Type) {
				MGLRenderbuffer * renderbuffer = (MGLRenderbuffer *)framebuffer->depth_attachment;
				if (Py_REFCNT(renderbuffer) == 2) {
					MGLRenderbuffer_Invalidate(renderbuffer);
				}
			}

			Py_DECREF(framebuffer->depth_attachment);
		}

		Py_DECREF(framebuffer->context);
	}

	Py_TYPE(framebuffer) = &MGLInvalidObject_Type;

	Py_DECREF(framebuffer);
}
