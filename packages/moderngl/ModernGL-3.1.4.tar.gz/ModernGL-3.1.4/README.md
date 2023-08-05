# ModernGL
:boom: modern OpenGL binding for Python

## [Docs](https://moderngl.github.io) and [Examples](https://moderngl.github.io/Examples.html)

## Description

OpenGL is a great environment for developing portable, platform independent,
interactive 2D and 3D graphics applications. The API implementation in Python
is cumbersome, resulting in applications with high latency. To solve this
problem we have developed ModernGL, a wrapper over OpenGL that simplifies the
creation of simple graphics applications like scientific simulations, small
games or user interfaces. Usually, acquiring in-depth knowledge of OpenGL
requires a steep learning curve. In contrast, ModernGL is easy to learn and
use, moreover it is capable of rendering with the same performance and
quality, with less code written.

## Sample

```py

ctx = ModernGL.create_context()

prog = ctx.Program([
	ctx.VertexShader('''
		#version 330
		in vec2 vert;
		void main() {
			gl_Position = vec4(vert, 0.0, 1.0);
		}
	'''),
	ctx.FragmentShader('''
		#version 330
		out vec4 color;
		void main() {
			color = vec4(0.2, 0.6, 0.9, 1.0);
		}
	'''),
])

vbo = ctx.Buffer(struct.pack('6f', 0, 0, 1, 0, 0, 1))
vao = ctx.SimpleVertexArray(prog, vbo, '2f', ['vert'])

vao.render(ModernGL.TRIANGLES)

```

## How to install

```
pip install ModernGL
```

-----

for **Ubuntu**:
```
apt-get install python3-dev libgl1-mesa-dev libx11-dev
pip3 install ModernGL
```

...
