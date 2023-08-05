#include "Program.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"
#include "Shader.hpp"
#include "Uniform.hpp"
#include "UniformBlock.hpp"
#include "Attribute.hpp"
#include "Subroutine.hpp"
#include "SubroutineUniform.hpp"
#include "ProgramStage.hpp"
#include "Varying.hpp"

PyObject * MGLProgram_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLProgram * self = (MGLProgram *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLProgram_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLProgram_tp_dealloc(MGLProgram * self) {

	#ifdef MGL_VERBOSE
	printf("MGLProgram_tp_dealloc %p\n", self);
	#endif

	MGLProgram_Type.tp_free((PyObject *)self);
}

int MGLProgram_tp_init(MGLProgram * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Program manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLProgram_tp_str(MGLProgram * self) {
	return PyUnicode_FromFormat("<ModernGL.Program>");
}

PyObject * MGLProgram_release(MGLProgram * self) {
	MGLProgram_Invalidate(self);
	Py_RETURN_NONE;
}

char MGLProgram_release_doc[] = R"(
	release()

	Release the program object.
)";

PyMethodDef MGLProgram_tp_methods[] = {
	{"release", (PyCFunction)MGLProgram_release, METH_NOARGS, MGLProgram_release_doc},
	{0},
};

PyObject * MGLProgram_get_shaders(MGLProgram * self, void * closure) {
	Py_INCREF(self->shaders);
	return self->shaders;
}

char MGLProgram_shaders_doc[] = R"(
	shaders

	The shaders.
	The return value is a tuple.
)";

PyObject * MGLProgram_get_varyings(MGLProgram * self, void * closure) {
	Py_INCREF(self->varyings_proxy);
	return self->varyings_proxy;
}

char MGLProgram_varyings_doc[] = R"(
	varyings

	The program's varyings.
	The return value is a dictinary.
	It can be used to access varyings by name.
)";

PyObject * MGLProgram_get_uniforms(MGLProgram * self, void * closure) {
	Py_INCREF(self->uniforms_proxy);
	return self->uniforms_proxy;
}

char MGLProgram_uniforms_doc[] = R"(
	uniforms

	The program's uniforms.
	The return value is a dictinary.
	It can be used to access uniforms by name.
)";

PyObject * MGLProgram_get_uniform_blocks(MGLProgram * self, void * closure) {
	Py_INCREF(self->uniform_blocks_proxy);
	return self->uniform_blocks_proxy;
}

char MGLProgram_uniform_blocks_doc[] = R"(
	uniform_blocks

	The program's uniform blocks.
	The return value is a dictinary.
	It can be used to access uniform blocks by name.
)";

PyObject * MGLProgram_get_attributes(MGLProgram * self, void * closure) {
	Py_INCREF(self->attributes_proxy);
	return self->attributes_proxy;
}

char MGLProgram_attributes_doc[] = R"(
	attributes

	The program's attributes.
	The return value is a dictinary.
	It can be used to access attributes by name.
)";

PyObject * MGLProgram_get_geometry_input(MGLProgram * self, void * closure) {
	if (self->geometry_input) {
		Py_INCREF(self->geometry_input);
		return (PyObject *)self->geometry_input;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_geometry_input_doc[] = R"(
	geometry_input

	The geometry input primitive.
	The GeometryShader's input primitive if the GeometryShader is present otherwise ``None``.
	The geometry input primitive will be used for validation when rendering.
)";

PyObject * MGLProgram_get_geometry_output(MGLProgram * self, void * closure) {
	if (self->geometry_output) {
		Py_INCREF(self->geometry_output);
		return (PyObject *)self->geometry_output;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_geometry_output_doc[] = R"(
	geometry_output

	The geometry output primitive.
	The GeometryShader's output primitive if the GeometryShader is present otherwise ``None``.
)";

PyObject * MGLProgram_get_geometry_vertices(MGLProgram * self, void * closure) {
	return PyLong_FromLong(self->geometry_vertices);
}

char MGLProgram_geometry_vertices_doc[] = R"(
	geometry_vertices

	The maximum number of vertices that the geometry shader in program will output.
)";

PyObject * MGLProgram_get_vertex_shader(MGLProgram * self, void * closure) {
	if (self->vertex_shader) {
		Py_INCREF(self->vertex_shader);
		return self->vertex_shader;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_vertex_shader_doc[] = R"(
	vertex_shader
)";

PyObject * MGLProgram_get_fragment_shader(MGLProgram * self, void * closure) {
	if (self->fragment_shader) {
		Py_INCREF(self->fragment_shader);
		return self->fragment_shader;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_fragment_shader_doc[] = R"(
	fragment_shader
)";

PyObject * MGLProgram_get_geometry_shader(MGLProgram * self, void * closure) {
	if (self->geometry_shader) {
		Py_INCREF(self->geometry_shader);
		return self->geometry_shader;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_geometry_shader_doc[] = R"(
	geometry_shader
)";

PyObject * MGLProgram_get_tesselation_evaluation_shader(MGLProgram * self, void * closure) {
	if (self->tesselation_evaluation_shader) {
		Py_INCREF(self->tesselation_evaluation_shader);
		return self->tesselation_evaluation_shader;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_tesselation_evaluation_shader_doc[] = R"(
	tesselation_evaluation_shader
)";

PyObject * MGLProgram_get_tesselation_control_shader(MGLProgram * self, void * closure) {
	if (self->tesselation_control_shader) {
		Py_INCREF(self->tesselation_control_shader);
		return self->tesselation_control_shader;
	} else {
		Py_RETURN_NONE;
	}
}

char MGLProgram_tesselation_control_shader_doc[] = R"(
	tesselation_control_shader
)";

PyGetSetDef MGLProgram_tp_getseters[] = {
	{(char *)"shaders", (getter)MGLProgram_get_shaders, 0, MGLProgram_shaders_doc, 0},
	{(char *)"uniforms", (getter)MGLProgram_get_uniforms, 0, MGLProgram_uniforms_doc, 0},
	{(char *)"uniform_blocks", (getter)MGLProgram_get_uniform_blocks, 0, MGLProgram_uniform_blocks_doc, 0},
	{(char *)"attributes", (getter)MGLProgram_get_attributes, 0, MGLProgram_attributes_doc, 0},
	{(char *)"varyings", (getter)MGLProgram_get_varyings, 0, MGLProgram_varyings_doc, 0},

	{(char *)"geometry_input", (getter)MGLProgram_get_geometry_input, 0, MGLProgram_geometry_input_doc, 0},
	{(char *)"geometry_output", (getter)MGLProgram_get_geometry_output, 0, MGLProgram_geometry_output_doc, 0},
	{(char *)"geometry_vertices", (getter)MGLProgram_get_geometry_vertices, 0, MGLProgram_geometry_vertices_doc, 0},

	{(char *)"vertex_shader", (getter)MGLProgram_get_vertex_shader, 0, MGLProgram_vertex_shader_doc, 0},
	{(char *)"fragment_shader", (getter)MGLProgram_get_fragment_shader, 0, MGLProgram_fragment_shader_doc, 0},
	{(char *)"geometry_shader", (getter)MGLProgram_get_geometry_shader, 0, MGLProgram_geometry_shader_doc, 0},
	{(char *)"tesselation_evaluation_shader", (getter)MGLProgram_get_tesselation_evaluation_shader, 0, MGLProgram_tesselation_evaluation_shader_doc, 0},
	{(char *)"tesselation_control_shader", (getter)MGLProgram_get_tesselation_control_shader, 0, MGLProgram_tesselation_control_shader_doc, 0},
	{0},
};

// PyObject * Program_get_item(Program * self, PyObject * key) {
// }

// int Program_set_item(Program * self, PyObject * key, PyObject * value) {
// }

PyMappingMethods Program_map = {
	0,
	// (binaryfunc)Program_get_item,
	// (objobjargproc)Program_set_item,
};

const char * MGLProgram_tp_doc = R"(
)";

PyTypeObject MGLProgram_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Program",                                     // tp_name
	sizeof(MGLProgram),                                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLProgram_tp_dealloc,                      // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLProgram_tp_str,                            // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	&Program_map,                                           // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLProgram_tp_str,                            // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLProgram_tp_doc,                                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLProgram_tp_methods,                                  // tp_methods
	0,                                                      // tp_members
	MGLProgram_tp_getseters,                                // tp_getset
	&MGLContextMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLProgram_tp_init,                           // tp_init
	0,                                                      // tp_alloc
	MGLProgram_tp_new,                                      // tp_new
};

MGLProgram * MGLProgram_New() {
	MGLProgram * self = (MGLProgram *)MGLProgram_tp_new(&MGLProgram_Type, 0, 0);
	return self;
}

void MGLProgram_Invalidate(MGLProgram * program) {
	if (Py_TYPE(program) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLProgram_Invalidate %p already released\n", program);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLProgram_Invalidate %p\n", program);
	#endif

	const GLMethods & gl = program->context->gl;

	gl.DeleteProgram(program->program_obj);

	{
		MGLUniform * uniform = 0;
		Py_ssize_t pos = 0;

		while (PyDict_Next(program->uniforms, &pos, 0, (PyObject **)&uniform)) {
			MGLUniform_Invalidate(uniform);
		}

		Py_DECREF(program->uniforms);
		Py_DECREF(program->uniforms_proxy);
	}

	{
		MGLAttribute * attribute = 0;
		Py_ssize_t pos = 0;

		while (PyDict_Next(program->attributes, &pos, 0, (PyObject **)&attribute)) {
			MGLAttribute_Invalidate(attribute);
		}

		Py_DECREF(program->attributes);
		Py_DECREF(program->attributes_proxy);
	}

	{
		MGLVarying * varying = 0;
		Py_ssize_t pos = 0;

		while (PyDict_Next(program->varyings, &pos, 0, (PyObject **)&varying)) {
			MGLVarying_Invalidate(varying);
		}

		Py_DECREF(program->varyings);
		Py_DECREF(program->varyings_proxy);
	}

	{
		int shaders_len = (int)PyTuple_GET_SIZE(program->shaders);

		for (int i = 0; i < shaders_len; ++i) {
			MGLShader * shader = (MGLShader *)PyTuple_GET_ITEM(program->shaders, i);
			if (Py_REFCNT(shader) == 2) {
				MGLShader_Invalidate(shader);
			}
		}

		Py_DECREF(program->shaders);
	}

	Py_XDECREF(program->geometry_input);
	Py_XDECREF(program->geometry_output);

	Py_DECREF(program->context);

	Py_TYPE(program) = &MGLInvalidObject_Type;

	Py_DECREF(program);
}

void clean_program_member_name(char * name, int & name_len) {
	if (name_len && name[name_len - 1] == ']') {
		name_len -= 1;
		while (name_len && name[name_len] != '[') {
			name_len -= 1;
		}
	}
	name[name_len] = 0;
}

void MGLProgram_Compile(MGLProgram * program, PyObject * outputs) {
	const GLMethods & gl = program->context->gl;

	int obj = gl.CreateProgram();

	MGLShader * shaders[NUM_SHADER_SLOTS] = {};

	int num_shaders = (int)PyTuple_GET_SIZE(program->shaders);

	for (int i = 0; i < num_shaders; ++i) {
		MGLShader * shader = (MGLShader *)PyTuple_GET_ITEM(program->shaders, i);
		shaders[shader->shader_slot] = shader;

		gl.AttachShader(obj, shader->shader_obj);
	}

	if (outputs != Py_None) {
		int outputs_len = (int)PyList_GET_SIZE(outputs);

		if (outputs_len) {
			const char ** varyings_array = new const char * [outputs_len];

			for (int i = 0; i < outputs_len; ++i) {
				varyings_array[i] = PyUnicode_AsUTF8(PyList_GET_ITEM(outputs, i));
			}

			gl.TransformFeedbackVaryings(obj, outputs_len, varyings_array, GL_INTERLEAVED_ATTRIBS);

			delete[] varyings_array;
		}
	}

	gl.LinkProgram(obj);

	int linked = GL_FALSE;
	gl.GetProgramiv(obj, GL_LINK_STATUS, &linked);

	if (!linked) {
		const char * message = "GLSL Linker failed";
		const char * title = "Program";
		const char * underline = "=======";

		int log_len = 0;
		gl.GetProgramiv(obj, GL_INFO_LOG_LENGTH, &log_len);

		char * log = new char[log_len];
		gl.GetProgramInfoLog(obj, log_len, &log_len, log);

		gl.DeleteProgram(obj);

		MGLError * error = MGLError_New(TRACE, "%s\n\n%s\n%s\n%s\n", message, title, underline, log);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);

		delete[] log;
		return;
	}

	program->program_obj = obj;

	if (shaders[VERTEX_SHADER_SLOT]) {
		MGLProgramStage * program_stage = MGLProgramStage_New();
		program_stage->program_obj = program->program_obj;
		program_stage->shader = shaders[VERTEX_SHADER_SLOT];
		MGLProgramStage_Complete(program_stage, gl);
		program->vertex_shader = (PyObject *)program_stage;
	} else {
		program->vertex_shader = 0;
	}

	if (shaders[FRAGMENT_SHADER_SLOT]) {
		MGLProgramStage * program_stage = MGLProgramStage_New();
		program_stage->program_obj = program->program_obj;
		program_stage->shader = shaders[FRAGMENT_SHADER_SLOT];
		MGLProgramStage_Complete(program_stage, gl);
		program->fragment_shader = (PyObject *)program_stage;
	} else {
		program->fragment_shader = 0;
	}

	if (shaders[GEOMETRY_SHADER_SLOT]) {
		MGLProgramStage * program_stage = MGLProgramStage_New();
		program_stage->program_obj = program->program_obj;
		program_stage->shader = shaders[GEOMETRY_SHADER_SLOT];
		MGLProgramStage_Complete(program_stage, gl);
		program->geometry_shader = (PyObject *)program_stage;
	} else {
		program->geometry_shader = 0;
	}

	if (shaders[TESSELATION_EVALUATION_SHADER_SLOT]) {
		MGLProgramStage * program_stage = MGLProgramStage_New();
		program_stage->program_obj = program->program_obj;
		program_stage->shader = shaders[TESSELATION_EVALUATION_SHADER_SLOT];
		MGLProgramStage_Complete(program_stage, gl);
		program->tesselation_evaluation_shader = (PyObject *)program_stage;
	} else {
		program->tesselation_evaluation_shader = 0;
	}

	if (shaders[TESSELATION_CONTROL_SHADER_SLOT]) {
		MGLProgramStage * program_stage = MGLProgramStage_New();
		program_stage->program_obj = program->program_obj;
		program_stage->shader = shaders[TESSELATION_CONTROL_SHADER_SLOT];
		MGLProgramStage_Complete(program_stage, gl);
		program->tesselation_control_shader = (PyObject *)program_stage;
	} else {
		program->tesselation_control_shader = 0;
	}

	PyObject * uniforms = PyDict_New();

	int num_uniforms = 0;
	gl.GetProgramiv(program->program_obj, GL_ACTIVE_UNIFORMS, &num_uniforms);

	for (int i = 0; i < num_uniforms; ++i) {
		MGLUniform * uniform = MGLUniform_New();

		int name_len = 0;
		char name[256];

		gl.GetActiveUniform(program->program_obj, i, 256, &name_len, &uniform->array_length, (GLenum *)&uniform->type, name);

		uniform->location = gl.GetUniformLocation(program->program_obj, name);

		clean_program_member_name(name, name_len);

		// Skip uniforms from uniform buffers

		if (uniform->location < 0) {
			Py_DECREF((PyObject *)uniform);
			continue;
		}

		uniform->number = i;
		uniform->program_obj = program->program_obj;
		uniform->name = PyUnicode_FromStringAndSize(name, name_len);

		MGLUniform_Complete(uniform, gl);

		// TODO: check shadow and sampler cube

		PyDict_SetItem(uniforms, uniform->name, (PyObject *)uniform);
		Py_DECREF(uniform);
	}

	program->uniforms = uniforms;
	program->uniforms_proxy = PyDictProxy_New(uniforms);
	Py_INCREF(uniforms);

	PyObject * uniform_blocks = PyDict_New();

	int num_uniform_blocks = 0;
	gl.GetProgramiv(obj, GL_ACTIVE_UNIFORM_BLOCKS, &num_uniform_blocks);

	for (int i = 0; i < num_uniform_blocks; ++i) {
		MGLUniformBlock * uniform_block = MGLUniformBlock_New();

		int name_len = 0;
		char name[256];

		gl.GetActiveUniformBlockName(program->program_obj, i, 256, &name_len, name);
		gl.GetActiveUniformBlockiv(program->program_obj, i, GL_UNIFORM_BLOCK_BINDING, &uniform_block->location);
		gl.GetActiveUniformBlockiv(program->program_obj, i, GL_UNIFORM_BLOCK_DATA_SIZE, &uniform_block->array_length);

		clean_program_member_name(name, name_len);

		// if (uniform_block->location < 0) {
		// 	Py_DECREF((PyObject *)uniform_block);
		// 	continue;
		// }

		uniform_block->number = i;
		uniform_block->program_obj = program->program_obj;
		uniform_block->name = PyUnicode_FromStringAndSize(name, name_len);

		MGLUniformBlock_Complete(uniform_block, gl);

		// TODO: check shadow and sampler cube

		PyDict_SetItem(uniform_blocks, uniform_block->name, (PyObject *)uniform_block);
		Py_DECREF(uniform_block);
	}

	program->uniform_blocks = uniform_blocks;
	program->uniform_blocks_proxy = PyDictProxy_New(uniform_blocks);
	Py_INCREF(uniform_blocks);

	PyObject * attributes = PyDict_New();

	int num_attributes = 0;
	gl.GetProgramiv(program->program_obj, GL_ACTIVE_ATTRIBUTES, &num_attributes);

	for (int i = 0; i < num_attributes; ++i) {
		MGLAttribute * attribute = MGLAttribute_New();

		int name_len = 0;
		char name[256];

		gl.GetActiveAttrib(program->program_obj, i, 256, &name_len, &attribute->array_length, (GLenum *)&attribute->type, name);

		attribute->location = gl.GetAttribLocation(program->program_obj, name);

		clean_program_member_name(name, name_len);

		// if (attribute->location < 0) {
		// 	Py_DECREF(attribute);
		// 	continue;
		// }

		attribute->number = i;
		attribute->program_obj = program->program_obj;
		attribute->name = PyUnicode_FromStringAndSize(name, name_len);

		MGLAttribute_Complete(attribute, gl);

		PyDict_SetItem(attributes, attribute->name, (PyObject *)attribute);
		Py_DECREF(attribute);
	}

	program->attributes = attributes;
	program->attributes_proxy = PyDictProxy_New(attributes);
	Py_INCREF(attributes);

	PyObject * varyings = PyDict_New();

	int num_varyings = 0;
	gl.GetProgramiv(program->program_obj, GL_TRANSFORM_FEEDBACK_VARYINGS, &num_varyings);

	for (int i = 0; i < num_varyings; ++i) {
		MGLVarying * varying = MGLVarying_New();

		int name_len = 0;
		char name[256];

		gl.GetTransformFeedbackVarying(program->program_obj, i, 256, &name_len, &varying->array_length, (GLenum *)&varying->type, name);

		varying->number = i;
		varying->program_obj = program->program_obj;
		varying->name = PyUnicode_FromStringAndSize(name, name_len);

		MGLVarying_Complete(varying, gl);

		PyDict_SetItem(varyings, varying->name, (PyObject *)varying);
		Py_DECREF(varying);
	}

	program->varyings = varyings;
	program->varyings_proxy = PyDictProxy_New(varyings);
	Py_INCREF(varyings);

	if (shaders[GEOMETRY_SHADER_SLOT]) {

		int geometry_in = 0;
		int geometry_out = 0;
		program->geometry_vertices = 0;

		gl.GetProgramiv(obj, GL_GEOMETRY_INPUT_TYPE, &geometry_in);
		gl.GetProgramiv(obj, GL_GEOMETRY_OUTPUT_TYPE, &geometry_out);
		gl.GetProgramiv(obj, GL_GEOMETRY_VERTICES_OUT, &program->geometry_vertices);

		switch (geometry_in) {
			case GL_TRIANGLES:
				program->geometry_input = MGL_TRIANGLES;
				break;

			case GL_TRIANGLE_STRIP:
				program->geometry_input = MGL_TRIANGLE_STRIP;
				break;

			case GL_TRIANGLE_FAN:
				program->geometry_input = MGL_TRIANGLE_FAN;
				break;

			case GL_LINES:
				program->geometry_input = MGL_LINES;
				break;

			case GL_LINE_STRIP:
				program->geometry_input = MGL_LINE_STRIP;
				break;

			case GL_LINE_LOOP:
				program->geometry_input = MGL_LINE_LOOP;
				break;

			case GL_POINTS:
				program->geometry_input = MGL_POINTS;
				break;

			case GL_LINE_STRIP_ADJACENCY:
				program->geometry_input = MGL_LINE_STRIP_ADJACENCY;
				break;

			case GL_LINES_ADJACENCY:
				program->geometry_input = MGL_LINES_ADJACENCY;
				break;

			case GL_TRIANGLE_STRIP_ADJACENCY:
				program->geometry_input = MGL_TRIANGLE_STRIP_ADJACENCY;
				break;

			case GL_TRIANGLES_ADJACENCY:
				program->geometry_input = MGL_TRIANGLES_ADJACENCY;
				break;

			default:
				program->geometry_input = 0;
				break;
		}

		switch (geometry_out) {
			case GL_TRIANGLES:
				program->geometry_output = MGL_TRIANGLES;
				break;

			case GL_TRIANGLE_STRIP:
				program->geometry_output = MGL_TRIANGLE_STRIP;
				break;

			case GL_TRIANGLE_FAN:
				program->geometry_output = MGL_TRIANGLE_FAN;
				break;

			case GL_LINES:
				program->geometry_output = MGL_LINES;
				break;

			case GL_LINE_STRIP:
				program->geometry_output = MGL_LINE_STRIP;
				break;

			case GL_LINE_LOOP:
				program->geometry_output = MGL_LINE_LOOP;
				break;

			case GL_POINTS:
				program->geometry_output = MGL_POINTS;
				break;

			case GL_LINE_STRIP_ADJACENCY:
				program->geometry_output = MGL_LINE_STRIP_ADJACENCY;
				break;

			case GL_LINES_ADJACENCY:
				program->geometry_output = MGL_LINES_ADJACENCY;
				break;

			case GL_TRIANGLE_STRIP_ADJACENCY:
				program->geometry_output = MGL_TRIANGLE_STRIP_ADJACENCY;
				break;

			case GL_TRIANGLES_ADJACENCY:
				program->geometry_output = MGL_TRIANGLES_ADJACENCY;
				break;

			default:
				program->geometry_output = 0;
				break;
		}

		if (program->geometry_input) {
			Py_INCREF(program->geometry_input);
		}

		if (program->geometry_output) {
			Py_INCREF(program->geometry_output);
		}

	} else {

		program->geometry_input = 0;
		program->geometry_output = 0;
		program->geometry_vertices = 0;
	}
}
