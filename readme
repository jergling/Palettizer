# Palettizer
A program for generating quantized color lookup tables from a set of images

# Background:
FPV video is a unique space with a unique set of performance metrics. Where traditional videography demands color depth, motion smoothness and image completeness, drone pilots may prioritize latency and resolution above all else. For racing pilots, who have held onto traditional analog video systems, latency trumps all. For freestyle pilots, who often navigate unexplored areas with many small obstacles ("scraggle"), resolution and contrast may be more important than color accuracy or even latency.

Current market solutions take a generalized approach to color, leaning on the broad applicability of standard color space to any given image, and the reliable results produced by using the default settings on, for example, an h.264 codec with YUV8 color. These default colorspaces work well regardless of the data being transmitted, because they cover every value possible within the space. Such a scheme encodes 24 bits of color per pixel, and quite efficiently, but it could be better!

Unfortunately, hardware encoders are not general computing devices. A hardware CODEC is hard-wired to process a specific-sized image with a specific colorspace with a specific encoding with little intervention, but the job is typically passed (slowly and via framebuffer) to a CPU or GPU if soon as it strays from those specifications. Since practically every hardware CODEC on the market is designed for high-quality, non-realtime video, very little research or hardware exists for compression with alternative goals.

# Introduction:
With this project, I demonstrate a different strategy for color that reduces image depth while retaining the data most valuable to racing and freestyle FPV pilots. In this scheme, a pregenerated and pre-sorted color lookup table (CLUT or palette) is generated offline from a sample set of images which are representative of a particular environment. This indexes the RGB8 (16 million colors) color depth down to a much smaller CLUT (typically 256 to 1024 colors)

This palette on its own is unexceptional, but the means to generate it from environment-specific samples is a key step to optimization. By selecting an appropriate color palette (ex. "Daytime, Outdoors") and synchronizing this selection between encoder and decoder, the bitrate of video can be reduced with less impact to perceived color resolution. 

Further, this method would be useless for realtime compression if supplied as a bare LUT, since all 16 million indexes of the input color must be mapped to as few as 256 colors in the ouptut, which is a slow and tedious process. With a pregenerated map from every input color to a given output color, the storage required would be large (16 mB just for the 24-bit keys) and the search space would be enormous. 

Instead, this encoding packages the CLUT as an octree, which can be traversed with simple bitwise rules for fast approximate Nearest Neighbor (faNN) searching on the simplest hardware. (TODO - Implement ANN)