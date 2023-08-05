#pragma once

#include "Python.hpp"

#include "FramebufferAttachment.hpp"

struct MGLMultisampleTexture : public MGLFramebufferAttachment {
};

extern PyTypeObject MGLMultisampleTexture_Type;

MGLMultisampleTexture * MGLMultisampleTexture_New();
void MGLMultisampleTexture_Invalidate(MGLMultisampleTexture * texture);
