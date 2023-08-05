#pragma once

#include "Python.hpp"

#include "Object.hpp"

#include "GLMethods.hpp"
#include "GLContext.hpp"

struct MGLContext : public MGLObject {
	PyObject * default_framebuffer;

	GLContext gl_context;

	int max_texture_units;
	int default_texture_unit;

	GLMethods gl;
};

extern PyTypeObject MGLContext_Type;

MGLContext * MGLContext_New();
void MGLContext_Invalidate(MGLContext * context);
void MGLContext_Initialize(MGLContext * self);
