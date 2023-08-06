#ifndef VCASHHASH_H
#define VCASHHASH_H

#ifdef __cplusplus
extern "C" {
#endif

void blake_hash(const char* input, char* output);

void whirlpoolx_hash(const char* input, char* output);

#ifdef __cplusplus
}
#endif

#endif
