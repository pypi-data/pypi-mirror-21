#include "Shader.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

const int SHADER_TYPE[] = {
	GL_VERTEX_SHADER,
	GL_FRAGMENT_SHADER,
	GL_GEOMETRY_SHADER,
	GL_TESS_EVALUATION_SHADER,
	GL_TESS_CONTROL_SHADER,
};

const char * SHADER_NAME[] = {
	"VertexShader",
	"FragmentShader",
	"GeometryShader",
	"TessEvaluationShader",
	"TessControlShader",
};

const char * SHADER_NAME_UNDERLINE[] = {
	"============",
	"==============",
	"==============",
	"====================",
	"=================",
};

PyObject * MGLShader_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLShader * self = (MGLShader *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLShader_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLShader_tp_dealloc(MGLShader * self) {

	#ifdef MGL_VERBOSE
	printf("MGLShader_tp_dealloc %p\n", self);
	#endif

	MGLShader_Type.tp_free((PyObject *)self);
}

int MGLShader_tp_init(MGLShader * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Shader manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLShader_tp_str(MGLShader * self) {
	return PyUnicode_FromFormat("<ModernGL.Shader>");
}

PyObject * MGLShader_release(MGLShader * self) {
	MGLShader_Invalidate(self);
	Py_RETURN_NONE;
}

PyMethodDef MGLShader_tp_methods[] = {
	{"release", (PyCFunction)MGLShader_release, METH_NOARGS, 0},
	{0},
};

PyObject * MGLShader_get_source(MGLShader * self, void * closure) {
	Py_INCREF(self->source);
	return self->source;
}

char MGLShader_source_doc[] = R"(
	source

	The source code of the shader.
)";

PyObject * MGLShader_get_typename(MGLShader * self, void * closure) {
	return PyUnicode_FromFormat("%s", SHADER_NAME[self->shader_slot]);
}

char MGLShader_typename_doc[] = R"(
	typename

	The type of the shader. The return value is a string.

		- ``'VertexShader'``
		- ``'FragmentShader'``
		- ``'GeometryShader'``
		- ``'TessEvaluationShader'``
		- ``'TessControlShader'``
)";

PyGetSetDef MGLShader_tp_getseters[] = {
	{(char *)"source", (getter)MGLShader_get_source, 0, MGLShader_source_doc, 0},
	{(char *)"typename", (getter)MGLShader_get_typename, 0, MGLShader_typename_doc, 0},
	{0},
};

const char * MGLShader_tp_doc = R"(
	Shader

	Create a :py:class:`~ModernGL.Shader` using:

		- :py:meth:`~ModernGL.Context.VertexShader`
		- :py:meth:`~ModernGL.Context.FragmentShader`
		- :py:meth:`~ModernGL.Context.GeometryShader`
		- :py:meth:`~ModernGL.Context.TessEvaluationShader`
		- :py:meth:`~ModernGL.Context.TessControlShader`
)";

PyTypeObject MGLShader_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Shader",                                      // tp_name
	sizeof(MGLShader),                                      // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLShader_tp_dealloc,                       // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLShader_tp_str,                             // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLShader_tp_str,                             // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLShader_tp_doc,                                       // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLShader_tp_methods,                                   // tp_methods
	0,                                                      // tp_members
	MGLShader_tp_getseters,                                 // tp_getset
	&MGLContextMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLShader_tp_init,                            // tp_init
	0,                                                      // tp_alloc
	MGLShader_tp_new,                                       // tp_new
};

MGLShader * MGLShader_New() {
	MGLShader * self = (MGLShader *)MGLShader_tp_new(&MGLShader_Type, 0, 0);
	return self;
}

void MGLShader_Invalidate(MGLShader * shader) {
	if (Py_TYPE(shader) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLShader_Invalidate %p already released\n", shader);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLShader_Invalidate %p\n", shader);
	#endif

	const GLMethods & gl = shader->context->gl;
	gl.DeleteShader(shader->shader_obj);

	Py_DECREF(shader->source);
	Py_DECREF(shader->context);

	Py_TYPE(shader) = &MGLInvalidObject_Type;

	Py_DECREF(shader);
}

void MGLShader_Compile(MGLShader * shader) {
	const GLMethods & gl = shader->context->gl;

	const char * source = PyUnicode_AsUTF8(shader->source);

	int obj = gl.CreateShader(shader->shader_type);

	gl.ShaderSource(obj, 1, &source, 0);
	gl.CompileShader(obj);

	int compiled = GL_FALSE;
	gl.GetShaderiv(obj, GL_COMPILE_STATUS, &compiled);

	if (!compiled) {
		const char * message = "GLSL Compiler failed";
		const char * title = SHADER_NAME[shader->shader_slot];
		const char * underline = SHADER_NAME_UNDERLINE[shader->shader_slot];

		int log_len = 0;
		gl.GetShaderiv(obj, GL_INFO_LOG_LENGTH, &log_len);

		char * log = new char[log_len];
		gl.GetShaderInfoLog(obj, log_len, &log_len, log);

		gl.DeleteShader(obj);

		MGLError * error = MGLError_New(TRACE, "%s\n\n%s\n%s\n%s\n", message, title, underline, log);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);

		delete[] log;
		return;
	}

	shader->shader_obj = obj;
}
