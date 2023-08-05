#pragma once

#include "Python.hpp"

#include "FramebufferAttachment.hpp"

struct MGLTexture : public MGLFramebufferAttachment {
};

extern PyTypeObject MGLTexture_Type;

MGLTexture * MGLTexture_New();
void MGLTexture_Invalidate(MGLTexture * texture);
