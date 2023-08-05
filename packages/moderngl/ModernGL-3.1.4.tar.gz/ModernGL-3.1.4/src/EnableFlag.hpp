#pragma once

#include "Python.hpp"

#include "Object.hpp"

struct MGLEnableFlag : public MGLObject {
	const char * name;
	int flag;
};

extern PyTypeObject MGLEnableFlag_Type;

MGLEnableFlag * MGLEnableFlag_New();

extern MGLEnableFlag * MGL_BLEND;
extern MGLEnableFlag * MGL_DEPTH_TEST;
extern MGLEnableFlag * MGL_CULL_FACE;
extern MGLEnableFlag * MGL_MULTISAMPLE;
