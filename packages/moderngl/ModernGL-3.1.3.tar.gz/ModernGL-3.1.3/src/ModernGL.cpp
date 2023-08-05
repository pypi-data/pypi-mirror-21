#include "Attribute.hpp"
#include "Buffer.hpp"
#include "BufferAccess.hpp"
#include "ComputeShader.hpp"
#include "Context.hpp"
#include "ContextMember.hpp"
#include "EnableFlag.hpp"
#include "Error.hpp"
#include "Framebuffer.hpp"
#include "FramebufferAttachment.hpp"
#include "InvalidObject.hpp"
#include "MultisampleRenderbuffer.hpp"
#include "MultisampleTexture.hpp"
#include "Object.hpp"
#include "Primitive.hpp"
#include "Program.hpp"
#include "ProgramMember.hpp"
#include "ProgramStage.hpp"
#include "ProgramStageMember.hpp"
#include "Renderbuffer.hpp"
#include "Shader.hpp"
#include "Subroutine.hpp"
#include "SubroutineUniform.hpp"
#include "Texture.hpp"
#include "Uniform.hpp"
#include "UniformBlock.hpp"
#include "Varying.hpp"
#include "Version.hpp"
#include "VertexArray.hpp"
#include "VertexArrayAttribute.hpp"
#include "VertexArrayListAttribute.hpp"
#include "VertexArrayMatrixAttribute.hpp"
#include "VertexArrayMember.hpp"

#include "GLContext.hpp"

MGLContext * create_standalone_context(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"size", "require", 0};

	int width = 256;
	int height = 256;

	MGLVersion * require = (MGLVersion *)Py_None;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|(II)$O",
		(char **)kwlist,
		&width,
		&height,
		&require
	);

	if (!args_ok) {
		return 0;
	}

	if (require != (MGLVersion *)Py_None && Py_TYPE(require) != &MGLVersion_Type) {
		MGLError * error = MGLError_New(TRACE, "require must be a ModernGL.Version not %s", Py_TYPE(require)->tp_name);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	MGLContext * ctx = MGLContext_New();

	ctx->gl_context = CreateGLContext();

	if (PyErr_Occurred()) {
		return 0;
	}

	MGLContext_Initialize(ctx);

	if (PyErr_Occurred()) {
		return 0;
	}

	return ctx;
}

const char * create_standalone_context_doc = R"(
	create_standalone_context(require = None)

	Keyword Arguments:
		require (version): OpenGL version.

	Returns:
		:py:class:`ModernGL.Context`
)";

MGLContext * create_context(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"require", 0};

	MGLVersion * require = (MGLVersion *)Py_None;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|$O",
		(char **)kwlist,
		&require
	);

	if (!args_ok) {
		return 0;
	}

	if (require != (MGLVersion *)Py_None && Py_TYPE(require) != &MGLVersion_Type) {
		MGLError * error = MGLError_New(TRACE, "require must be a ModernGL.Version not %s", Py_TYPE(require)->tp_name);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	MGLContext * ctx = MGLContext_New();

	ctx->gl_context = LoadCurrentGLContext();

	if (PyErr_Occurred()) {
		return 0;
	}

	MGLContext_Initialize(ctx);

	if (PyErr_Occurred()) {
		return 0;
	}

	Py_INCREF(ctx);

	return ctx;
}

const char * create_context_doc = R"(
	create_context(require = None)

	Keyword Arguments:
		require (version): OpenGL version.

	Returns:
		:py:class:`ModernGL.Context`
)";

PyMethodDef MGL_module_methods[] = {
	{"create_standalone_context", (PyCFunction)create_standalone_context, METH_VARARGS | METH_KEYWORDS, create_standalone_context_doc},
	{"create_context", (PyCFunction)create_context, METH_VARARGS | METH_KEYWORDS, create_context_doc},
	{0},
};

const char * MGL_module_doc = R"(
	ModernGL
)";

bool MGL_InitializeModule(PyObject * module) {
	{
		if (PyType_Ready(&MGLAttribute_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Attribute in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLAttribute_Type);

		PyModule_AddObject(module, "Attribute", (PyObject *)&MGLAttribute_Type);
	}

	{
		if (PyType_Ready(&MGLBuffer_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Buffer in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLBuffer_Type);

		PyModule_AddObject(module, "Buffer", (PyObject *)&MGLBuffer_Type);
	}

	{
		if (PyType_Ready(&MGLBufferAccess_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register BufferAccess in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLBufferAccess_Type);

		PyModule_AddObject(module, "BufferAccess", (PyObject *)&MGLBufferAccess_Type);
	}

	{
		if (PyType_Ready(&MGLComputeShader_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register ComputeShader in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLComputeShader_Type);

		PyModule_AddObject(module, "ComputeShader", (PyObject *)&MGLComputeShader_Type);
	}

	{
		if (PyType_Ready(&MGLContext_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Context in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLContext_Type);

		PyModule_AddObject(module, "Context", (PyObject *)&MGLContext_Type);
	}

	{
		if (PyType_Ready(&MGLContextMember_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register ContextMember in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLContextMember_Type);

		PyModule_AddObject(module, "ContextMember", (PyObject *)&MGLContextMember_Type);
	}

	{
		if (PyType_Ready(&MGLEnableFlag_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register EnableFlag in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLEnableFlag_Type);

		PyModule_AddObject(module, "EnableFlag", (PyObject *)&MGLEnableFlag_Type);
	}

	{
		if (PyType_Ready(&MGLError_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Error in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLError_Type);

		PyModule_AddObject(module, "Error", (PyObject *)&MGLError_Type);
	}

	{
		if (PyType_Ready(&MGLFramebuffer_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Framebuffer in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLFramebuffer_Type);

		PyModule_AddObject(module, "Framebuffer", (PyObject *)&MGLFramebuffer_Type);
	}

	{
		if (PyType_Ready(&MGLFramebufferAttachment_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register FramebufferAttachment in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLFramebufferAttachment_Type);

		PyModule_AddObject(module, "FramebufferAttachment", (PyObject *)&MGLFramebufferAttachment_Type);
	}

	{
		if (PyType_Ready(&MGLInvalidObject_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register InvalidObject in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLInvalidObject_Type);

		PyModule_AddObject(module, "InvalidObject", (PyObject *)&MGLInvalidObject_Type);
	}

	{
		if (PyType_Ready(&MGLMultisampleRenderbuffer_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register MultisampleRenderbuffer in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLMultisampleRenderbuffer_Type);

		PyModule_AddObject(module, "MultisampleRenderbuffer", (PyObject *)&MGLMultisampleRenderbuffer_Type);
	}

	{
		if (PyType_Ready(&MGLMultisampleTexture_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register MultisampleTexture in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLMultisampleTexture_Type);

		PyModule_AddObject(module, "MultisampleTexture", (PyObject *)&MGLMultisampleTexture_Type);
	}

	{
		if (PyType_Ready(&MGLObject_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Object in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLObject_Type);

		PyModule_AddObject(module, "Object", (PyObject *)&MGLObject_Type);
	}

	{
		if (PyType_Ready(&MGLPrimitive_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Primitive in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLPrimitive_Type);

		PyModule_AddObject(module, "Primitive", (PyObject *)&MGLPrimitive_Type);
	}

	{
		if (PyType_Ready(&MGLProgram_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Program in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLProgram_Type);

		PyModule_AddObject(module, "Program", (PyObject *)&MGLProgram_Type);
	}

	{
		if (PyType_Ready(&MGLProgramMember_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register ProgramMember in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLProgramMember_Type);

		PyModule_AddObject(module, "ProgramMember", (PyObject *)&MGLProgramMember_Type);
	}

	{
		if (PyType_Ready(&MGLProgramStage_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register ProgramStage in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLProgramStage_Type);

		PyModule_AddObject(module, "ProgramStage", (PyObject *)&MGLProgramStage_Type);
	}

	{
		if (PyType_Ready(&MGLProgramStageMember_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register ProgramStageMember in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLProgramStageMember_Type);

		PyModule_AddObject(module, "ProgramStageMember", (PyObject *)&MGLProgramStageMember_Type);
	}

	{
		if (PyType_Ready(&MGLRenderbuffer_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Renderbuffer in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLRenderbuffer_Type);

		PyModule_AddObject(module, "Renderbuffer", (PyObject *)&MGLRenderbuffer_Type);
	}

	{
		if (PyType_Ready(&MGLShader_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Shader in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLShader_Type);

		PyModule_AddObject(module, "Shader", (PyObject *)&MGLShader_Type);
	}

	{
		if (PyType_Ready(&MGLSubroutine_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Subroutine in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLSubroutine_Type);

		PyModule_AddObject(module, "Subroutine", (PyObject *)&MGLSubroutine_Type);
	}

	{
		if (PyType_Ready(&MGLSubroutineUniform_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register SubroutineUniform in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLSubroutineUniform_Type);

		PyModule_AddObject(module, "SubroutineUniform", (PyObject *)&MGLSubroutineUniform_Type);
	}

	{
		if (PyType_Ready(&MGLTexture_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Texture in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLTexture_Type);

		PyModule_AddObject(module, "Texture", (PyObject *)&MGLTexture_Type);
	}

	{
		if (PyType_Ready(&MGLUniform_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Uniform in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLUniform_Type);

		PyModule_AddObject(module, "Uniform", (PyObject *)&MGLUniform_Type);
	}

	{
		if (PyType_Ready(&MGLUniformBlock_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register UniformBlock in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLUniformBlock_Type);

		PyModule_AddObject(module, "UniformBlock", (PyObject *)&MGLUniformBlock_Type);
	}

	{
		if (PyType_Ready(&MGLVarying_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Varying in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVarying_Type);

		PyModule_AddObject(module, "Varying", (PyObject *)&MGLVarying_Type);
	}

	{
		if (PyType_Ready(&MGLVersion_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register Version in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVersion_Type);

		PyModule_AddObject(module, "Version", (PyObject *)&MGLVersion_Type);
	}

	{
		if (PyType_Ready(&MGLVertexArray_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register VertexArray in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVertexArray_Type);

		PyModule_AddObject(module, "VertexArray", (PyObject *)&MGLVertexArray_Type);
	}

	{
		if (PyType_Ready(&MGLVertexArrayAttribute_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register VertexArrayAttribute in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVertexArrayAttribute_Type);

		PyModule_AddObject(module, "VertexArrayAttribute", (PyObject *)&MGLVertexArrayAttribute_Type);
	}

	{
		if (PyType_Ready(&MGLVertexArrayListAttribute_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register VertexArrayListAttribute in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVertexArrayListAttribute_Type);

		PyModule_AddObject(module, "VertexArrayListAttribute", (PyObject *)&MGLVertexArrayListAttribute_Type);
	}

	{
		if (PyType_Ready(&MGLVertexArrayMatrixAttribute_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register VertexArrayMatrixAttribute in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVertexArrayMatrixAttribute_Type);

		PyModule_AddObject(module, "VertexArrayMatrixAttribute", (PyObject *)&MGLVertexArrayMatrixAttribute_Type);
	}

	{
		if (PyType_Ready(&MGLVertexArrayMember_Type) < 0) {
			PyErr_Format(PyExc_ImportError, "Cannot register VertexArrayMember in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
			return false;
		}

		Py_INCREF(&MGLVertexArrayMember_Type);

		PyModule_AddObject(module, "VertexArrayMember", (PyObject *)&MGLVertexArrayMember_Type);
	}

	{
		MGL_TRIANGLES = MGLPrimitive_New();
		MGL_TRIANGLES->name = "TRIANGLES";
		MGL_TRIANGLES->primitive = GL_TRIANGLES;
		MGL_TRIANGLES->geometry_primitive = GL_TRIANGLES;
		MGL_TRIANGLES->transform_primitive = GL_TRIANGLES;
		PyModule_AddObject(module, "TRIANGLES", (PyObject *)MGL_TRIANGLES);

		MGL_TRIANGLE_STRIP = MGLPrimitive_New();
		MGL_TRIANGLE_STRIP->name = "TRIANGLE_STRIP";
		MGL_TRIANGLE_STRIP->primitive = GL_TRIANGLE_STRIP;
		MGL_TRIANGLE_STRIP->geometry_primitive = GL_TRIANGLES;
		MGL_TRIANGLE_STRIP->transform_primitive = GL_TRIANGLES;
		PyModule_AddObject(module, "TRIANGLE_STRIP", (PyObject *)MGL_TRIANGLE_STRIP);

		MGL_TRIANGLE_FAN = MGLPrimitive_New();
		MGL_TRIANGLE_FAN->name = "TRIANGLE_FAN";
		MGL_TRIANGLE_FAN->primitive = GL_TRIANGLE_FAN;
		MGL_TRIANGLE_FAN->geometry_primitive = GL_TRIANGLES;
		MGL_TRIANGLE_FAN->transform_primitive = GL_TRIANGLES;
		PyModule_AddObject(module, "TRIANGLE_FAN", (PyObject *)MGL_TRIANGLE_FAN);

		MGL_LINES = MGLPrimitive_New();
		MGL_LINES->name = "LINES";
		MGL_LINES->primitive = GL_LINES;
		MGL_LINES->geometry_primitive = GL_LINES;
		MGL_LINES->transform_primitive = GL_LINES;
		PyModule_AddObject(module, "LINES", (PyObject *)MGL_LINES);

		MGL_LINE_STRIP = MGLPrimitive_New();
		MGL_LINE_STRIP->name = "LINE_STRIP";
		MGL_LINE_STRIP->primitive = GL_LINE_STRIP;
		MGL_LINE_STRIP->geometry_primitive = GL_LINES;
		MGL_LINE_STRIP->transform_primitive = GL_LINES;
		PyModule_AddObject(module, "LINE_STRIP", (PyObject *)MGL_LINE_STRIP);

		MGL_LINE_LOOP = MGLPrimitive_New();
		MGL_LINE_LOOP->name = "LINE_LOOP";
		MGL_LINE_LOOP->primitive = GL_LINE_LOOP;
		MGL_LINE_LOOP->geometry_primitive = GL_LINES;
		MGL_LINE_LOOP->transform_primitive = GL_LINES;
		PyModule_AddObject(module, "LINE_LOOP", (PyObject *)MGL_LINE_LOOP);

		MGL_POINTS = MGLPrimitive_New();
		MGL_POINTS->name = "POINTS";
		MGL_POINTS->primitive = GL_POINTS;
		MGL_POINTS->geometry_primitive = GL_POINTS;
		MGL_POINTS->transform_primitive = GL_POINTS;
		PyModule_AddObject(module, "POINTS", (PyObject *)MGL_POINTS);

		MGL_LINE_STRIP_ADJACENCY = MGLPrimitive_New();
		MGL_LINE_STRIP_ADJACENCY->name = "LINE_STRIP_ADJACENCY";
		MGL_LINE_STRIP_ADJACENCY->primitive = GL_LINE_STRIP_ADJACENCY;
		MGL_LINE_STRIP_ADJACENCY->geometry_primitive = GL_LINES_ADJACENCY;
		MGL_LINE_STRIP_ADJACENCY->transform_primitive = GL_LINES;
		PyModule_AddObject(module, "LINE_STRIP_ADJACENCY", (PyObject *)MGL_LINE_STRIP_ADJACENCY);

		MGL_LINES_ADJACENCY = MGLPrimitive_New();
		MGL_LINES_ADJACENCY->name = "LINES_ADJACENCY";
		MGL_LINES_ADJACENCY->primitive = GL_LINES_ADJACENCY;
		MGL_LINES_ADJACENCY->geometry_primitive = GL_LINES_ADJACENCY;
		MGL_LINES_ADJACENCY->transform_primitive = GL_LINES;
		PyModule_AddObject(module, "LINES_ADJACENCY", (PyObject *)MGL_LINES_ADJACENCY);

		MGL_TRIANGLE_STRIP_ADJACENCY = MGLPrimitive_New();
		MGL_TRIANGLE_STRIP_ADJACENCY->name = "TRIANGLE_STRIP_ADJACENCY";
		MGL_TRIANGLE_STRIP_ADJACENCY->primitive = GL_TRIANGLE_STRIP_ADJACENCY;
		MGL_TRIANGLE_STRIP_ADJACENCY->geometry_primitive = GL_TRIANGLES_ADJACENCY;
		MGL_TRIANGLE_STRIP_ADJACENCY->transform_primitive = GL_TRIANGLES;
		PyModule_AddObject(module, "TRIANGLE_STRIP_ADJACENCY", (PyObject *)MGL_TRIANGLE_STRIP_ADJACENCY);

		MGL_TRIANGLES_ADJACENCY = MGLPrimitive_New();
		MGL_TRIANGLES_ADJACENCY->name = "TRIANGLES_ADJACENCY";
		MGL_TRIANGLES_ADJACENCY->primitive = GL_TRIANGLES_ADJACENCY;
		MGL_TRIANGLES_ADJACENCY->geometry_primitive = GL_TRIANGLES_ADJACENCY;
		MGL_TRIANGLES_ADJACENCY->transform_primitive = GL_TRIANGLES;
		PyModule_AddObject(module, "TRIANGLES_ADJACENCY", (PyObject *)MGL_TRIANGLES_ADJACENCY);
	}

	{
		MGL_BLEND = MGLEnableFlag_New();
		MGL_BLEND->name = "BLEND";
		MGL_BLEND->flag = GL_BLEND;
		PyModule_AddObject(module, "BLEND", (PyObject *)MGL_BLEND);

		MGL_DEPTH_TEST = MGLEnableFlag_New();
		MGL_DEPTH_TEST->name = "DEPTH_TEST";
		MGL_DEPTH_TEST->flag = GL_DEPTH_TEST;
		PyModule_AddObject(module, "DEPTH_TEST", (PyObject *)MGL_DEPTH_TEST);

		MGL_CULL_FACE = MGLEnableFlag_New();
		MGL_CULL_FACE->name = "CULL_FACE";
		MGL_CULL_FACE->flag = GL_CULL_FACE;
		PyModule_AddObject(module, "CULL_FACE", (PyObject *)MGL_CULL_FACE);

		MGL_MULTISAMPLE = MGLEnableFlag_New();
		MGL_MULTISAMPLE->name = "MULTISAMPLE";
		MGL_MULTISAMPLE->flag = GL_MULTISAMPLE;
		PyModule_AddObject(module, "MULTISAMPLE", (PyObject *)MGL_MULTISAMPLE);
	}

	{
		MGLVersion * CORE_330 = MGLVersion_New();
		CORE_330->major = 3;
		CORE_330->minor = 3;
		PyModule_AddObject(module, "CORE_330", (PyObject *)CORE_330);

		MGLVersion * CORE_400 = MGLVersion_New();
		CORE_400->major = 4;
		CORE_400->minor = 0;
		PyModule_AddObject(module, "CORE_400", (PyObject *)CORE_400);

		MGLVersion * CORE_410 = MGLVersion_New();
		CORE_410->major = 4;
		CORE_410->minor = 1;
		PyModule_AddObject(module, "CORE_410", (PyObject *)CORE_410);

		MGLVersion * CORE_420 = MGLVersion_New();
		CORE_420->major = 4;
		CORE_420->minor = 2;
		PyModule_AddObject(module, "CORE_420", (PyObject *)CORE_420);

		MGLVersion * CORE_430 = MGLVersion_New();
		CORE_430->major = 4;
		CORE_430->minor = 3;
		PyModule_AddObject(module, "CORE_430", (PyObject *)CORE_430);

		MGLVersion * CORE_440 = MGLVersion_New();
		CORE_440->major = 4;
		CORE_440->minor = 4;
		PyModule_AddObject	(module, "CORE_440", (PyObject *)CORE_440);

		MGLVersion * CORE_450 = MGLVersion_New();
		CORE_450->major = 4;
		CORE_450->minor = 5;
		PyModule_AddObject(module, "CORE_450", (PyObject *)CORE_450);
	}

	return true;
}

#if PY_MAJOR_VERSION >= 3

PyModuleDef MGL_moduledef = {
	PyModuleDef_HEAD_INIT,
	"ModernGL",
	MGL_module_doc,
	-1,
	MGL_module_methods,
	0,
	0,
	0,
	0,
};

extern "C" PyObject * PyInit_ModernGL() {
	PyObject * module = PyModule_Create(&MGL_moduledef);

	if (!MGL_InitializeModule(module)) {
		return 0;
	}

	return module;
}

#else

extern "C" PyObject * initModernGL() {
	PyObject * module = Py_InitModule("ModernGL", MGL_module_methods);

	if (!MGL_InitializeModule(module)) {
		return 0;
	}

	return module;
}

#endif

